#delay the start of the program for 1 minutes, because of an issues with the DNS resolver
if __name__ != '__main__':
	import time
	print("sleeping!")
	time.sleep(120)


import runner

print("main!")

runner.runSP()

