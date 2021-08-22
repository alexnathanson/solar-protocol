print('solar protocol class in attendence')

# currently this class only handles some new functionality for solarProtocol.py.
# Refactoring is required to create additional methods and apply this to clientPostIP.py too

class SolarProtocol:
	def _init_(self):
		self.localConfigFile = "/home/pi/local/local.json"
		self.localConfigData
		self.loadLocalConfigFile()

	#load in data from config file
	def loadLocalConfigFile(self):
		print('loading config file...')
		#load file
		try:
			with open(self.localConfigFile) as locFile:
				self.localConfigData = json.load(locFile)
				print(self.localConfigData)
				print('local config data loaded')
		except:
			print('local config file exception')

	#returns a specific piece of local config data
	def getLocalConfig(self, key):
		#load file
		try:
			return self.localConfigData[key]
		except:
			print('local config file exception')

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
	def moduleScaler(self):
		try:
			return 50.0 / self.localConfigData['pvWatts']
		except:
			return 1

	# Returns the scaled wattaged
	def scaledPvWatts(self):
		try:
			return self.localConfigData['pvWatts'] * self.moduleScaler()
		except:
			return 50