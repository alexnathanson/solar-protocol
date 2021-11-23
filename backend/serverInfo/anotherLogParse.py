#!/usr/bin/env python

"""
from: https://medium.com/devops-challenge/apache-log-parser-using-python-8080fbc41dda

USAGE:

logparsing_apache.py apache_log_file

This script takes apache log file as an argument and then generates a report, with hostname,
bytes transferred and status

"""

import sys

log_file_name = "/var/log/apache2/access.log"

def apache_output(line):
    split_line = line.split()
    return {'remote_host': split_line[0],
            'apache_status': split_line[8],
            'data_transfer': split_line[9],
    }


def final_report(logfile):
    for line in logfile:
        line_dict = apache_output(line)
        print(line_dict)


if __name__ == "__main__":
    
    try:
        infile = open(log_file_name, 'r')
    except IOError:
        print ("You must specify a valid file to parse")
        print (__doc__)
        sys.exit(1)
    log_report = final_report(infile)
    print (log_report)
    infile.close()