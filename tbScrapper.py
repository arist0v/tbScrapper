#!/usr/bin/python3.5
import urllib2
from datetime import datetime
import argparse
import string
import random
import os
from threading import Thread
from Queue import Queue
from time import sleep
import sys
import re

#version 0.2
def getArgs():
	"""
	function to get data from command line
	"""
	parser = argparse.ArgumentParser(description="try to find valid termbin page and download data")
	parser.add_argument("-m", "--maxgrabs",type=int, default=10, help="number of valid url to get, Default: 10")
	parser.add_argument("-f", "--folder",default="./", help="folder to save the data in, default: current folder")
	parser.add_argument("-k", "--keyword", help="only get data that contain this keyword can't be use with regex")
	
	parser.add_argument("-r", "--regex", help="get data that contain this regex can't be use with keyword")

	parser.add_argument("-t", "--thread",type=int, default=1, help="number of thread to use. Default: 1")

	args = parser.parse_args()
	
	if args.keyword and args.regex:
		#test if both keyword and regex are selected
		print("Error: You can't user keyword and regex at the same time.\n\n")
		parser.print_help()
		sys.exit(1)

	if args.folder[-1:] is not "/":
		#test if folder end with / if not add it
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
		#if no code have been tested yet
		testedCode.append(code)
		#add code to list of tested code
		return False

	for data in testedCode:
		#browse the list
		if data == code:
		#if code is in list
			return True
		else:
			testedCode.append(code)
			#add code to list
			return False

def getUrl(code):
	"""
	function to get the url and data if exist
	"""
	try:
		data = urllib2.urlopen('http://termbin.com/{0}'.format(code))
		#try to open the termbin url
	except Exception as e:
		#if got an exception
		if e.getcode() == 404:
			#if it's 404
			answer = [e.getcode(), "Null"]
			#return 404
		else:
			raise
			
	else:
		answer = [data.getcode(), data.read()]
		#if we get valid data, return the http code and data

	return answer

def writeTB(code, data, path):
	"""
	function to write data into a file .tb
	"""

	if not os.path.exists(path):
		#if don't exist create folder
		os.makedirs(path)

	filename = "{0}{1}.tb".format(path, code)
	#create filename with folder and code.tb
	
	with open(filename, "w") as theFile:
		theFile.write(data)
		#save data to file

def main(args, q):
	"""
	main function of the program
	"""
	global dataFound
		
	while (dataFound < int(args.maxgrabs)) and len(testedCode) < 1679616 :
		#until we get the number of grabs or we have tested all code
		
		code = q.get()
		#get a code from queue
		
		if not testCode(code):
			#if we haven't tested it yet
			data = getUrl(code)
			#get data
			
			print("testing code: {0}".format(code))
			#test the code

			if data[0] == 200:
				#if we got http 200
				if args.keyword is None and args.regex is None:
					#if we don't want specific keyword
					writeTB(code, data[1], args.folder)
					#write data to file
					dataFound +=1
				elif args.keyword:
					if args.keyword in data[1]:
						#if keyword is find in data
						writeTB(code, data[1], args.folder)
						#write data to file
						dataFound +=1
				elif args.regex:
					if re.search(args.regex, data[1]):
						#if regex found in data
						writeTB(code, data[1], args.folder)
						#write data to file
						dataFound +=1
		q.task_done()
	print("exited")

def mainThread(args, q):
	i = 0
	threads = []

	while i < int(args.thread):
		#until we didn'T get the number of thread requested
		print "thread {0} started".format(i +1)
		t = Thread(target=main, args=(args, q))
		#create thread
		threads.append(t)
		#add thread to list
		i+=1

	for t in threads:
		#start all thread
		t.start()

	for t in threads:
		#look all thread to wait until all finished
		t. join()

def code2Queue(q, args):
	"""
	function to fill queue with code
	"""
	global dataFound
	
	while dataFound < args.maxgrabs:
		#until we don'T have found the # of data wanted
		while not q.full():
			#until queue is not full
			code = genCode()
			#get a code
			q.put(code)
			#add it to the queue
	
if __name__ == '__main__':
	t0 = datetime.now()
	#start execution timer
	dataFound= 0
	testedCode= []

	args = getArgs()
	#get args from command line
	
	q = Queue(5)
	#create empty queue

	codeThread = Thread(target=code2Queue, args=(q,args))
	codeThread.start()
	#start the code generation thread

	mainThread(args, q)
	#start threading
	t0 = datetime.now() - t0
	#stop timer

	print("{0} data(s) found in {1} , saved in the folder: {2}".format(dataFound, t0, args.folder))
