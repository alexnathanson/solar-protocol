import requests
import time

dstIP = '192.168.1.180'
url = 'http://'+dstIP+'/api.php'

headers = {
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}

myIP = 	requests.get('http://whatismyip.akamai.com/').text
print(myIP)
#myobj = {'Stamp': time.time(), 'IP': myIP}
myString = "api_key=tPmAT5Ab3j7F9&stamp="+str(time.time())+"&ip="+myIP
print(myString)

x = requests.post(url, headers=headers,data = myString)

print(x.text)