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
		#os.system(subCall + ' ' + dnsKey)
		
		getDNS(requests.get('http://whatismyip.akamai.com/').text)

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

def getEnv(thisEnv):
	#subprocess.Popen('. ./home/pi/solar-protocol/backend/get_env.sh', shell=true)
	proc = subprocess.Popen(['bash','/home/pi/solar-protocol/backend/get_env.sh',thisEnv], stdout=subprocess.PIPE)
	e = proc.stdout.read()
	#convert byte string to string
	e = e.decode("utf-8") 
	#remove line breaks
	e = e.replace("\n", "")
	return e

#this could be greatly simplified in the future...
def getDNS(ip):
	try:
		#returns a single value
		dnsDST = "https://server.solarpowerforartists.com?ip=" + ip + "&key=" + str(getEnv('DNS_KEY'))
		print(dnsDST)
		response = requests.get(dnsDST, timeout = 5)
		print(response.text)		
	except requests.exceptions.HTTPError as err:
		print(err)
	except requests.exceptions.Timeout as err:
		print(err)
	except:
		print(err)

def postDNS(dstIP):

	headers = {
	    #'X-Auth-Key': KEY,
	    'Content-Type': 'application/x-www-form-urlencoded',
	}

	dstData = "ip="+ dstIP +"&key="+str(getEnv('DNS_KEY'))

	try:
		x = requests.post('http://dns.solarprotocol.net/', headers=headers,data = dstData, timeout=5)
		print(x.text)
		#print(x.json())
		if x.ok:
			try:
				print("Post to " + dstIP+ " successful")
			except:
				print(x.text)
		#requests.raise_for_status()
	except json.decoder.JSONDecodeError as e:
		print("JSON decoding error", e)
	except requests.exceptions.HTTPError as errh:
	 	print("An Http Error occurred:" + repr(errh))
	except requests.exceptions.ConnectionError as errc:
		print("An Error Connecting to the API occurred:" + repr(errc))
	except requests.exceptions.Timeout as errt:
	 	print("A Timeout Error occurred:" + repr(errt))
	except requests.exceptions.RequestException as err:
	 	print("An Unknown Error occurred" + repr(err))

subCall += str(getEnv('DNS_KEY'))

#this should be wlan0 even if using ethernet, because its used for identifying hardware regardless of how the connection is made...
myMAC = getmac("wlan0")
#print("my mac: " + myMAC)

localPVData = float(localData()) * SP.pvWattsScaler()
print("My wattage scaled by " + str(SP.pvWattsScaler()) + ": " + str(localPVData))
remotePVData = remoteData(getIPList())
#print("Remote Voltage: " + remotePVData)
determineServer()
