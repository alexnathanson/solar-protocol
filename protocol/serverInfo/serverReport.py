"""
This script is not currently in use, but may have some utility in the future.
(For example, if we want server-status to be private this could package it up and pipe it out via the API in a more controlled way.)

USAGE:

This script reads and parses an apache log file. It combines it with the server-status info and generates a report with:

* all the auto server status info
* all time total amount of unique hosts
* all time amount of unique hosts (exluding SP network devices)
* 72 hours total amount of unique hosts
* 72 hours total amount of unique hosts (exluding SP network devices)

Re from https://www.seehuhn.de/blog/52.html

Apache Logging Basics: https://www.loggly.com/ultimate-guide/apache-logging-basics/
"""

import csv
import re
import requests
import json
import datetime
from dateutil.parser import parse
from logging import debug, error, info

deviceList = "/data/devices.json"

log_file_name = "/var/log/apache2/access.log"

json_file_name = "/home/pi/local/server-report.json"

# ignore these loopback addresses
ignoreLocalHosts = [
    "::1",
    "0000:0000:0000:0000:0000:0000:0000:0001",
    "127.0.0.1",
    "localhost",
]

parts = [
    r"(?P<host>\S+)",  # host %h
    r"\S+",  # indent %l (unused)
    r"(?P<user>\S+)",  # user %u
    r"\[(?P<time>.+)\]",  # time %t
    r'"(?P<request>.+)"',  # request "%r"
    r"(?P<status>[0-9]+)",  # status %>s
    r"(?P<size>\S+)",  # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',  # referer "%{Referer}i"
    r'"(?P<agent>.*)"',  # user agent "%{User-agent}i"
]

pattern = re.compile(r"\s+".join(parts) + r"\s*\Z")


def parseLogFile(logfile):
    logFileStats = {}

    spIPList = getKeyList("ip")

    spDevices = []
    exDevices = []

    debug(type(logfile))

    # firstLine = ''
    # lastLine = ''
    # fL = True

    # convert each line of the log file into a dictionary
    for line in logfile:
        # if fL:
        #     firstLine = line
        #     fL = False

        """filter out the hex stuff that is fucking shit up
        x00 may represent failed requests from https"""
        if "\x00" not in line:
            m = pattern.match(line)
            mDict = m.groupdict()
            line_dict = convertApacheToPython(mDict)

            # check that the IP isn't in the local hosts list
            if line_dict["host"] not in ignoreLocalHosts:
                # create list of logs from SP devices
                if line_dict["host"] in spIPList:
                    spDevices.append(line_dict)
                # create list of logs from SP devices
                else:
                    exDevices.append(line_dict)

        # lastLine = line

    # all time unique SP hosts
    spHosts = {}
    # all time requests from SP hosts
    spReq = 0
    # past 72 SP hosts
    spHosts72 = {}
    # past 72 SP requests
    spReq72 = 0

    # days
    tDelta = 1

    for line in spDevices:
        # create dictionary of all hosts and requests
        if line["host"] in spHosts.keys():
            spHosts[line["host"]] = spHosts[line["host"]] + 1
        else:
            spHosts[line["host"]] = 1
        spReq = spReq + 1

        # filter to the only data logged within a given delta
        if line["time"].replace(
            tzinfo=None
        ) > datetime.datetime.now() - datetime.timedelta(tDelta):
            # create dictionary of all hosts and requests
            if line["host"] in spHosts72.keys():
                spHosts72[line["host"]] = spHosts72[line["host"]] + 1
            else:
                spHosts72[line["host"]] = 1
            spReq72 = spReq72 + 1

    # total amount of hosts making requests
    logFileStats["allSPHosts"] = len(spHosts.keys())
    # total amount of requests
    logFileStats["allSPRequests"] = spReq
    # total amount of hosts making requests
    logFileStats["filteredSPHosts"] = len(spHosts72.keys())
    # total amount of requests
    logFileStats["filteredSPRequests"] = spReq72

    # get non Solar Protocol host making requests

    # all time unique SP hosts
    exHosts = {}
    # all time requests from SP hosts
    exReq = 0
    # past 72 SP hosts
    exHosts72 = {}
    # past 72 SP requests
    exReq72 = 0

    for line in exDevices:
        # create dictionary of all hosts and requests
        if line["host"] in exHosts.keys():
            exHosts[line["host"]] = exHosts[line["host"]] + 1
        else:
            exHosts[line["host"]] = 1
        exReq = exReq + 1

        # filter to the only data logged within a given delta
        if line["time"].replace(
            tzinfo=None
        ) > datetime.datetime.now() - datetime.timedelta(tDelta):
            # create dictionary of all hosts and requests
            if line["host"] in exHosts72.keys():
                exHosts72[line["host"]] = exHosts72[line["host"]] + 1
            else:
                exHosts72[line["host"]] = 1
            exReq72 = exReq72 + 1

    # total amount of hosts making requests
    logFileStats["allExHosts"] = len(exHosts.keys())
    # total amount of requests
    logFileStats["allExRequests"] = exReq
    # total amount of hosts making requests
    logFileStats["filteredExHosts"] = len(exHosts72.keys())
    # total amount of requests
    logFileStats["filteredExRequests"] = exReq72

    return logFileStats


# pass in a Apache log line converted to a dictionary
# based on code from https://www.seehuhn.de/blog/52.html
def convertApacheToPython(lineDict):
    # convert Apache format to Python data types (not really necessary for us...)
    if lineDict["user"] == "-":
        lineDict["user"] = None

    lineDict["status"] = int(lineDict["status"])

    if lineDict["size"] == "-":
        lineDict["size"] = 0
    else:
        lineDict["size"] = int(lineDict["size"])

    if lineDict["referer"] == "-":
        lineDict["referer"] = None

    # convert string to timezone aware datetime object
    # source: https://nablux.net/tgp/weblog/2013/10/29/parsing-timestamps-apache-log-files-python/
    lineTime = lineDict["time"]
    lineDict["time"] = parse(lineTime[:11] + " " + lineTime[12:])

    return lineDict


# pass in the return info from the server-status?auto
def parseServerStatus(autoStatus):
    autoStatusLines = autoStatus.splitlines()

    statusDict = {}

    for line in autoStatusLines:
        splitPos = line.find(":")
        # check if there is no delineator
        if splitPos != -1:
            # remove leading and trailing whitespace and line breaks
            statusDict[line[0:splitPos]] = (
                line[splitPos + 1 :].replace("\n", "").strip()
            )
        else:
            statusDict["URL"] = line.replace("\n", "").strip()

    debug("server status {statusDict.keys()}")

    return statusDict


def getRequest(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except requests.exceptions.HTTPError as err:
        error(err)
    except requests.exceptions.Timeout as err:
        error(err)
    except requests.exceptions.RequestException as err:
        error(err)


def getKeyList(getKey):
    ipList = []

    with open(deviceList) as f:
        data = json.load(f)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList


def writeReport(fReport):
    with open(json_file_name, "w") as reportFile:
        json.dump(fReport, reportFile)


if __name__ == "__main__":
    # get current server status
    # FIXME: DOES THIS NEED TO PULL PORT???
    serverStatus = getRequest("http://localhost/server-status?auto")
    serverStatDict = parseServerStatus(serverStatus)
    info(serverStatDict)

    try:
        infile = open(log_file_name, "r")
    except IOError:
        error("You must specify a valid file to parse")
        error(__doc__)

    logDict = parseLogFile(infile)
    info(logDict)

    # merge dictionaries into the final report
    finalReport = {**serverStatDict, **logDict}
    info("***FINAL REPORT***")
    info(finalReport)
    writeReport(finalReport)

    infile.close()
