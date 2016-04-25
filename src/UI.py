# -*- coding:utf-8 -*-

# Cyril Fournier
# 19/01/2016

import sys
import tty,termios # for getch
import threading
import time
import Queue

import UtilsAndGlobal as UAG

# ===========================
#    ===   Class UI   ===
# ===========================

class UI(threading.Thread):
	"""
	Object controlling the interaction with the user: User Interface.
	This class use one thread.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, threadID, name, queue, queueLock, delay):
		# Init thread module in this class
		threading.Thread.__init__(self)
		
		self.threadID = threadID
		self.name = name
		self.queue = queue
		self.queueLock = queueLock
		self.delay = delay
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _getch(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(3)
		except KeyboardInterrupt: 
			ch = False
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
	
	def _getch2(self):
		"""Waits for a single keypress on stdin.

		This is a silly function to call if you need to do it a lot because it has
		to store stdin's current setup, setup stdin for reading single keystrokes
		then read the single keystroke then revert stdin back after reading the
		keystroke.

		Returns the character of the key that was pressed (zero on
		KeyboardInterrupt which can happen when a signal gets handled)

		"""
		import termios, fcntl, sys, os
		fd = sys.stdin.fileno()
		# save old state
		flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
		attrs_save = termios.tcgetattr(fd)
		# make raw - the way to do this comes from the termios(3) man page.
		attrs = list(attrs_save) # copy the stored version to update
		# iflag
		attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
				      | termios.ISTRIP | termios.INLCR | termios. IGNCR 
				      | termios.ICRNL | termios.IXON )
		# oflag
		attrs[1] &= ~termios.OPOST
		# cflag
		attrs[2] &= ~(termios.CSIZE | termios. PARENB)
		attrs[2] |= termios.CS8
		# lflag
		attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
				      | termios.ISIG | termios.IEXTEN)
		termios.tcsetattr(fd, termios.TCSANOW, attrs)
		# turn off non-blocking
		fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
		# read a single keystroke
		try:
			ret = sys.stdin.read(3) # returns a single character
		except KeyboardInterrupt: 
			ret = 0
		finally:
			# restore old state
			termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
			fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
		return ret

	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def movement(self):
		"""
		Check if the movement is valid (key pressed is ok).
		"""
		key = self._getch()
		print "[UI] Key: %s" %key
		if   key == '\x1b[A': return UAG.MovementUp
		elif key == '\x1b[B': return UAG.MovementDown
		elif key == '\x1b[C': return UAG.MovementRight
		elif key == '\x1b[D': return UAG.MovementLeft
		return False
	
	def run(self):
		mvt = True
		while mvt and not UAG.ExitFlag:
#			print "[objUI] 1 - Waiting movement"
			mvt = self.movement()
			self.queueLock.acquire()
#			print "[objUI] 2 - Put movement in queue"
			self.queue.put(mvt)
			self.queueLock.release()
			time.sleep(self.delay)
#			try:
#				self.queue.put_nowait(mvt)
#			except Queue.Full():
#				print "[objUI] Fail to add movement to queue: queue Full."
#				pass
