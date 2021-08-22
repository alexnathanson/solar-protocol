print('solar protocol class in attendence')

class SolarProtocol:
	def _init_(self, localConfig):
		self.localConfig = "/home/pi/local/local.json"

	def getLocalConfig(key):
		#load file
		try:
			#locFile = json.loads(localConfig)
			with open(self.localConfig) as locFile:
				locData = json.load(locFile)
				#print(locData)
				#print(locData[key])
				return locData[key]
		except:
			print('local config file exception')

			if key == 'name':
				return 'pi'
			elif key == 'httpPort':
				return ''