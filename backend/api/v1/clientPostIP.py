'''
Reads list of destination IPs and posts own IP address to those other devices.
'''
import requests
import time
import json
import re

headers = {
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}

deviceList = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";

localConfig = "/home/pi/local/local.json";

poeLog = "/home/pi/solar-protocol/backend/api/v1/poe.log"
poeData = []

myIP = 	requests.get('http://whatismyip.akamai.com/').text

print("MY IP: " + myIP)

#this only works with linux
def getmac(interface):

	try:
		mac = open('/sys/class/net/'+interface+'/address').readline()
	except:
		mac = "00:00:00:00:00:00"

	return mac

def getIPList():

	ipList = []

	with open(deviceList) as f:
	  data = json.load(f)

	#print(data)

	for i in range(len(data)):
		ipList.append(data[i]['ip'])

	#print(ipList)

	return ipList

def getPoeLog():

	try:
		poeFile = open(poeLog)

		poeFileLines = poeFile.readlines()

		#read the most recent 50 lines
		for l in range(100):

			#print(poeFileLines[l])

			#remove "INFO:root:" from the string and strip spaces
			poeData.append(poeFileLines[len(poeFileLines)-l-1][10:-1])

			if l > len(poeFileLines)-1:
				break

		poeFile.close()

	except:
		poeData.append(0)

	#print(poeData)

def getLocalConfig(key):

	#load file
	try:
		#locFile = json.loads(localConfig)
		with open(localConfig) as locFile:
			locData = json.load(locFile)
			print(locData)
			print(locData[key])
			return locData[key]

	except:
		print('local config file exception')
		return 'pi'

def writeSelf():
	#load file
	try:
		
		with open(deviceList) as l:
			devData = json.load(l)

			#print(len(devData))
		
			newMac = True

			for i in range(len(devData)):
				if devData[i]['mac'] == myMAC:
					devData[i]['time stamp'] = str(time.time())
					devData[i]['name'] = myName
					devData[i]['log'] = join(poeData)
					print("updating MAC...")
					print(devData)
					newMac = False

			#write new content if needed
			if newMac == True:
				newDevice={
					"mac":myMAC,
					"time stamp":str(time.time()),
					"name": myName,
					"log":join(poeData)
				}
				print(newDevice)
				# newDevice["mac"] = myMAC				
				# newDevice["time stamp"] = str(time.time())
				# newDevice["name"] = myName
				# newDevice["log"] = join(poeData)

				devData.append(newDevice)
				print("writing new MAC...")
				print(devData)

	except:
		print('write self exception')

def makePosts(ipList):
	
	myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC+"&name="+myName+"&log="+','.join(poeData)

	print(myString)

	for dst in ipList:
		print("DST: " + dst)
		#if statement only necessary if storing local IP... if not storing local IP, must auto Post regulary instead of checking for changes...
		#if dst != myIP: #does not work when testing only with local network
		try:
			x = requests.post('http://'+dst+'/api/v1/api.php', headers=headers,data = myString, timeout=5)
			#print(x.text)
			print("Post successful")
			#requests.raise_for_status()
		except requests.exceptions.HTTPError as errh:
		 	print("An Http Error occurred:" + repr(errh))
		except requests.exceptions.ConnectionError as errc:
			print("An Error Connecting to the API occurred:" + repr(errc))
		except requests.exceptions.Timeout as errt:
		 	print("A Timeout Error occurred:" + repr(errt))
		except requests.exceptions.RequestException as err:
		 	print("An Unknown Error occurred" + repr(err))

#wlan0 might need to be changed to eth0 if using an ethernet cable
myMAC = getmac("wlan0")

myName = getLocalConfig("name")
#myName = myName.lower();#make lower case
myName = re.sub('[^A-Za-z0-9_ ]+', '', myName)#remove all characters not specified


apiKey = getLocalConfig("apiKey")
#apiKey = os.getenv('SP_API_KEY')

getPoeLog()

writeSelf()

dstList = getIPList()
makePosts(dstList)

