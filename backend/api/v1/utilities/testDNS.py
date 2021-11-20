'''
Run this script to test that the DNS can be properly pointed to the server.
'''

from SolarProtocolClass import SolarProtocol

dnsKey = ''

#initialize SolarProtocolClass
SP = SolarProtocol()

def testDNS():

	print('Testing point of entry')
	
	SP.getRequest(SP.updateDNS(SP.myIP,str(SP.getEnv('DNS_KEY'))))

testDNS()