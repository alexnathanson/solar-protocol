'''
This posts IP address to the other devices
'''
import requests
import time
import json

#dstIP = '192.168.1.180'
url = 'http://'+dstIP+'/api.php'

apiKey='tPmAT5Ab3j7F9'

headers = {
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}

dstList = []
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

	with open('path_to_file/person.json') as f:
	  data = json.load(f)

	print(data)

	for i in range(len(data)):
		dstList.append(data[i]['ip'])

	print(dstList)

getIPList()

myMAC = getmac("wlan0")

myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC
print(myString)

x = requests.post(url, headers=headers,data = myString)

print(x.text)


