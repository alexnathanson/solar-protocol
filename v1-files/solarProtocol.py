'''
This script retreives PV data from other servers.
Compares data between devices and identifies the primary.
If the local devices is the primary it updates the DNS system.
'''

import requests
import os
import fileinput
import json

#terminal command to update DNS record
subCall = 'python /home/pi/dynamic-IP-updater/cloudFlare-dynamic-IP-updater.py'

#localPVData = ""

'''
possible values (use "-" instead of spaces):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
'''
apiValue = 'PV-voltage'

deviceList = "/home/pi/distributed-dynamic-IP-exchanger-API/v1-files/deviceList.json";

#return data from a particular server
def getData(dst):
	#returns a single value
	response = requests.get('http://' + dst + '/api.php?value='+apiValue)
	#print(response)

	return response.text

def remoteData():
	allData = []

	for dst in dstIPs:
		#print(dst)
		allData.append(getData(dst))

	print("ALL DATA:")
	print(allData)

	#determineServer(allData)

def determineServer(arrayOfData):

	thisServer = True

	#loop through data from all servers and compare voltages
	for s in arrayOfData:
		print(s['pvData']['voltage'])
		print(localPVData['pvData']['voltage'])
		if float(s['pvData']['voltage'])>float(localPVData['pvData']['voltage']):
			thisServer = False

	if thisServer:
		print('Point of contact')
		os.system(subCall)

def localData():
	#get the local PV data

	# read file
	with open('/var/www/html/pvData.json', 'r') as myfile:
	    data=myfile.read()

	return json.loads(data)


def getIPList():

	ipList = []

	with open(deviceList) as f:
	  data = json.load(f)

	#print(data)

	for i in range(len(data)):
		ipList.append(data[i]['ip'])

	#print(ipList)

	return ipList

localPVData = localData()
dstIPs = getDstIPs()
remoteData()