'''
This script retreives PV data from other servers.
Compares data between devices and identifies the primary.
If the local devices is the primary it updates the DNS system.
'''

import requests
import os
import fileinput
import json
import datetime
import csv
#import pandas

#terminal command to update DNS record
subCall = 'python /home/pi/dynamic-IP-updater/cloudFlare-dynamic-IP-updater.py'

#localPVData = ""

'''
possible values (use "-" instead of spaces):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
'''
dataValue = 'PV voltage'
apiValue = 'PV-voltage'

deviceList = "/home/pi/distributed-dynamic-IP-exchanger-API/v1-files/deviceList.json"

localDataFile = "/home/pi/EPSolar_Tracer/data/tracerData"+ str(datetime.date.today()) +".csv"

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

	csvArray = []

	#get the local PV data
	with open(localDataFile, mode='r') as csvfile:
		localPVData = csv.reader(csvfile)

		for row in localPVData:
		 	csvArray.append(row)

		print(csvArray)

		#loop through headers to determine position of value needed
		for v in range(len(csvArray[0])):
			if csvArray[0][v] == dataValue:
				return csvArray[-1][v]

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
print(localPVData)
#dstIPs = getDstIPs()
#remoteData()