import requests
import time

dstIP = '192.168.1.180'
url = 'https://'+dstIP+'/postIP.php'


headers = {
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}

myIP = 	requests.get('http://whatismyip.akamai.com/').text

#myobj = {'Stamp': time.time(), 'IP': myIP}
myString = "api_key=tPmAT5Ab3j7F9&stamp="+str(time.time())+"&ip="+myIP

x = requests.post(url, data = myString)

print(x.text)