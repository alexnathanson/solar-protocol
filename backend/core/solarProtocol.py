'''
Every server runs this script.
This script retreives live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) and updates the DNS system.
Otherwise, the script changes nothing.
'''
import os
import fileinput
import datetime
import csv
import logging
import requests
import json
import sys

DEV = 'DEV' in sys.argv

if DEV:
	localDataFile = f'/home/pi/solar-protocol/dev/data/tracerDataTest.csv'
else:
	localDataFile = f'/home/pi/solar-protocol/charge-controller/data/tracerData{str(datetime.date.today())}.csv'

'''
apiValue is what we use to determine who should be the point of entry

possible apiValues:

PV-current
PV-power-H
PV-power-L
PV-voltage
battery-percentage
battery-voltage
charge-current
charge-power-H
charge-power-L
date
load-current
load-power
load-voltage
time
scaled-wattage
'''
apiValue = 'scaled-wattage'

# return data from a particular server
# maybe this should be moved into the class
def getData(host, chosenApiValue):
	try:
		# returns a single value
		url = f'http://{host}/api/v1/chargecontroller.php?value={chosenApiValue}'
		response = requests.get(url, timeout = 5)
		# check if the response can be converted to a float
		return float(response.text)
	except requests.exceptions.HTTPError as err:
		print(err)
		return -1
	except requests.exceptions.Timeout as err:
		print(err)
		return -1
	except:
		return -1

'''
If this server has the highest value, update DNS to be point of entry
'''
def determineServer(apiValues, myValue, SP):
    if myValue > max(apiValues):
		print('Point of entry')

		logging.info(datetime.datetime.now())
		
		# Do not update DNS if running in DEV
        key = 'this-will-fail' if DEV else str(SP.getEnv('DNS_KEY'))
        url = SP.updateDNS(SP.myIP, key)
        print(SP.getRequest(url))
	else:
		print('Not point of entry')

def runSP():
	print()
	print("***** Running Solar Protocol script *****")
	print()

	SP = SolarProtocolClass()

    logging.basicConfig(filename='/home/pi/solar-protocol/backend/data/poe.log', level=logging.INFO)

    # get all ips, mac addresses, and apiValues for devices in the device list
    ips = SP.getDeviceValues('ip')
    macs = SP.getDeviceValues('macs')
	apiValues = [getValue(ip, apiValue) for ip in ips]

    # If we are in the device list, check if we should update the point of entry
	myMAC = SP.getMAC(SP.MACinterface)
    if myMAC in macs:
      myValue = apiValues[macs.index(myMAC)]
      determineServer(apiValues, myValue, SP)

if __name__ == '__main__':
	from SolarProtocolClass import SolarProtocol as SolarProtocolClass	
	runSP()
else:
	from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
