#delay the start of the program for 1 minutes, because of an issues with the DNS resolver
if __name__ != '__main__':
	import time
	time.sleep(60)


import runner

print("main!")

runner.runSP()

