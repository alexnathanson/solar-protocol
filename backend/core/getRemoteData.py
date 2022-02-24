'''
Every server runs this script.
This collects the PV data from remote servers via the open data API
The purpose of this is minimize the amount of on the fly API calls.
'''

'''
1) loop through network devices
	2) get most recent 4 files, if call is successful:
		3) strip headers and merge into 1 file organized by time (scale by tz???)
		4) save file
'''

import json

def run():
	print()
	print("*****Running GET Remote Data script*****")
	print()

	#initialize SolarProtocolClass
	SP = SolarProtocolClass()

	# deviceList = "/home/pi/solar-protocol/backend/data/deviceList.json"

	#this is the directory where files are saved to
	fileDst = "/home/pi/local/data/"

	ipList = SP.getDevVal('ip', False)
	nameList = SP.getDevVal('name', False)

	#get local server name
	myMAC = SP.getMAC(SP.MACinterface)
	macList = SP.getDevVal('mac', False)
	myName = ''
	for m in range(len(macList)):
		if myMAC == macList[m]:
			myName = nameList[m]
			break

	endPt = '/api/v1/opendata.php?day=4'

	for dst, name in zip(ipList, nameList):
		print(name + ": " + dst)
		if name == myName:
			dstRes = SP.getRequest("http://localhost" + endPt, True)
		else:
			dstRes = SP.getRequest("http://" + dst + endPt, True)
		print(type(dstRes))

		if isinstance(dstRes, str):
			#remove spaces and make all lower case
			name = name.replace(" ","").lower()

			handleData(dstRes, name)


def handleData(ccFiles, name):
	#strip headers, combine all 4 files into 1, save file

	combinedFile = []

	ccFiles = json.loads(ccFiles)

	for f in ccFiles:

		fHeaders = f[0]
		print(fHeaders)

		print(len(f))
		f.pop(0)
		print(len(f))
		combinedFile.append(f)

	#add headers back in to top
	combinedFile.insert(0, fHeaders)

	with open("/home/pi/local/data/" + name + '.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(combinedFile))
		f.close()

if __name__ == '__main__':
	from SolarProtocolClass import SolarProtocol as SolarProtocolClass	
	run()

else:
	consoleOutput = False
	from .SolarProtocolClass import SolarProtocol as SolarProtocolClass