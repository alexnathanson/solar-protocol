import requests

dstIP = '192.168.1.180'

url = 'http://'+dstIP+'/api.php'

PVdata = 	requests.get(url).text
print(PVdata)