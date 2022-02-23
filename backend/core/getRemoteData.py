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

def run():
	print()
	print("*****Running GET Remote Data script*****")
	print()

	#initialize SolarProtocolClass
	SP = SolarProtocolClass()

	deviceList = "/home/pi/solar-protocol/backend/data/deviceList.json"

	fileDst = "/home/pi/local/data/"

	myMAC = SP.getMAC(SP.MACinterface)

	endPt = '/api/v1/opendata.php?day=4'

	ipList = SP.getDevVal('ip')

	macList = SP.getDevVal('mac')

	for dst, mac in zip(ipList, macList):
		#print(dst)
		handleData(SP.getData("http://" + dst + endPt, True), mac)


def handleData(ccFiles, macAddr):
	#strip headers, combine all 4 files into 1, save file

	combinedFile = []
	for f in ccFiles:
		fHeaders = f[0]

		f = f.pop(0)
		combinedFile.append(f)

	#add headers back in to top
	combinedFile.insert(0, fHeaders)

	with open("/home/pi/local/data/" + macAddr + '.json', 'w', encoding='utf-8') as f:
		json.dump(combinedFile, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
	from SolarProtocolClass import SolarProtocol as SolarProtocolClass	
	run()

else:
	consoleOutput = False
	from .SolarProtocolClass import SolarProtocol as SolarProtocolClass