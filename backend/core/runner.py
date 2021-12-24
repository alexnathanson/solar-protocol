'''
This script controls when the other scripts run based on battery status
>90% every 10 minutes
>70% & <= 90% every 15 minutes
>50% & <=70% every 20 minutes
<=50% every 30 minutes
'''


def runSP():
	print("SP Runner Started!")

	#initialize SolarProtocolClass
	SP = SolarProtocolClass()

	solarProtocol.runSP()

if __name__ == '__main__':
	import clientPostIP
	import solarProtocol
	from SolarProtocolClass import SolarProtocol as SolarProtocolClass
	runSP()
else:
	from core import clientPostIP
	from core import solarProtocol
	from core.SolarProtocolClass import SolarProtocol as SolarProtocolClass