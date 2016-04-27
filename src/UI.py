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
			query = [UAG.CellCharacterPacman, self.movement()]
			self.queueLock.acquire()
#			print "[objUI] 2 - Put movement in queue"
			self.queue.put(query)
			self.queueLock.release()
			time.sleep(self.delay)
