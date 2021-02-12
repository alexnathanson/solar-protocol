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

newDSTList = []

myIP = 	requests.get('http://whatismyip.akamai.com/').text

print("MY IP: " + myIP)

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

def getNewDST(responseList):
	#check if is is a new MAC and post if so

	if type(responseList) == list
	#if MAC exists check if it is a new IP and post if so (maybe compare time stamps accounting for time zone)
	for r in responseList:
		#print(r['mac'])

		if r['mac'] not in getKeyList('mac'):
			newDSTList.append(r['ip'])
		elif r['ip'] not in getKeyList('ip'):
			#in the future add in a time stamp heirchy here - taking in to account timezones (or use a 24 hours window)
			newDSTList.append(r['ip'])

def postIt(dstIP,dstData):
	try:
		x = requests.post('http://'+dstIP+'/api/v1/api.php', headers=headers,data = dstData, timeout=5)
		#print("request response!!!")
		#print(x.text)
		#print(x.json())
		if x.ok:
			getNewDST(x.json())
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

def makePosts(ipList):
	
	myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC+"&name="+myName+"&log="+','.join(poeData)

	print(myString)

	#post to self automatically
	postIt(myIP,myString)

	for dst in ipList:
		print("DST: " + dst)

		#post own IP but make sure it is the most recent
		if dst != myIP: #does not work when testing only with local network
			postIt(dst, myString)

#wlan0 might need to be changed to eth0 if using an ethernet cable
myMAC = getmac("wlan0")

myName = getLocalConfig("name")
#myName = myName.lower();#make lower case
myName = re.sub('[^A-Za-z0-9_ ]+', '', myName)#remove all characters not specified

apiKey = getLocalConfig("apiKey")
#apiKey = os.getenv('SP_API_KEY')

getPoeLog()

#writeSelf()

dstList = getKeyList('ip')
makePosts(dstList)
print('new DST list')
print(newDSTList)
makePosts(newDSTList)

