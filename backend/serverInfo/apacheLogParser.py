#!/usr/bin/env python

"""
USAGE:

This script reads and parses an apache log file. It combines it with the server-status info and generates a report with:

* server creation time
* server up time
* all time total amount of unique hosts
* all time amount of unique hosts (exluding SP network devices)
* 7 days total amount of unique hosts
* 7 days total amount of unique hosts (exluding SP network devices)

Are there relevent errors to display?

"""

import csv
import re

log_file_name = "/var/log/apache2/access.log"

csv_file_name = "server-report.csv"

#ignore these loopback addresses
ignoreHosts = ["::1","0000:0000:0000:0000:0000:0000:0000:0001","127.0.0.1","localhost"]

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

'''
for line in file:
    m = pattern.match(line)
    result = m.groups()
    csv_out.writerow(result)
'''

# def apache_output(line):
#     split_line = line.split()
#     return {'remote_host': split_line[0],
#             #'apache_status': split_line[8],
#             #'data_transfer': split_line[9],
#     }


def final_report(logfile):
    hosts = {}

    for line in logfile:
        m = pattern.match(line)
        line_dict = m.groupdict()
        print(line_dict)
        #line_dict = apache_output(line)

        #check that the IP isn't in the ignore lists
        if line_dict['host'] not in ignoreHosts:
            #these x00 may represent failed requests from https
            if 'x00' not in line_dict['host']:
                if line_dict['host'] in hosts.keys():
                    hosts[line_dict['host']] = hosts[line_dict['host']] + 1
                else:
                    hosts[line_dict['host']] = 1
        #print(line_dict)
    
    return hosts


if __name__ == "__main__":
    
    try:
        infile = open(log_file_name, 'r')
    except IOError:
        print ("You must specify a valid file to parse")
        print (__doc__)
    log_report = final_report(infile)
    print (log_report)
    print(len(log_report))
    infile.close()