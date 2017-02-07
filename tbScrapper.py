#!/usr/bin/python3.5
import urllib2
import time
import argparse
import string
import random
import os
from threading import Thread

t0 = time.time()
#start execution time timer
dataFound = 0
#data found counter

testedCode = []
#list of all the code that have been tested

def getArgs():
	"""
	function to get data from command line
	"""
	parser = argparse.ArgumentParser(description="try to find valid termbin page and download data")
	parser.add_argument("-m", "--maxgrabs",type=int, default=10, help="number of valid url to get, Default: 10")
	parser.add_argument("-f", "--folder",default="./", help="folder to save the data in, default: current folder")
	parser.add_argument("-k", "--keyword", help="only get data that contain this keyword")

	parser.add_argument("-t", "--thread",type=int, default=1, help="number of thread to use. Default: 1")

	args = parser.parse_args()
	
	if int(args.thread) >= int(args.maxgrabs) and args.maxgrabs > 1:
		args.thread = int(args.maxgrabs) - 1
	
	if args.folder[-1:] is not "/":
		args.folder += "/"

	return args

def genCode():
	"""
	function to generate a random 4 char a-z0-9 string
	"""
	charset = string.ascii_lowercase + string.digits
	#gen the charset for the code
	code = "".join(random.choice(charset) for _ in range(4))
	#gen 4 char code

	return code

def testCode(code):
	"""
	function to test if the code have already been tested
	"""
	global testedCode
	#accessing global list of tested code
	
	if not len(testedCode):
		testedCode.append(code)
		return False
	for data in testedCode:
		#browse the list
		if data == code:
		#if code is in list
			return True
		else:
			testedCode.append(code)
			return False

def getUrl(code):
	"""
	function to get the url and data if exist
	"""
	try:
		data = urllib2.urlopen('http://termbin.com/{0}'.format(code))
	except Exception as e:

		if e.getcode() == 404:
			answer = [e.getcode(), "Null"]
		else:
			raise
	else:
		answer = [data.getcode(), data.read()]
	
	return answer

def writeTB(code, data, path):
	"""
	function to write data into a file .tb
	"""

	if not os.path.exists(path):
		os.makedirs(path)

	filename = "{0}{1}.tb".format(path, code)
	
	with open(filename, "w") as theFile:
		theFile.write(data)	
			

def main(args):
	"""
	main function of the program
	"""
	global dataFound
		
	while (dataFound < int(args.maxgrabs)):
		code = genCode()
		if not testCode(code):
			data = getUrl(code)
			print("testing code: {0}".format(code))
			if data[0] == 200:
				
				if args.keyword is None:
					writeTB(code, data[1], args.folder)
					dataFound +=1
				else:
					if args.keyword in data[1]:
						writeTB(code, data[1], args.folder)
						dataFound +=1
def mainThread(args):
	i = 0
	threads = []
	while i < int(args.thread):
		print "thread {0} started".format(i +1)
		t = Thread(target=main, args=(args,))
		threads.append(t)
		i+=1
	for t in threads:
		t.start()

	for t in threads:
		t. join()

if __name__ == '__main__':
	args = getArgs()
	mainThread(args)
	t0 = time.time() - t0

	print("{0} data(s) found in {1} seconds, saved in the folder: {2}".format(dataFound, t0, args.folder))
