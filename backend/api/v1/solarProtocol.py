'''
Every server runs this script.
This script retreives live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) and updates the DNS system.
Otherwise, the script changes nothing.
'''

import requests
import os
import fileinput
import json
import datetime
import csv
import logging
from SolarProtocolClass import SolarProtocol

dnsKey = ''
#constants

apiPVCurrent         = 'PV-current'
apiPVPowerH          = 'PV-power-H'
apiPVPowerL          = 'PV-power-L'
apiPVVoltage         = 'PV-voltage'
apiBatteryPercentage = 'battery-percentage'
apiBatteryVoltage    = 'battery-volage'
apiChargeCurrent     = 'charge-current'
apiChargePowerH      = 'charge-power-H'
apiChargePowerL      = 'charge-power-L'
apiDate              = 'date'
apiLoadCurrent       = 'load-current'
apiLoadPower         = 'load-power'
apiLoadVoltage       = 'load-voltage'
apiTime              = 'time'
apiScaledWattage     = 'scaled-wattage'

apiToCsv = {
    apiPVCurrent: 'PV current',
    apiPVPowerH: 'PV power H',
    apiPVPowerL: 'PV power L',
    apiVoltage: 'PV voltage',
    apiBatteryPercentage: 'battery percentage',
    apiBatteryVoltage: 'battery voltage',
    apiChargeCurrent: 'charge current',
    apiChargePowerH: 'charge power H',
    apiChargePowerL: 'charge power L',
    apiDate: 'date',
    apiLoadCurrent: 'load current',
    apiLoadPower: 'load power',
    apiLoadVoltage: 'load voltage',
    apiTime: 'time',
    apiScaledWattage: 'PV power L'
}

#this is the key to retrieve from remote devices
apiValue = apiScaledWattage
#this is the value to be retrieved locally (and then scaled). It could potentially be retrieved via an API call to itself, which might make code cleaner
dataValue = apiToCsv[apiValue]

deviceList = "/home/pi/solar-protocol/backend/api/v1/deviceList.json"

localDataFile = "/home/pi/solar-protocol/charge-controller/data/tracerData"+ str(datetime.date.today()) +".csv"

logging.basicConfig(filename='/home/pi/solar-protocol/backend/api/v1/poe.log', level=logging.INFO)

#initialize SolarProtocolClass
SP = SolarProtocol()

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

def determineServer(remoteData,localData):

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

		#getDNS(requests.get('http://whatismyip.akamai.com/').text)
		SP.getRequest(SP.updateDNS(SP.myIP,str(SP.getEnv('DNS_KEY'))))

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

#this should be added to class
def getIPList(deviceListJson, myMACAddr):

	ipList = []

	with open(deviceListJson) as f:
	  data = json.load(f)

	#print(data)

	for i in range(len(data)):
		#filter out local device's mac address
		if str(data[i]['mac']).strip() !=  myMACAddr.strip():
			ipList.append(data[i]['ip'])

	#print(ipList)

	return ipList

myMAC = SP.getMAC(SP.MACinterface)
#print("my mac: " + myMAC)

localPVData = float(localData(localDataFile, dataValue)) * SP.pvWattsScaler()
print("My wattage scaled by " + str(SP.pvWattsScaler()) + ": " + str(localPVData))
remotePVData = remoteData(getIPList(deviceList, myMAC), apiValue)
#print("Remote Voltage: " + remotePVData)
determineServer(remotePVData, localPVData)
