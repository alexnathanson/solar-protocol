"""
A script to test API GET requests
Arguments

clientGet-example.py ip key value
"""

import requests, sys

[ip, key, value] = sys.argv

print (ip, key, value)

url = ""

"""Value
possible values (use - instead of space):
PV current,PV power H,PV power L,PV voltage,
battery percentage,battery voltage,charge current,
charge power H,charge power L,date,load current,load power,load voltage,time
"""

url = f"http://{ip}/api/charge-controller"
params = { key: value }

response = requests.get(url=url, params=params).text
print(response)
