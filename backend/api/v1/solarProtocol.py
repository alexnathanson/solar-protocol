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
import logging

#terminal command to update DNS record
subCall = 'sudo sh /home/pi/solar-protocol/backend/update_ip2.sh'

'''
possible values (use "-" instead of spaces):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
'''
dataValue = 'PV voltage'
apiValue = 'PV-voltage'

deviceList = "/home/pi/solar-protocol/backend/api/v1/deviceList.json"

localDataFile = "/home/pi/solar-protocol/charge-controller/data/tracerData"+ str(datetime.date.today()) +".csv"

logging.basicConfig(filename='/home/pi/solar-protocol/backend/api/v1/poe.log', level=logging.INFO)

#return data from a particular server
def getData(dst):
	try:
		#returns a single value
		response = requests.get('http://' + dst + '/api/v1/chargecontroller.php?value='+apiValue, timeout = 5)
		#print(response.text)		
		#check if the response can be converted to a float
		# try:
		# 	response = requests.get('http://' + dst + '/api/v1/chargecontroller.php?value='+apiValue, timeout = 5) 
		#this was in the try
		return float(response.text)
		# except:
		# 	return -1
	except requests.exceptions.HTTPError as err:
		print(err)
		return -1
	except requests.exceptions.Timeout as err:
		print(err)
		return -1
	except:
		return -1

def remoteData(dstIPs):
	allData = []

	for dst in dstIPs:
		#print(dst)
		allData.append(getData(dst))

	#print("ALL DATA:")
	#print(allData)

	return allData
	#determineServer(allData)

def determineServer():

	thisServer = True

	#print(remotePVData)

	#loop through data from all servers and compare voltages
	for s in remotePVData:
		if s > localPVData:
			thisServer = False

	if thisServer:
		print('Point of entry')

		logging.info(datetime.datetime.now())

		#comment back in to run
		os.system(subCall)
	else:
		print('Not point of entry')
		#logging.info(datetime.datetime.now())#comment this out after testing

def localData():

	csvArray = []

	#get the local PV data
	with open(localDataFile, mode='r') as csvfile:
		localPVData = csv.reader(csvfile)

		for row in localPVData:
		 	csvArray.append(row)

		#print(csvArray)

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
		#filter out local device's mac address
		if str(data[i]['mac']).strip() !=  myMAC.strip():
			ipList.append(data[i]['ip'])

	#print(ipList)

	return ipList

#this only works with linux
def getmac(interface):

	try:
		mac = open('/sys/class/net/'+interface+'/address').readline()
	except:
		mac = "00:00:00:00:00:00"

	return mac


#this should be wlan0 even if using ethernet, because its used for identifying hardware regardless of how the connection is made...
myMAC = getmac("wlan0")
#print("my mac: " + myMAC)

localPVData = float(localData())
#print("My Voltage: "+localPVData)
remotePVData = remoteData(getIPList())
#print("Remote Voltage: " + remotePVData)
determineServer()