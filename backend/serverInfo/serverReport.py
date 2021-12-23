"""
USAGE:

This script reads and parses an apache log file. It combines it with the server-status info and generates a report with:

* server creation time
* current time
* server up time
* all time total amount of unique hosts
* all time amount of unique hosts (exluding SP network devices)
* 7 days total amount of unique hosts - not implemented
* 7 days total amount of unique hosts (exluding SP network devices) - not implemented

Are there relevent errors to display?

Re from https://www.seehuhn.de/blog/52.html

Apache Logging Basics: https://www.loggly.com/ultimate-guide/apache-logging-basics/
"""

import csv
import re
import requests
import json
import datetime
from dateutil.parser import parse

deviceList = "/home/pi/solar-protocol/backend/api/v1/deviceList.json"

log_file_name = "/var/log/apache2/access.log"

json_file_name = "/home/pi/local/server-report.json"

#ignore these loopback addresses
ignoreLocalHosts = ["::1","0000:0000:0000:0000:0000:0000:0000:0001","127.0.0.1","localhost"]

parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]

pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

def parseLogFile(logfile):
    logFileStats = {}
    
    spIPList = getKeyList('ip')

    spDevices = []
    exDevices = []

    #convert each line of the log file into a dictionary
    for line in logfile:

        '''filter out the hex stuff that is fucking shit up
        x00 may represent failed requests from https'''
        if '\x00' not in line:
            m = pattern.match(line)
            mDict = m.groupdict()
            line_dict = convertApacheToPython(mDict)
            
            #check that the IP isn't in the local hosts list
            if line_dict['host'] not in ignoreLocalHosts:
                #create list of logs from SP devices
                if line_dict['host'] in spIPList:
                    spDevices.append(line_dict)
                #create list of logs from SP devices
                else:
                    exDevices.append(line_dict)

    #all time unique SP hosts
    spHosts = {}
    #all time requests from SP hosts
    spReq = 0
    #past 72 SP hosts
    spHosts72 = {}
    #past 72 SP requests
    spReq72 = 0

    for line in spDevices:
        #create dictionary of all hosts and requests
        if line['host'] in spHosts.keys():
            spHosts[line['host']] = spHosts[line['host']] + 1
        else:
            spHosts[line['host']] = 1
        spReq = spReq + 1

        print(line['time'])
        print(type(line['time']))

        #filter to the only data logged in the last 72 hours
        # if line['time'] > datetime.datetime.now() - datetime.timedelta(3):
        #     #create dictionary of all hosts and requests
        #     if line['host'] in spHosts.keys():
        #         spHosts72[line['host']] = spHosts72[line['host']] + 1
        #     else:
        #         spHosts72[line['host']] = 1
        #     spReq72 = spReq72 + 1


    #total amount of hosts making requests
    logFileStats['allSPHosts'] = len(spHosts.keys())
    #total amount of requests
    logFileStats['allSPRequests'] = spReq
    #total amount of hosts making requests
    logFileStats['72SPHosts'] = len(spHosts72.keys())
    #total amount of requests
    logFileStats['72SPRequests'] = spReq72


    # #get non Solar Protocol host making requests
    # externalHosts = {}
    # totExReq = 0

    # for h in hosts.keys():
    #     #check that the IP isn't in the network devices list
    #     if h not in spIPList:
    #         #these x00 may represent failed requests from https
    #         if '\x00' not in h:
    #             externalHosts[h] = hosts[h]
    #             totExReq = totExReq + hosts[h]
        


    return logFileStats

#pass in a Apache log line converted to a dictionary
#based on code from https://www.seehuhn.de/blog/52.html
def convertApacheToPython(lineDict):
    print(lineDict)

    #convert Apache format to Python data types (not really necessary for us...)
    if lineDict["user"] == "-":
        lineDict["user"] = None

    lineDict["status"] = int(lineDict["status"])

    if lineDict["size"] == "-":
        lineDict["size"] = 0
    else:
        lineDict["size"] = int(lineDict["size"])

    if lineDict["referer"] == "-":
        lineDict["referer"] = None

    #convert string to timezone aware datetime object
    lineTime = lineDict["time"]
    lineDict["time"] = parse(lineTime[:11]+ " " + lineTime[12:])

    return lineDict

#pass in the return info from the server-status?auto
def parseServerStatus(autoStatus):
    autoStatusLines = autoStatus.splitlines()

    statusDict = {}

    for line in autoStatusLines:
        splitPos = line.find(":")
        #check if there is no delineator
        if(splitPos != -1):
            #remove leading and trailing whitespace and line breaks
            statusDict[line[0:splitPos]] = line[splitPos + 1:].replace("\n", "").strip()
        else:
            statusDict['URL'] = line.replace("\n", "").strip()

    # print("server status")
    # print(statusDict.keys())

    return statusDict

def getRequest(url):
        try:            
            response = requests.get(url, timeout = 5)
            return response.text       
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.Timeout as err:
            print(err)
        except requests.exceptions.RequestException as err:
            print(err)

def getKeyList(getKey):

    ipList = []

    with open(deviceList) as f:
      data = json.load(f)

    #print(data)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList

def writeReport(fReport):


        f = open(json_file_name, "w")

        json.dump(fReport, f)

        f.close()


    # with open(csv_file_name, 'w') as out:
    #     csv_out=csv.writer(out)
        #csv_out.writerow(['server built', 'current time','server uptime', 'total requesting hosts', 'total requesting hosts excluding SP devices','7 day total requesting hosts', '7 day total requesting hosts excluding SP devices'])


if __name__ == "__main__":
    
    #get current server status
    #DOES THIS NEED TO PULL PORT???
    serverStatus = getRequest("http://localhost/server-status?auto")
    serverStatDict = parseServerStatus(serverStatus)
    print(serverStatDict)

    try:
        infile = open(log_file_name, 'r')
    except IOError:
        print ("You must specify a valid file to parse")
        print (__doc__)

    logDict = parseLogFile(infile)
    print(logDict)

    #merge dictionaries into the final report
    finalReport = {**serverStatDict,**logDict}
    print("***FINAL REPORT***")
    print (finalReport)
    writeReport(finalReport)

    infile.close()