'''
A script to test get requests
'''

import requests

dstIP = '192.168.1.180'
'''
possible values (use - instead of space):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
'''
url = 'http://'+dstIP+'/api.php?value=PV-voltage'

PVdata = 	requests.get(url).text
print(PVdata)