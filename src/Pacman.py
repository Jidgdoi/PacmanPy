# -*- coding:utf-8 -*-

# Cyril Fournier
# 20/01/2016

import os,sys
import wx
import threading
import Queue
import time

import UtilsAndGlobal as UAG
from Cell import Cell
from Map import Map
from UI import UI, UICatcher
from GhostAI import GhostAI
from Graphical import Graphical

from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ===============================
#    ===   Class Pacman   ===
# ===============================

class Pacman():
	"""
	Object representing Pacman.
	"""
	def __init__(self, lives, state, points=0, direction=None):
		self.character = UAG.CellCharacterPacman
		self.ID = UAG.CellCharacterPacman
		self.lives = lives
		self.state = state
		self.points = points
		self.mvt = direction
		self.countdownPower = 0.0

	def __repr__(self):
		return "\033[1;31m[%spts - %s lives]\033[0m" %(self.points, self.lives)

	def setNewDirection(self, direction):
		"""
		Set the new direction of Pacman.
		"""
		self.mvt = direction

	def pickPoint(self):
		self.points += 1

	def pickPower(self):
		self.points += 10
		self.state = UAG.PacmanOverPower
		self.countdownPower = time.time() + UAG.powerTime

	def endPower(self):
		self.state = UAG.PacmanSafe
		self.countdownPower = 0.0

	def killGhost(self):
		self.points += 100

# ===================================
#    ===   Class PacmanGame   ===
# ===================================

class PacmanGame():
	"""
	Main
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, mapFile, dataQueue, threadLock, delay, objUI, objGhostAI, objPacman):
		self.pacman = objPacman
		self.dataQueue = dataQueue
		self.threadLock = threadLock
		self.delay = delay
		self.objMap = Map(mapFile)
		self.objGraphical = Graphical()
		self.objUI = objUI
		self.objGhostAI = objGhostAI
		
		self._addObjCharacterToCells()


	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _addObjCharacterToCells(self):
		"""
		Just after initializing the map, add the obj characters to the corresponding cells.
		"""
		# Add Pacman
		pacmanPos = self.objMap.getPacmanPosition()
		self.objMap.getCell(pacmanPos).addCharacter(self.pacman)
		# Add ghosts
		for g in self.objGhostAI.dGhosts.values():
			ghostPos = self.objMap.getGhostPosition(g.ID)
			self.objMap.getCell(ghostPos).addCharacter(g)

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
		
		# --- If the move is correct
		if self.objMap.isMovePossible(From=pacmanPos, direction=direction):
			nextCell = self.objMap.getCell(nextCellPos)
			# Check for items
			if nextCell.getItem() == UAG.CellItemPoint:
				self.pacman.pickPoint()
				nextCell.deleteItem()
			elif nextCell.getItem() == UAG.CellItemPower:
				self.pacman.pickPower()
				nextCell.deleteItem()
			# Check for ghost:
			for c in nextCell.getCharactersObj():
				if c.state == UAG.GhostAfraid:
					self.pacman.killGhost()
					c.die()
				elif c.state == UAG.GhostAlive:
					self.pacman.getKilled()
					if self.pacman.lives == 0:
						UAG.ExitFlag = 1
						print "You lose."
			# Update Pacman positions
			self.pacman.setNewDirection(direction)
			self.objMap.setPacmanPosition(nextCellPos)
			# Update Cell's characters
			nextCell.addCharacter(self.objMap.getCell(pacmanPos).popCharacter(self.pacman.ID))

	def ghostMovement(self, objGhost):
		"""
		Make all modifications and actions to move the ghosts to their new positions.
		"""
		ghostPos = self.objMap.getGhostPosition(objGhost.ID)
		cellGhost = self.objMap.getCell(ghostPos)
		
		# Define a direction for the ghost
		direction = self.objGhostAI.directionFollowingState(objGhost, cellGhost.getAuthorizedMoves(UAG.CellCharacterGhost))
		
		nextCellPos = self.objMap.getNextCellPos(ghostPos, direction)
		nextCell = self.objMap.getCell(nextCellPos)
		# Check for actions:
		if UAG.CellCharacterPacman in nextCell.getCharactersType(mostImportant=True):
			if objGhost.state == UAG.GhostAfraid:
				self.pacman.killGhost()
				objGhost.die()
			elif objGhost.state == UAG.GhostAlive:
				self.pacman.getKilled()
				if self.pacman.lives == 0:
					UAG.ExitFlag = 1
					print "You lose."
		# Update ghost positions
		objGhost.setNewDirection(direction)
		self.objMap.setGhostPosition(objGhost.ID, nextCellPos)
		# Update Cell's characters
		nextCell.addCharacter(cellGhost.popCharacter(objGhost.ID))

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
			self.pacman.points += 1
			print "Points: %s" %self.pacman.points
		elif action == UAG.ActionPower:
			self.pacman.points += 10
			self.objGhostAI.fearThem()
		elif action == UAG.ActionGhostDie:
			self.query[0].die()
		elif action == UAG.ActionLose:
			UAG.ExitFlag = 1
			print "You lose."


	# ----------------------------------
	# --- RUN
	# ----------------------------------
	def run(self):
		mvt = True
		c = 1
		while not UAG.ExitFlag:
			# Get data from queue
			try:
				query = self.dataQueue.get_nowait()
			except :
				# Queue is empty: Query.Empty() exception but don't work
				query = [None,None]
			# Analyse movement
			if query[1] == None:
				pass
			elif query[1] == "Quit":
				print "\033[1;31m[PacmanGame] Movement is False: ExitFlag\033[0m"
				UAG.ExitFlag = 1
			else:
				self.analyzeQuery(query)
				# Update screen every 4 moves
				if c%4 == 0:
					c = 0
					self.threadLock.acquire()
					# Clear screen
#					print(chr(27) + "[2J")
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
	
	# --- Initiate threads and the wx app
	lock = threading.Lock()
	queue = Queue.Queue(5)
	
	objApp = wx.PySimpleApp()
	objUI = UI(1, "Thread-UI", queue, lock, UAG.PacmanDelay)
	objCatcher = UICatcher(2, "Thread-UICatcher", objApp, objUI)
	objGhostAI = GhostAI(3, "Thread-Ghost", queue, lock, UAG.GhostSpeed)
	
	lThreads = [objUI, objCatcher, objGhostAI]
	
	print "[PacmanGame] Initiate threads"
	for t in lThreads:
		print "\t%s" %t.threadName
		t.start()
	
	# --- Initiate game
	objPacman = Pacman(lives=UAG.Lives, state=UAG.PacmanSafe)
	game = PacmanGame(mapFile, queue, lock, UAG.PacmanDelay, objUI=objUI, objGhostAI=objGhostAI, objPacman=objPacman)
	game.run()
	
	# --- Wait for all threads to terminate before leaving
	print "[PacmanGame] Wait all threads before leaving"
	for t in lThreads:
		print "\t%s" %t.threadName
		t.join()
	
	print "Exit Pacman"

#os.system("gnome-terminal --geometry=60x20+2000+2000")


