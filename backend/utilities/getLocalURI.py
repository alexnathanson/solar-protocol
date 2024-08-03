# NOT FINISHED OR TESTED YET!!!

# Many LANs have unqiue configurations that mean not every IP or URI is viable.
# This script identifies viable URIs that the server can use to query itself on its LAN

import requests
import ipaddress

toTest = ['localhost']

passed = []

# get public IP and append to URI lists
try:
	# if response >= 400 if fails
	t = requestTest("https://server.solarpowerforartists.com/?myip=true")
	if t != False:
		ipaddress.ip_address(t) #confirm the IP address is valid
		toTest.append(requestTest(t))
except e as Exception:
	print(e)

# get device list IP
try:

# test URIs with variants
for u in toTest:
	for uL in [u, u + ':' + p, u + ':' + pS,'http://' + u,'http://' + u + ':' + p,'https://' + u,'https://' + u + ':' + pS]:
		rT = requestTest(uL)
		if rT != False:
			passed.append(rT)
print(passed)

def requestTest(u):
	try:
		r = request.get(u)
		if r.status_code >= 400:
			print(u + " failed")
			return False
		else:
			print(u + " passed")
			return u
	except e as Exception:
		print(e)
		print(u + " failed")

