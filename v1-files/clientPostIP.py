'''
Reads list of destination IPs and posts own IP address to those other devices.
'''
import requests
import time
import json

apiKey='tPmAT5Ab3j7F9'

headers = {
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}

deviceList = "/home/pi/distributed-dynamic-IP-exchanger-API/v1-files/deviceList.json";

myIP = 	requests.get('http://whatismyip.akamai.com/').text

print("MY IP: " + myIP)

myName = 'pi'

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

def makePosts(ipList):
	
	myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC+"&name="+myName
	print(myString)

	for dst in ipList:
		print("DST: " + dst)
		#if statement only necessary if storing local IP... if not storing local IP, must auto Post regulary instead of checking for changes...
		#if dst != myIP: #does not work when testing only with local network
		x = requests.post('http://'+dst+'/api.php', headers=headers,data = myString)
		print(x.text)

#wlan0 might need to be changed to eth0 if using an ethernet cable
myMAC = getmac("wlan0")
dstList = getIPList()
makePosts(dstList)

