# -*- coding:utf-8 -*-

# Cyril Fournier
# 20/01/2016

import os,sys
import wx
import threading
import Queue
import time

#from UtilsAndGlobal import *
import UtilsAndGlobal as UAG
from Cell import Cell
from Map import Map
from UI import UI
from GhostAI import GhostAI
from Graphical import Graphical

from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ===============================
#    ===   Class Pacman   ===
# ===============================

class Pacman():
	"""
	Main
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, mapFile, dataQueue, threadLock, delay, objUI, objGhostAI):
		self.dataQueue = dataQueue
		self.threadLock = threadLock
		self.delay = delay
		self.objMap = Map(mapFile)
		self.objGraphical = Graphical()
		self.objUI = objUI
		self.objGhostAI = objGhostAI
		self.points = 0

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
	def pacmanMovement(self, direction):
		"""
		Make all modifications and actions to move Pacman to his new position.
		"""
		# --- Get both Pacman and his next cell positions
		pacmanPos = self.objMap.getPacmanPosition()
		nextCellPos = self.objMap.getNextCellPos(pacmanPos, direction)
		print "Size map: %s, %s" %(self.objMap.size[0], self.objMap.size[1])
		print "Postion: %s\tNext: %s" %(pacmanPos, nextCellPos)
		
		# If the move was correct
		if self.objMap.isMovePossible(From=pacmanPos, move=direction):
			action = self.objMap.moveAction(From=pacmanPos, To=nextCellPos)
			self.objMap.makeMove(From=pacmanPos, To=nextCellPos, action=action)
			if action in [UAG.ActionPoint, UAG.ActionPower]: self.points += 1
			#TODO
			# Following the action, add a point, give power and die: update Graphical interface
	
	def ghostMovement(self):
		"""
		Make all modifications and actions to move the ghosts to their new positions.
		"""
		



	# ----------------------------------
	# --- RUN
	# ----------------------------------
	def run(self):
		mvt = True
		while not UAG.ExitFlag:
			# Catch movement
#			print "[Pacman] 1 - Get data from queue."
			try:
				mvt = self.dataQueue.get_nowait()
			except :
#				print "[Pacman] Queue.Empty()"
				mvt = None
#			mvt = self.dataQueue.get()
#			print "[Pacman] 2 - Get data from queue."
			# Analyse movement
			if mvt == False:
#				print "[Pacman] Movement is False: ExitFlag"
				UAG.ExitFlag = 1
			elif mvt == None:
				time.sleep(self.delay)
			else:
#				print(chr(27) + "[2J")
				os.system('clear')
				print "Movement: %s" %mvt
				print "Points: %s" %self.points
				self.pacmanMovement(mvt)
				print self.objMap
		return

if __name__=='__main__':
	print "="*23
	print "Welcome".center(23)
	print "To the PacmanPy game !".center(23)
	print "="*23
	
	# --- Get map file
	rootDir = os.sep.join(os.path.realpath(sys.argv[0]).split(os.sep)[:-2])
	if len(sys.argv) == 2: mapFile = sys.argv[1]
	else: mapFile = "%s%s%s" %(rootDir, os.sep, "data/defaultPacmanMap.map")
	
	# --- Initiate threads
	lock = threading.Lock()
	queue = Queue.Queue(1)
	delay = 0.05
	ghostSpeed = 1.0
	
	dThreads = {"Thread-UI":UI(1, "Thread-UI", queue, lock, delay),
	            "Thread-Ghost":GhostAI(2, "Thread-Ghost", ghostSpeed)}
	print "[Pacman] Initiate threads"
	for t in dThreads:
		print "\t%s" %dThreads[t].name
		dThreads[t].start()
	
	# --- Initiate game
	game = Pacman(mapFile, queue, lock, delay, objUI=dThreads["Thread-UI"], objGhostAI=dThreads["Thread-Ghost"])
	game.run()
	
	# --- Wait for all threads to terminate before leaving
	print "[Pacman] Wait all threads before leaving"
	for t in dThreads:
		print "\t%s" %dThreads[t].name
		dThreads[t].join()
	
	print "Exiting Pacman"

