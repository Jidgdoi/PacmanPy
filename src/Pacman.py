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

from Colors import *


##########################################
# TODO: Pause when lose a life
# TODO: PacmanTracking functionality --> ghost can track Pacman when he's near them.
#		or create a new "power" which instead of afraid ghosts, enraged them and track Pacman.
# TODO: Begin graphical interface with wxPython
##########################################

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

	def __repr__(self):
		return "\033[1;31m[%spts - %s lives]\033[0m" %(self.points, self.lives)

	def setNewDirection(self, direction):
		"""
		Set the new direction of Pacman.
		"""
		self.mvt = direction

	def pickPointReward(self):
		self.points += UAG.PointReward

	def pickPowerReward(self):
		self.points += UAG.PowerReward

	def killGhostReward(self):
		self.points += UAG.KillReward

	def getKilled(self):
		self.lives -= 1
		if self.lives == 0: return True
		return False

	def getLifeBonus(self):
		self.lives += 1

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
	def __init__(self, objMap, dataQueue, threadLock, delay, objUI, objGhostAI):
		self.dataQueue = dataQueue
		self.threadLock = threadLock
		self.delay = delay
		self.objMap = objMap
		self.pacman = Pacman(lives=self.objMap.playerLives, points=self.objMap.playerPoints, state=UAG.PacmanSafe)
		self.objGraphical = Graphical()
		self.objUI = objUI
		self.objGhostAI = objGhostAI
		self.eventText = ''
		self.countdownEventText = 0.0
		
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
	# --- Graphic functions
	# ----------------------------------
	def clearScreen(self):
		print(chr(27) + "[2J")
#		os.system('clear')

	def printEvent(self, txt=''):
		"""
		Print the last event for 3 secondes.
		"""
		if txt:
			self.eventText = txt
			self.countdownEventText = time.time() + UAG.EventTextTime
		
		if self.countdownEventText:
			if time.time() < self.countdownEventText:
				print self.eventText
			else:
				self.countdownEventText = 0.0

	# ----------------------------------
	# --- Game functions
	# ----------------------------------
	def pacmanGetKilled(self):
		"""
		Pacman lose a life. Every characters spawn to their respawn.
		"""
		print "\033[1;31mA ghost killed you: you lose a life.\033[0m"
		if self.pacman.getKilled():
			# Game end
			UAG.ExitFlag = 1
			return UAG.ActionLose
		else:
			# --- Ghosts
			for i in self.objGhostAI.dGhosts.keys():
				# Cell character
				self.objMap.getCell(self.objMap.dGhostSpawns[i]).addCharacter(self.objMap.getCell(self.objMap.dGhostPositions[i]).popCharacter(i))
				# Map position
				self.objMap.dGhostPositions[i] = self.objMap.dGhostSpawns[i]
				# Ghost state
				self.objGhostAI.dGhosts[i].respawn()
			# --- Pacman
			# Cell character
			self.objMap.getCell(self.objMap.pacmanSpawn).addCharacter(self.objMap.getCell(self.objMap.pacmanPosition).popCharacter(self.pacman.ID))
			# Map position
			self.objMap.pacmanPosition = self.objMap.pacmanSpawn
			
			# Free DataQueue
			self.threadLock.acquire()
			while not self.dataQueue.empty():
				self.dataQueue.get()
			self.threadLock.release()
			return UAG.ActionLoseLife

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
		# --- Check action
		if not action: return ''
		elif action == UAG.ActionPower: return UAG.Plus10Points
		elif action == UAG.ActionGhostDie: return UAG.Plus100Points
		elif action == UAG.ActionLoseLife: return UAG.GhostKilledYou
		elif action == UAG.ActionGetLife: return UAG.Plus1LifeBonus
		elif action == UAG.ActionLose: return UAG.GameOver
		elif action == UAG.ActionWin: return UAG.GameWin

	def checkCountdowns(self):
		"""
		Check ghosts' fear countdown.
		"""
		# Ghost fear countdown
		for g in self.objGhostAI.dGhosts.values():
			if g.countdownFear:
				if time.time() > g.countdownFear:
					g.notAfraidAnymoreBitch()

	# ----------------------------------
	# --- Movement functions
	# ----------------------------------
	def pacmanMovement(self, direction):
		"""
		Make all modifications and actions to move Pacman to his new position.
		"""
		action = False
		# --- Get both Pacman and his next cell positions
		pacmanPos = self.objMap.getPacmanPosition()
		nextCell = self.objMap.getNextCell(pacmanPos, direction, False)
		
		# --- If the move is correct
		if self.objMap.isMovePossible(From=pacmanPos, direction=direction):
			# Check for items
			if nextCell.getItem() == UAG.CellItemPoint:
				nextCell.deleteItem()
				self.pacman.pickPointReward()
				if self.objMap.updatePointsLeft():
					UAG.ExitFlag = 1
					return UAG.ActionWin
				if (self.pacman.points%UAG.LifeBonusThresh - UAG.PointReward) < 0:
					self.pacman.getLifeBonus()
					action = UAG.ActionGetLife
			elif nextCell.getItem() == UAG.CellItemPower:
				nextCell.deleteItem()
				self.pacman.pickPowerReward()
				self.objGhostAI.fearThem()
				action = UAG.ActionPower
				if (self.pacman.points%UAG.LifeBonusThresh - UAG.PowerReward) < 0:
					self.pacman.getLifeBonus()
					action = UAG.ActionGetLife
			# Check for ghost:
			for c in nextCell.getCharactersObj().values():
				if c.state == UAG.GhostAfraid:
					c.die()
					self.pacman.killGhostReward()
					action = UAG.ActionGhostDie
					if (self.pacman.points%UAG.LifeBonusThresh - UAG.KillReward) < 0:
						self.pacman.getLifeBonus()
						action = UAG.ActionGetLife
				elif c.state == UAG.GhostAlive:
					return self.pacmanGetKilled()
			# Update Pacman positions
			self.pacman.setNewDirection(direction)
			self.objMap.setPacmanPosition(nextCell.pos)
			self.objMap.updateCellsPacmanDistance()
			# Update Cell's characters
			nextCell.addCharacter(self.objMap.getCell(pacmanPos).popCharacter(self.pacman.ID))
		return action

	def ghostMovement(self, objGhost):
		"""
		Make all modifications and actions to move the ghosts to their new positions.
		"""
		action = False
		ghostPos = self.objMap.getGhostPosition(objGhost.ID)
		cellGhost = self.objMap.getCell(ghostPos)
		
		# Define a direction for the ghost
		if objGhost.state != UAG.GhostDead:
			if UAG.GhostPredator:
				direction = self.objGhostAI.predatorMove(objGhost.mvt,
														 cellGhost.getAuthorizedMoves(UAG.CellCharacterGhost),
														 self.objMap.getNeighborsPacmanDist(cellGhost))
			else:
				direction = self.objGhostAI.randomMove(objGhost.mvt,
													   cellGhost.getAuthorizedMoves(UAG.CellCharacterGhost))
		else:
			direction = cellGhost.getGSpawnDirection(objGhost.ID)
		
		nextCell = self.objMap.getNextCell(ghostPos, direction, False)
		# Check for actions:
		if UAG.CellCharacterPacman in nextCell.getCharactersType(mostImportant=True):
			if objGhost.state == UAG.GhostAfraid:
				objGhost.die()
				self.pacman.killGhostReward()
				action = UAG.ActionGhostDie
				if (self.pacman.points%UAG.LifeBonusThresh - UAG.KillReward) < 0:
					self.pacman.getLifeBonus()
					action = UAG.ActionGetLife
			elif objGhost.state == UAG.GhostAlive:
				return self.pacmanGetKilled()
		# Check for ghost resurection
		if nextCell.pos == self.objMap.dGhostSpawns[objGhost.ID]:
			objGhost.resurect()
		
		# Update ghost positions
		objGhost.setNewDirection(direction)
		self.objMap.setGhostPosition(objGhost.ID, nextCell.pos)
		# Update Cell's characters
		nextCell.addCharacter(cellGhost.popCharacter(objGhost.ID))
		return action

	# ----------------------------------
	# --- RUN
	# ----------------------------------
	def run(self):
		mvt = True
		c = 1
		while not UAG.ExitFlag:
			# --- Get data from queue
			try:
				query = self.dataQueue.get_nowait()
			except :
				# Queue is empty: Query.Empty() exception but don't work
				continue
			# --- Analyze event
			if query[1] == "Quit":
				print "\033[1;31m[PacmanGame] Movement is False: ExitFlag\033[0m"
				UAG.ExitFlag = 1
			elif query[1] == "Save":
				fileName = "%s%ssave%ssave_%s.map" %(rootDir, os.sep, os.sep, time.strftime("%A_%d_%B-%Hh%Mm%S"))
				print "\033[1;33m[PacmanGame] Save game to %s\033[0m" %fileName
				self.objMap.writePacmanMap(fileName, self.pacman.points, self.pacman.lives)
			else:
				if c%4 == 0 or query[0] == UAG.CellCharacterPacman:
					self.clearScreen()
				eventText = self.analyzeQuery(query)
				# Update screen every 4 moves
				if c%4 == 0 or query[0] == UAG.CellCharacterPacman or eventText:
					c = 0
#					self.threadLock.acquire()
					self.printEvent(eventText)
					self.objMap.printMap(self.pacman.points, self.pacman.lives)
					if eventText == UAG.GhostKilledYou: time.sleep(UAG.EventTextTime)
#					self.threadLock.release()
				c += 1
			
			# --- Treat other game parameters independant from movement
			self.checkCountdowns()
		return
