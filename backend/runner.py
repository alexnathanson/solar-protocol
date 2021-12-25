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

	loopFrequency = setFreq()


	while True:

		#pass the argument "now" to run everything once
		if len(sys.argv) > 0:
				if sys.argv[0] == "now":
					scriptsToRun()
					return

		# print(datetime.datetime.now().minute)
		
		if datetime.datetime.now().minute % loopFrequency == 0:

			scriptsToRun()

			loopFrequency = setFreq()

		#sleep for 60 seconds
		time.sleep(60)

def scriptsToRun():

	clientPostIP.runClientPostIP()
	solarProtocol.runSP()
	viz.main()
	create_html.main()

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
			lF = 10
	except:
	 	lF = 30

	return lF

if __name__ == '__main__':
	runSP()