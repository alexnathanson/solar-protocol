'''
A script to test API GET requests
Arguments
1 = dst
2 = key
3 = value
'''

import requests, sys

print(sys.argv)

dst = sys.argv[1]

url = ''

'''Value
possible values (use - instead of space):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
'''
if sys.argv[2] == 'value':
	url = 'http://'+dst+'/api/v1/api.php?value='+sys.argv[3]

'''Line'''
if sys.argv[2] == 'line':
	url = 'http://'+dst+'/api/v1/api.php?line='+sys.argv[3]

'''File'''
if sys.argv[2] == 'file':
	url = 'http://'+dst+'/api/v1/api.php?file='+sys.argv[3]

PVdata = requests.get(url).text
print(PVdata)