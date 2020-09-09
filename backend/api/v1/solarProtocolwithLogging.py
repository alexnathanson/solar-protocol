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

logging.basicConfig(filename='/home/pi/solar-protocol/backend/api/v1/poc.log', level=logging.INFO)

#return data from a particular server
def getData(dst):
	try:
		#returns a single value
		response = requests.get('http://' + dst + '/api/v1/api.php?value='+apiValue)
		#print(response)
		return response.text
	except requests.exceptions.HTTPError as err:
		return err

#this posts info across the network if it is the Point of Contact (not working yet)
# def postPoint(ipList):
	
# 	#myName should be read from a centralized json...
# 	myName = ""

# 	myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&name="+myName
# 	print(myString)

# 	for dst in ipList:
# 		print("DST: " + dst)
# 		#if statement only necessary if storing local IP... if not storing local IP, must auto Post regulary instead of checking for changes...
# 		#if dst != myIP: #does not work when testing only with local network
# 		try:
# 			x = requests.post('http://'+dst+'/api/v1/api.php', headers=headers,data = myString)
# 			print(x.text)
# 			#requests.raise_for_status()
# 		except requests.exceptions.HTTPError as errh:
# 		 	print("An Http Error occurred:" + repr(errh))
# 		except requests.exceptions.ConnectionError as errc:
# 			print("An Error Connecting to the API occurred:" + repr(errc))
# 		except requests.exceptions.Timeout as errt:
# 		 	print("A Timeout Error occurred:" + repr(errt))
# 		except requests.exceptions.RequestException as err:
# 		 	print("An Unknown Error occurred" + repr(err))

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

	#loop through data from all servers and compare voltages
	for s in remotePVData:
		if s > localPVData:
			thisServer = False

	if thisServer:
		print('Point of contact')

		logging.info(datetime.datetime.now())

		#comment back in to run
		os.system(subCall)
	else:
		print('Not point of contact')
		logging.info(datetime.datetime.now())#comment this out after testing

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


myMAC = getmac("wlan0")
#print("my mac: " + myMAC)

localPVData = localData()
#print("My Voltage: "+localPVData)
remotePVData = remoteData(getIPList())
#print("Remote Voltage: " + remotePVData)
determineServer()