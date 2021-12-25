#source: https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9
# This script generates the path from an arbitrary file to another

import os


def realPath(aFile):
	#the full path for this utilities directory that the findPath.py lives in
	utilDirectory = os.path.dirname(__file__)

	#this is the distance from utilDirectory to our root Solar Protocol directory
	rootDirectory = "/../../"
	print(utilDirectory + rootDirectory)

	#this is the full path to a given file
	realPath = os.path.realpath(utilDirectory + rootDirectory + aFile)

	return realPath



if __name__ == "__main__":

    print(realPath("backend/data/deviceList.json"))
