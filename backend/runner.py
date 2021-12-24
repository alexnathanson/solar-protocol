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

loopFrequency = 15

def runSP():
	print("*****Runner Started!******")
	
	solarProtocol.runSP()

	clientPostIP.runClientPostIP()

	# while True:
	# 	print(datetime.datetime.now().minute)
	# 	if datetime.datetime.now().minute % loopFrequency == 0:
	# 		solarProtocol.runSP()

	# 		clientPostIP.runClientPostIP()

	# 	#sleep for 60 seconds
	# 	time.sleep(60)


if __name__ == '__main__':
	runSP()