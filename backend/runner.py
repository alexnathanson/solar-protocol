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

loopFrequency = 10

def runSP():
	print("*****Runner Started!******")
	
	# logging.basicConfig(filename='/home/pi/solar-protocol/backend/data/runner.log', encoding='utf-8', level=logging.INFO)

	# solarProtocol.runSP()

	# clientPostIP.runClientPostIP()
	SP = SolarProtocolClass()

	batPercentage =	SP.getRequest("http://localhost/api/v1/?value=battery-percentage", True)

	print(batPercentage)
	print(type(batPercentage))
	print(type(int(batPercentage)))
	# while True:

	# 	print(datetime.datetime.now().minute)
		
	# 	if datetime.datetime.now().minute % loopFrequency == 0:

	# 		#log when the script triggers
	# 		# logging.info(datetime.datetime.now())

	# 		clientPostIP.runClientPostIP()

	# 		solarProtocol.runSP()

	# 		SP.getRequest("http://localhost/api/v1/", True)

	# 	#sleep for 60 seconds
	# 	time.sleep(60)


if __name__ == '__main__':
	runSP()