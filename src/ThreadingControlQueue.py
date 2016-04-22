# -*- coding:utf-8 -*-

# Cyril Fournier
# 22/04/2016

import os,sys
import threading
import time
import Queue

from UtilsAndGlobal import *

from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# =================================
#    ===   Class Threading   ===
# =================================

class ThreadControl(threading.Thread):
	"""
	Object controlling the threads release and lock etc.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, threadID, name, delay, queue):
		# Init thread module in this class
		threading.Thread.__init__(self)
		
		self.threadID = threadID
		self.name = name
		self.delay = delay
		self.queue = queue
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def run(self):
		print "Starting thread: %s" %self.name
		while not exitFlag:
			data = ""
			# --- Lock the queue for yourself
			queueLock.acquire()
			if not self.queue.empty():
				# Pick the data in the queue
				data = self.queue.get()
			# Then unlock the queue: others threads will have access again to the queue
			queueLock.release()
			
			# --- Treat data
			if not data:
				continue
			elif data == "Bread":
				self.process_bread(data)
			elif data == "Tomato":
				self.process_tomato(data)
			elif data == "Letuce":
				self.process_letuce(data)
			else:
				self.process_others(data)
			# Sleep for a time
			time.sleep(self.delay)
		print "Exiting thread: %s" %self.name
	
	def process_bread(self, data):
		print "\033[1;3%sm%s\033[0m is processing '\033[1;33m%s\033[0m'" %(self.threadID, self.name, data)
	
	def process_tomato(self, data):
		print "\033[1;3%sm%s\033[0m is processing '\033[1;31m%s\033[0m'" %(self.threadID, self.name, data)
	
	def process_letuce(self, data):
		print "\033[1;3%sm%s\033[0m is processing '\033[1;32m%s\033[0m'" %(self.threadID, self.name, data)
	
	def process_others(self, data):
		print "\033[1;3%sm%s\033[0m is processing '\033[1;34m%s\033[0m'" %(self.threadID, self.name, data)


if __name__=='__main__':
	# exitFlag will set to 1 when we'll want to terminates threads.
	exitFlag = 0
	
	# Create the 'Locker' for all threads in the queue
	queueLock = threading.Lock()
	# Create the working queue, with a maximum size (maximum number of threads)
	workQueue = Queue.Queue(-1)
	
	# === Create new threads
	lThreads = list()
	for i in range(1,6):
		thread = ThreadControl(threadID=i, name="Thread-%s" %i, delay=i, queue=workQueue)
		thread.start()
		lThreads.append(thread)
	
	# === Fill the queue with data
	lData = ["Bread","Cheese","Letuce","Tomato","Steak","Steak","Sauce","Bread"]*2
	queueLock.acquire()
	for i in lData:
		workQueue.put(i)
	print "*** All ingredients have been put in the machine's queue."
	queueLock.release()
	
	# === Wait queue to be empty
	while not workQueue.empty():
		pass
	print "*** Burger is ready."
	
	# Queue is now empty (no more data in it): notify threads it's time to terminates
	exitFlag = 1
	
	# Wait for all threads to terminate before leaving
	for t in lThreads:
		t.join()
	
	print "Exiting Main"
