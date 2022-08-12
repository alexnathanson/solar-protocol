'''
Every server runs this script.
Reads list of destination IPs and posts own IP address to those other devices.
'''

#these modules are only used by this module within this packages
#all other modules are imported via __init__
import re
from threading import local
import time
import requests
import json
import subprocess
import os
import sys

consoleOutput = True

headers = {
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}

if os.environ.get("ENV") == "DEV" or 'DEV' in sys.argv:
	print("Dev mode")
	dataRoot = "../../dev-data/"
	deviceList = dataRoot + "deviceList.json"
	localConfig = dataRoot + "local.json"
	poeLog = dataRoot + "poe.log"
	envVar = "this-will-fail" #sys.argv[2]
	DEV = True
else:
	deviceList = "/home/pi/solar-protocol/backend/data/deviceList.json"
	localConfig = "/home/pi/local/local.json"
	poeLog = "/home/pi/solar-protocol/backend/data/poe.log"
	DEV = False

newDSTList = []
runningDSTList = []

#this only works with linux
def getmac(interface):

	try:
		mac = open('/sys/class/net/'+interface+'/address').readline()
	except:
		mac = "00:00:00:00:00:00"

	return mac

def getKeyList(getKey):

	ipList = []

	with open(deviceList) as f:
	  data = json.load(f)

	#print(data)

	for i in range(len(data)):
		ipList.append(data[i][getKey])

	return ipList

def getPoeLog():
	poeData = []

	try:
		poeFile = open(poeLog)

		poeFileLines = poeFile.readlines()

		#read the most recent 216 lines
		#if it runs solarProtocol.py every 10 minutes it could have up to 432 entries per 72 hours (if it was the POE every time)
		for l in range(216):

			#print(poeFileLines[l])

			#remove "INFO:root:" from the string and strip spaces
			poeData.append(poeFileLines[len(poeFileLines)-l-1][10:-1])

			if l > len(poeFileLines)-1:
				break

		poeFile.close()

	except:
		poeData.append(0)

	return poeData

def getLocalConfig(key):

	#load file
	try:
		#locFile = json.loads(localConfig)
		with open(localConfig) as locFile:
			locData = json.load(locFile)
			#print(locData)
			#print(locData[key])
			return locData[key]

	except:
		print('local config file exception with key ' + key)

		if key == 'name':
			return 'pi'
		elif key == 'httpPort':
			return ''

def getNewDST(responseList):
	global newDSTList, runningDSTList
	#check if is is a new MAC and post if so
	#if type(responseList) == list:
	#if MAC exists check if it is a new IP and post if so (maybe compare time stamps accounting for time zone)
	for r in responseList:
		#print(r['mac'])

		if r['mac'] not in getKeyList('mac'):
			if r['ip'] not in runningDSTList:
				outputToConsole("new ip: " + r['ip'])
				newDSTList.append(r['ip'])
				runningDSTList.append(r['ip'])
		elif r['ip'] not in getKeyList('ip'):
			#in the future add in a time stamp heirchy here - taking in to account timezones (or use a 24 hours window)
			if r['ip'] not in runningDSTList:
				outputToConsole("new ip: " + r['ip'])
				newDSTList.append(r['ip'])
				runningDSTList.append(r['ip'])

def postIt(dstIP,dstData):
	try:
		x = requests.post('http://'+dstIP+'/api/v1/api.php', headers=headers,data = dstData, timeout=5)
		#print("request response!!!")
		#print(x.text)
		#print(x.json())
		if x.ok:
			try:
				getNewDST(x.json())
				print("Post to " + dstIP+ " successful")
			except:
				print("Malformatted response from " + dstIP + ":")
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

#add a boolean back in if the 
def makePosts(ipList, api_Key, my_IP, my_Name, my_MAC, my_TZ):

	poeData = getPoeLog()

	global newDSTList

	newDSTList = []
	#all content that the server is posting. API key, timestamp for time of moment, extrenal ip, mac address, name, timezone, poe log
	myString = "api_key="+str(api_Key)+"&stamp="+str(time.time())+"&ip="+my_IP+"&mac="+my_MAC+"&name="+my_Name+"&tz=" + my_TZ +"&log="+','.join(str(pD) for pD in poeData)

	print(myString)

	#post to self automatically
	postIt('localhost', myString)

	#post to solarprotocol.net
	postIt('solarprotocol.net', myString)

	for dst in ipList:
		print("DST: " + dst)

		#postTrue
		if dst != my_IP: #does not work when testing only with local network
			postIt(dst, myString)

	if len(newDSTList) > 0:
		outputToConsole("New DST list:")
		outputToConsole(newDSTList)
		makePosts(newDSTList, api_Key, my_IP, my_Name, my_MAC, my_TZ)

def getEnv(thisEnv):
	if not DEV:
		#subprocess.Popen('. ./home/pi/solar-protocol/backend/get_env.sh', shell=true)
		proc = subprocess.Popen(['bash','/home/pi/solar-protocol/backend/get_env.sh',thisEnv], stdout=subprocess.PIPE)
		e = proc.stdout.read()
		#convert byte string to string
		e = e.decode("utf-8") 
		#remove line breaks
		e = e.replace("\n", "")
		return e
	else:
		return envVar

def addPort(thisPort):
	p = getLocalConfig(thisPort)
	outputToConsole(p)
	if p != "":
		return ":" + p
	else: 
		return ""

def runClientPostIP():
	print()
	print("*****Running ClientPostIP script*****")
	print()
	
	myIP = 	requests.get('https://server.solarpowerforartists.com/?myip').text
	print("MY IP: " + myIP)

	#wlan0 might need to be changed to eth0 if using an ethernet cable
	myMAC = getmac("wlan0")

	myName = getLocalConfig("name")
	#myName = myName.lower();#make lower case
	myName = re.sub('[^A-Za-z0-9_ ]+', '', myName)#remove all characters not specified

	myIP += addPort("httpPort") 

	#apiKey = getLocalConfig("apiKey") #not in use
	# apiKey = getEnv("API_KEY")

	#writeSelf()

	#get my timezone
	tz_url = "http://localhost" + addPort("httpPort") + "/api/v1/opendata.php?systemInfo=tz"
	myTZ = requests.get(tz_url).text

	dstList = getKeyList('ip')
	makePosts(dstList,getEnv("API_KEY"), myIP, myName, myMAC, myTZ)


def outputToConsole(printThis):
	if consoleOutput:
		print(printThis)

if __name__ == '__main__':
	runClientPostIP()

else:
	consoleOutput = False