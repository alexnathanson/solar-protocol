import json

print('solar protocol class in attendence')

# currently this class only handles some new functionality for solarProtocol.py.
# Refactoring is required to create additional methods and apply this to clientPostIP.py too

class SolarProtocol:
	def __init__(self):
		self.localConfigFile = "/home/pi/local/local.json"
		self.localConfigData = dict()
		self.loadLocalConfigFile()

	#load in data from config file
	def loadLocalConfigFile(self):
		print('loading config file')
		#load file
		try:
			with open(self.localConfigFile) as locFile:
				locData = json.load(locFile)
				print('local config data loaded 1')
				for key, value in locData:
				    # do something with value
				    self.localConfigData[key] = value
				print('local config data loaded 2')
		except:
			print('loadLocalConfigFile error')

	#returns a specific piece of local config data
	def getLocalConfig(self, key):
		#load file
		try:
			return self.localConfigData[key]
		except:
			print('getLocalConfig error')

			if key == 'name':
				return 'pi'
			elif key == 'httpPort':
				#should this return 80 as a default?
				return ''

	'''
	Returns the scaling factor for the module based on a standard of 50 watts
	(i.e. if a server is using a 100 watt module, it must be divided by 2,
	and if it is using a 25 watt module it must by multiplied by 2)
	In the future a more complex method that takes in to account I-V curves may need to be applied
	'''
	def pvWattsScaler(self):
		try:
			return 50.0 / self.localConfigData['pvWatts']
		except:
			return 1