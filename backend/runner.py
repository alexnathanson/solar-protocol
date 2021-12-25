'''
This script controls when the other scripts run based on battery status
>90% every 10 minutes
>70% & <= 90% every 15 minutes
>50% & <=70% every 20 minutes
<=50% every 30 minutes
'''
from core import clientPostIP
from core import solarProtocol
from core.SolarProtocolClass import SolarProtocol as SolarProtocolClass
from createHTML import create_html
from createHTML import viz
import datetime
import time
import sys

SP = SolarProtocolClass()

def runSP():
	print("*****Solar Protocol Runner Started******")
	print(sys.argv)

	loopFrequency = setFreq()
	print(loopFrequency)

	while True:

		#pass the argument "now" to run everything once
		if len(sys.argv) > 1:
				if sys.argv[1] == "now":
					scriptsToRun()
					return

		# print(datetime.datetime.now().minute)
		
		if datetime.datetime.now().minute % loopFrequency == 0:

			scriptsToRun()

			loopFrequency = setFreq()
			print(loopFrequency)

		#sleep for 60 seconds
		time.sleep(60)

def scriptsToRun():

	try:
		clientPostIP.runClientPostIP()
	except Exception as err:
		printLoud("clientPostIP.py Exception", err)

	try:
		solarProtocol.runSP()
	except Exception as err:
		printLoud("solarProtocol.py Exception", err)

	try:
		viz.main()
	except Exception as err:
		printLoud("viz Exception", err)

	try:
		create_html.main()
	except Exception as err:
		printLoud("create_html Exception", err)

def printLoud(mess, e):
	print()
	print("!!!!! " + mess + " !!!!!")
	print(e)
	print()

def setFreq():
	#print("setting frequency")
	
	try:
		bP =float(SP.getRequest("http://localhost/api/v1/chargecontroller.php?value=battery-percentage", True))

		if bP > .9:
			lF = 10
		elif bP > .7:
			lF = 15
		elif bP > .5:
			lF = 20
		else:
			lF = 30
	except:
	 	lF = 20

	return lF

if __name__ == '__main__':
	runSP()