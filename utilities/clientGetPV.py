'''
A script to test API GET requests
Arguments
0 = dst
1 = key
2 = value
'''

import requests, sys

dst = sys.argv[0]

'''Value
possible values (use - instead of space):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
'''
if sys.argv[1] == 'value':
	url = 'http://'+dst+'/api/v1/api.php?value='+sys.argv[2]

'''Line'''
if sys.argv[1] == 'line':
	url = 'http://'+dst+'/api/v1/api.php?line=head'+sys.argv[2]

'''File'''
if sys.argv[0] == 'file':
	url = 'http://'+dst+'/api/v1/api.php?file=list'+sys.argv[2]

PVdata = requests.get(url).text
print(PVdata)