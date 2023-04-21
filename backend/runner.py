'''
This script controls when the other scripts run based on battery status and solar power
>90% every 10 minutes
>70% & <= 90% every 15 minutes
>50% & <=70% every 20 minutes
>30% every 30 minutes
<= 30% every 60 minutes

pass the argument "now" to run everything immediately - otherwise sleep for 60 seconds before starting

If solar power production is 0 times are doubled.
If battery percentage is below 30, viz script doesn't run

'''
from core import clientPostIP
from core import solarProtocol
from core import getRemoteData
from core.SolarProtocolClass import SolarProtocol as SolarProtocolClass
from createHTML import create_html
from createHTML import viz
from createHTML import create_sunthinking
import datetime
import time
import sys
import logging
from math import trunc
import subprocess

SP = SolarProtocolClass()

def runSP():
	print("***** Solar Protocol Runner Started ******")
	#print(sys.argv)

	loopFrequency = setFreq()
	print("Loop frequency: " + str(loopFrequency) + " minutes")
	sScaler = solarScaler()

	timeOfRun = datetime.datetime.now()

	runCount = 1

	#pass the argument "now" to run everything immediately - otherwise sleep for 60 seconds before starting
	if len(sys.argv) > 1:
			if sys.argv[1] == "now":
				print("Running now")
	else:
		time.sleep(60)
	
	scriptsToRun(1, runCount)

	while True:

		# print(datetime.datetime.now().minute)
		
		if getElapsedTime(timeOfRun) % (loopFrequency * sScaler) == 0:

			timeOfRun = datetime.datetime.now()

			if loopFrequency == 60:
				sM = 0
			else:
				sM = 1

			runCount = runCount + 1

			scriptsToRun(sM, runCount)

			loopFrequency = setFreq()
			print("Loop frequency: " + str(loopFrequency) + " minutes")

			sScaler = solarScaler()

		#sleep for 60 seconds
		time.sleep(60)

def scriptsToRun(sMode,rC):

	print("Run number " + str(rC) + " at " + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

	runReport = "Exceptions: "

	try:
		clientPostIP.runClientPostIP()
	except Exception as err:
		printLoud("clientPostIP.py Exception", err)
		runReport = runReport + "clientPostIP "

	try:
		solarProtocol.runSP()
	except Exception as err:
		printLoud("solarProtocol.py Exception", err)
		runReport = runReport + "solarProtocol "

	try:
		getRemoteData.run()
	except Exception as err:
		printLoud("getRemoteData.py Exception", err)
		runReport = runReport + "getRemoteData "


	# when viz isn't run in subprocess it gets an index out of range error
	# I believe happens in the enumerate(ccData) loop but I don't know why
	try:
		subprocess.run(["python3", "/home/pi/solar-protocol/backend/createHTML/viz.py"])
	except Exception as err:
		printLoud("viz Exception", err)
		runReport = runReport + "viz "	

	try:
		create_html.main()
	except Exception as err:
		printLoud("create_html Exception", err)
		runReport = runReport + "create_html "

	try:
		create_sunthinking.main()
	except Exception as err:
		printLoud("create_sunthinking Exception", err)
		runReport = runReport + "create_sunthinking "


	print()
	print("Completed run " + str(rC) + " at " + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

	if runReport != "Exceptions: ":
		print(runReport)
	else:
		print(runReport + '0, all good')

	print()

def printLoud(mess, e):
	print()
	print("!!!!! " + mess + " !!!!!")
	print(e)
	print()

def getElapsedTime(oldTime):
	'''
		returns elapsed time since oldTime was set
	'''
	el = datetime.datetime.now() - oldTime
	elMin = trunc(el.seconds / 60)
	return elMin

def setFreq():
	'''
		Set how frequent the script should run various functions
	'''

	#print("setting frequency")
	
	#battery percentage
	try:
		bP =float(SP.getRequest("http://localhost/api/v2/opendata.php?value=battery-percentage", True))

		if bP > .9:
			lF = 10
		elif bP > .7:
			lF = 15
		elif bP > .5:
			lF = 20
		elif bP > .3:
			lF = 30
		else:
			lF = 60
	except:
	 	lF = 20

	return lF

def solarScaler():
	'''
	solar power multiplier
	above 6 w it runs at the normal pace (the max power draw is about 5w)
	between 0 and 6 w it scales between the normal pace and 2x slower
	if 0w (i.e. no sun) the frequency slows down by 2
	'''
	try:
		sP =float(SP.getRequest("http://localhost/api/v2/opendata.php?value=scaled-wattage", True))

		if sP >= 6.0:
			sM = 1
		elif sP > 0.0:
			sM = 1 + (1 - (sP /5.0))
		elif sP == 0.0:
			sM = 2
	except:
	 	sM = 1

	return sM

if __name__ == '__main__':
	print("running runner.py as __main__")
	runSP()