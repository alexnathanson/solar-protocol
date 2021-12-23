"""
USAGE:

This script reads and parses an apache log file. It combines it with the server-status info and generates a report with:

* server creation time
* current time
* server up time
* all time total amount of unique hosts
* all time amount of unique hosts (exluding SP network devices)
* 7 days total amount of unique hosts
* 7 days total amount of unique hosts (exluding SP network devices)

Are there relevent errors to display?

Re from https://www.seehuhn.de/blog/52.html

Apache Logging Basics: https://www.loggly.com/ultimate-guide/apache-logging-basics/
"""

import csv
import re
import requests

log_file_name = "/var/log/apache2/access.log"

csv_file_name = "server-report.csv"

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
    
    hosts = {}

    lineCount = 0
    for line in logfile:
        lineCount = lineCount + 1
        m = pattern.match(line)
        mDict = m.groupdict()

        line_dict = convertApacheToPython(mDict)
        #print(line_dict)
        
        #create dictionary of all hosts and requests
        if line_dict['host'] in hosts.keys():
            hosts[line_dict['host']] = hosts[line_dict['host']] + 1
        else:
            hosts[line_dict['host']] = 1

    #total amount of hosts making requests
    logFileStats['totalHosts'] = len(hosts.keys())
    #total amount of requests
    logFileStats['totalRequests'] = lineCount

    externalHosts = {}
    totExReq = 0
    for h in hosts.keys():
        #check that the IP isn't in the ignore lists
        if h not in ignoreLocalHosts:
            #these x00 may represent failed requests from https
            # if 'x00' not in h:
            if h.find('x00') == -1:
                externalHosts[h] = hosts[h]
                totExReq = totExReq + hosts[h]
        
    #amount of hosts making requests excluding SP devices
    logFileStats['externalHosts'] = len(externalHosts.keys())

    #total amount of requests excluding SP devices
    logFileStats['externalRequests'] = totExReq

    print("TOTALS")
    print(logFileStats)

    print(hosts.keys())

    return logFileStats

#pass in a Apache log line converted to a dictionary
#based on code from https://www.seehuhn.de/blog/52.html
def convertApacheToPython(lineDict):
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

    return lineDict

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

def writeReport(fReport):

    with open(csv_file_name, 'w') as out:
        csv_out=csv.writer(out)

        csv_out.writerow(['server built', 'current time','server uptime', 'total requesting hosts', 'total requesting hosts excluding SP devices','7 day total requesting hosts', '7 day total requesting hosts excluding SP devices'])

        # for line in file:
        #     m = pattern.match(line)
        #     result = m.groups()
        #     csv_out.writerow(result)

if __name__ == "__main__":
    
    #get current server status
    #DOES THIS NEED TO PULL PORT???
    serverStatus = getRequest("http://localhost/server-status?auto")
    print(serverStatus)
    
    try:
        infile = open(log_file_name, 'r')
    except IOError:
        print ("You must specify a valid file to parse")
        print (__doc__)
    log_report = parseLogFile(infile)
    # print (log_report)
    infile.close()