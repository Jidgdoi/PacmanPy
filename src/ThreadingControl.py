# -*- coding:utf-8 -*-

# Cyril Fournier
# 22/04/2016

import os,sys
import threading
import time

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
	def __init__(self, threadID, name, counter, delay):
		# Init thread module in this class
		threading.Thread.__init__(self)
		
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.delay = delay
	
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
		# Get lock to synchronize threads
		# During a lock, other threads can't operate
		threadLock.acquire()
		self.print_time()
		# Free lock to release next thread
		threadLock.release()
		print "Exiting thread: %s" %self.name
	
	def print_time(self):
		while self.counter:
			time.sleep(self.delay)
			print "%s: %s" %(self.name, time.ctime())
			self.counter -= 1


if __name__=='__main__':
	# Create the 'Locker' for all threads
	threadLock = threading.Lock()
	
	# Create new threads
	thread1 = ThreadControl(1, "Thread-1", 3, 1)
	thread2 = ThreadControl(2, "Thread-2", 4, 2)
	
	# Start threads
	thread1.start()
	thread2.start()
	
	# Join threads to wait until the thread terminates
	thread1.join(1.0)
	thread2.join()
	
	print thread1.isAlive()
	print "Exiting Main"
