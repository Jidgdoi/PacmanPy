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
		
		# If the move was correct
		action = False
		if self.objMap.isMovePossible(From=pacmanPos, direction=direction):
			# Get action
			action = self.objMap.moveAction(Who=UAG.CellCharacterPacman, To=nextCellPos)
			# Make Pacman move by updating objMap
			self.objMap.makeMove(From=pacmanPos, To=nextCellPos, Action=action)
		
		return action

	def ghostMovement(self, objGhost):
		"""
		Make all modifications and actions to move the ghosts to their new positions.
		"""
		ghostPos = self.objMap.getGhostPosition(objGhost.ID)
		cellGhost = self.objMap.getCell(ghostPos)
		print objGhost
		# Define a direction for the ghost
		if objGhost.state == UAG.GhostAlive:
			direction = self.objGhostAI.randomMove(objGhost.mvt, cellGhost.getAuthorizedMoves(UAG.CellCharacterGhost))
		elif objGhost.state == UAG.GhostAfraid:
			direction = self.objGhostAI.randomMove(objGhost.mvt, cellGhost.getAuthorizedMoves(UAG.CellCharacterGhost))
		else:
			direction = self.objGhostAI.shortestPathTo(ghostPos)
		
		# Make the ghost move, update objMap and objGhost direction
		nextCellPos = self.objMap.getNextCellPos(ghostPos, direction)
		action = self.objMap.moveAction(Who=UAG.CellCharacterGhost, To=nextCellPos)
		# Update cells
		self.objMap.makeMove(From=ghostPos, To=nextCellPos, Action=action, GhostID=objGhost.ID)
		objGhost.setNewDirection(direction)
		
		return action

	def analyzeQuery(self, query):
		"""
		Answer to the query.
		"""
		if query[0] == UAG.CellCharacterPacman:
			action = self.pacmanMovement(query[1])
		elif query[0] == UAG.CellCharacterGhost:
			action = self.ghostMovement(query[1])
		else:
			pass
		# Update Game informations
		if action == UAG.ActionPoint:
			self.points += 1
			print "Points: %s" %self.points
		elif action == UAG.ActionPower:
			self.points += 10
			self.objGhostAI.fearThem()
		elif action == UAG.ActionDie:
			UAG.ExitFlag = 1
			print "You lose."


	# ----------------------------------
	# --- RUN
	# ----------------------------------
	def run(self):
		mvt = True
		c = 1
		while not UAG.ExitFlag:
			# Catch movement
#			print "[Pacman] 1 - Get data from queue."
			try:
				query = self.dataQueue.get_nowait()
			except :
#				print "[Pacman] Queue.Empty()"
				query = [None,None]
#			query = self.dataQueue.get()
#			print "[Pacman] 2 - Get data from queue."
			# Analyse movement
			if query[1] == False:
				print "\033[1;31m[Pacman] Movement is False: ExitFlag\033[0m"
				UAG.ExitFlag = 1
			elif query[1] == None:
				pass
#				print "Query None"
#				time.sleep(self.delay)
			else:
				self.analyzeQuery(query)
				# Update screen every 4 moves
				if c%4 == 0:
					c = 0
					self.threadLock.acquire()
					print(chr(27) + "[2J")
#					os.system('clear')
					print self.objMap
					self.threadLock.release()
				c += 1
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
	queue = Queue.Queue(5)
	
	dThreads = {"Thread-UI":UI(1, "Thread-UI", queue, lock, UAG.PacmanDelay),
	            "Thread-Ghost":GhostAI(2, "Thread-Ghost", queue, lock, UAG.GhostSpeed)}
	print "[Pacman] Initiate threads"
	for t in dThreads:
		print "\t%s" %dThreads[t].name
		dThreads[t].start()
	
	# --- Initiate game
	game = Pacman(mapFile, queue, lock, UAG.PacmanDelay, objUI=dThreads["Thread-UI"], objGhostAI=dThreads["Thread-Ghost"])
	game.run()
	
	# --- Wait for all threads to terminate before leaving
	print "[Pacman] Wait all threads before leaving"
	for t in dThreads:
		print "\t%s" %dThreads[t].name
		dThreads[t].join()
	
	print "Exiting Pacman"

#os.system("gnome-terminal --geometry=60x20+2000+2000")


