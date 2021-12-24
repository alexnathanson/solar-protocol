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
import datetime
import time
# import logging

def runSP():
	print("*****Runner Started!******")
	
	# logging.basicConfig(filename='/home/pi/solar-protocol/backend/data/runner.log', encoding='utf-8', level=logging.INFO)

	SP = SolarProtocolClass()

	loopFrequency = setFreq()

	while True:

		print(datetime.datetime.now().minute)
		
		if datetime.datetime.now().minute % loopFrequency == 0:

			#log when the script triggers
			# logging.info(datetime.datetime.now())

			clientPostIP.runClientPostIP()

			solarProtocol.runSP()

			SP.getRequest("http://localhost/api/v1/", True)

			loopFrequency = setFreq()
		#sleep for 60 seconds
		time.sleep(60)


def setFreq():
	print("setting frequency")
	
	try:
		bP =float(SP.getRequest("http://localhost/api/v1/chargecontroller.php?value=battery-percentage", True))

		print(type(bP))

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