'''
Every server runs this script.
This script retreives live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) and updates the DNS system.
Otherwise, the script changes nothing.
'''

import requests
import os
import subprocess
import fileinput
import json
import datetime
#import time
import csv
import logging
from SolarProtocolClass import SolarProtocol

#terminal command to update DNS record
subCall = 'sudo sh /home/pi/solar-protocol/backend/update_ip2.sh '
dnsKey = ''

'''
possible values (use "-" instead of spaces):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
'''

dataValue = 'PV power L'
# apiValue = 'PV-voltage'
apiValue = 'scaled-wattage'

deviceList = "/home/pi/solar-protocol/backend/api/v1/deviceList.json"

localDataFile = "/home/pi/solar-protocol/charge-controller/data/tracerData"+ str(datetime.date.today()) +".csv"

logging.basicConfig(filename='/home/pi/solar-protocol/backend/api/v1/poe.log', level=logging.INFO)

#initialize SolarProtocolClass
SP = SolarProtocol()

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

	# print("ALL DATA:")
	# print(allData)

	return allData
	#determineServer(allData)

def determineServer():

	thisServer = True

	#print(remotePVData)

	#loop through data from all servers and compare scaled wattage
	for s in remotePVData:
		if s > localPVData:
			thisServer = False

	if thisServer:
		print('Point of entry')

		logging.info(datetime.datetime.now())

		#comment back in to run
		os.system(subCall + ' ' + dnsKey)
	else:
		print('Not point of entry')
		#logging.info(datetime.datetime.now())#comment this out after testing

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

def getIPList(devicesListJson, myMACAddr):

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

#this only works with linux
def getmac(interface):

	try:
		mac = open('/sys/class/net/'+interface+'/address').readline()
	except:
		mac = "00:00:00:00:00:00"

	return mac

def getEnv(thisEnv):
	#subprocess.Popen('. ./home/pi/solar-protocol/backend/get_env.sh', shell=true)
	proc = subprocess.Popen(['bash','/home/pi/solar-protocol/backend/get_env.sh',thisEnv], stdout=subprocess.PIPE)
	e = proc.stdout.read()
	#convert byte string to string
	e = e.decode("utf-8") 
	#remove line breaks
	e = e.replace("\n", "")
	return e

subCall += str(getEnv('DNS_KEY'))

#this should be wlan0 even if using ethernet, because its used for identifying hardware regardless of how the connection is made...
myMAC = getmac("wlan0")
#print("my mac: " + myMAC)

localPVData = float(localData(localDataFile, dataValue)) * SP.pvWattsScaler()
print("My wattage scaled by " + str(SP.pvWattsScaler()) + ": " + str(localPVData))
remotePVData = remoteData(getIPList(devicesList, myMAC))
#print("Remote Voltage: " + remotePVData)
determineServer()
