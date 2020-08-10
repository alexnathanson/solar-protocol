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
print(myIP)

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

	print(data)

	for i in range(len(data)):
		ipList.append(data[i]['ip'])

	print(ipList)

	return ipList

def makePosts(ipList):
	
	myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC
	print(myString)

	for dst in ipList:

		#if statement only necessary if storing local IP...
		if dst != myIP:
			x = requests.post('http://'+dst+'/api.php', headers=headers,data = myString)
			print(x.text)

myMAC = getmac("wlan0")
dstList = getIPList()
makePosts(dstList)

