'''
Every server runs this script.
This script retreives live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) and updates the DNS system.
Otherwise, the script changes nothing.
'''
import os
import fileinput
import datetime
import csv
import logging
import requests
import json
import sys

#globals
# SP = 0

if os.environ.get("ENV") == "DEV" or 'DEV' in sys.argv:
	dataRoot = "../../dev-data/"
	deviceList = dataRoot + "devicelist.json"
	#localConfig = dataRoot + "local.json"
	localDataFile = dataRoot + "testtracerdata.csv"
	envVar = "this-will-fail"
	DEV = True
else:
	deviceList = "/home/pi/solar-protocol/backend/data/deviceList.json"
	localDataFile = "/home/pi/solar-protocol/charge-controller/data/tracerData"+ str(datetime.date.today()) +".csv"
	envVar = str(SP.getEnv('DNS_KEY'))
	
consoleOutput = True

dnsKey = ''

'''
possible values for dataValue (use "-" instead of spaces):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
possible values for apiValue include all of the above + scaled-wattage
'''
#this is the value to be retrieved locally (and then scaled). It could potentially be retrieved via an API call to itself, which might make code cleaner
dataValue = 'PV power L'
#this is the key to retrieve from remote devices
apiValue = 'scaled-wattage'

#return data from a particular server
# this is redundant with the class... add this error handling to the class?
def getData(dst, chosenApiValue):

	try:
		#returns a single value
		response = requests.get('http://' + dst + '/api/v1/chargecontroller.php?value='+chosenApiValue, timeout = 5)
		#print(response.text)		
		#check if the response can be converted to a float
		return float(response.text)
	except requests.exceptions.HTTPError as err:
		print(err)
		return -1
	except requests.exceptions.Timeout as err:
		print(err)
		return -1
	except:
		return -1

def remoteData(dstIPs, chosenApiValue):
	allData = []

	for dst in dstIPs:
		#print(dst)
		allData.append(getData(dst, chosenApiValue))

	# print("ALL DATA:")
	# print(allData)

	return allData
	#determineServer(allData)

def determineServer(remoteData,localData, SP):

	thisServer = True

	#print(remotePVData)

	#loop through data from all servers and compare scaled wattage
	for s in remoteData:
		if s > localData:
			thisServer = False

	if thisServer:
		print('Point of entry')

		logging.info(datetime.datetime.now())
		
		#print(SP.myIP)
		#print(SP.getEnv('DNS_KEY'))

		#getDNS(requests.get('https://server.solarpowerforartists.com/?myip').text)
		#SP.getRequest(SP.updateDNS(SP.myIP,str(SP.getEnv('DNS_KEY'))), False)
		SP.getRequest(SP.updateDNS(SP.myIP,envVar), False)

	else:
		print('Not point of entry')
		#logging.info(datetime.datetime.now())#comment this out after testing

#this should be added to class
def localData(localDataFileCsv, chosenDataValue):

	csvArray = []

	#get the local PV data
	with open(localDataFileCsv, mode='r') as csvfile:
		localPVData = csv.reader(csvfile)

		for row in localPVData:
		 	csvArray.append(row)

		#print(csvArray)

		#loop through headers to determine position of value needed
		for v in range(len(csvArray[0])):
			if csvArray[0][v] == chosenDataValue:
				return csvArray[-1][v]

#a variation on this was added to the class - replace with that version at some point
def getIPList(deviceListJson, myMACAddr):

	ipList = []

	with open(deviceListJson) as f:
	  data = json.load(f)

	#print(data)

	for i in range(len(data)):
		#filter out local device's mac address
		if str(data[i]['mac']).strip() !=  myMACAddr.strip():
			ipList.append(data[i]['ip'])

	print(ipList)

	return ipList

def runSP():
	print()
	print("*****Running Solar Protocol script*****")
	print()

	#initialize SolarProtocolClass
	SP = SolarProtocolClass()

	#deviceList = "/home/pi/solar-protocol/backend/data/deviceList.json"

	#localDataFile = "/home/pi/solar-protocol/charge-controller/data/tracerData"+ str(datetime.date.today()) +".csv"

	#only log when not in developement mode
	if not DEV:
		logging.basicConfig(filename='/home/pi/solar-protocol/backend/data/poe.log', level=logging.INFO)

	myMAC = SP.getMAC(SP.MACinterface)
	#print("my mac: " + myMAC)

	localPVData = float(localData(localDataFile, dataValue)) * SP.pvWattsScaler()
	outputToConsole("My wattage scaled by " + str(SP.pvWattsScaler()) + ": " + str(localPVData))
	remotePVData = remoteData(getIPList(deviceList, myMAC), apiValue)
	#print("Remote Voltage: " + remotePVData)
	determineServer(remotePVData, localPVData, SP)


def outputToConsole(printThis):
	if consoleOutput:
		print(printThis)

if __name__ == '__main__':
	from SolarProtocolClass import SolarProtocol as SolarProtocolClass	
	runSP()

else:
	consoleOutput = False
	from .SolarProtocolClass import SolarProtocol as SolarProtocolClass


