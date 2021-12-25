#source: https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9
# This script generates the path from an arbitrary file to another

import os

#pass in the path to the file from the SP root directory.
#For example, to get the full path to the deviceList.json file use "backend/data/deviceList.json"

def fullPath(aFile):
	#the full path for this utilities directory that the findPath.py lives in
	utilDirectory = os.path.dirname(__file__)

	#this is the distance from utilDirectory to our root Solar Protocol directory
	rootDirectory = "/../../"
	print(utilDirectory + rootDirectory)

	#this is the full path to a given file
	fP = os.path.realpath(utilDirectory + rootDirectory + aFile)

	return fP



if __name__ == "__main__":

    print(fullPath("backend/data/deviceList.json"))
