# -*- coding:utf-8 -*-

# Cyril Fournier
# 19/01/2016

import random
import threading
import Queue
import time

import UtilsAndGlobal as UAG

# ==============================
#    ===   Class Ghost   ===
# ==============================

class Ghost():
	"""
	Object representing a ghost.
	"""
	def __init__(self, ID, state, color=''):
		self.character = UAG.CellCharacterGhost
		self.ID = ID
		self.state = state
		self.color = color or "\033[1;3%sm" %random.choice([1,2,4,7])
		self.mvt = UAG.MovementUp
		self.countdownFear = 0.0

	def __repr__(self):
		return "%s%s\033[0m: %s" %(self.color, self.ID, "Alive" if self.state == 1 else "Afraid" if self.state == 2 else "Dead")

	def setNewDirection(self, direction):
		"""
		Set new direction for the ghost.
		"""
		self.mvt = direction

	def booh(self):
		"""
		Change ghost's state to GhostAfraid and make him turn back.
		"""
		if self.state == UAG.GhostAlive:
			self.state = UAG.GhostAfraid
			# Turn back
			if self.mvt == UAG.MovementUp: self.mvt = UAG.MovementDown
			elif self.mvt == UAG.MovementDown: self.mvt = UAG.MovementUp
			elif self.mvt == UAG.MovementRight: self.mvt = UAG.MovementLeft
			else: self.mvt = UAG.MovementRight
			# Start FearTime countdown
			self.countdownFear = time.time() + UAG.FearTime
		else:
			print "The ghost %s is not alive, he can't be afraid." %self.ID

	def notAfraidAnymoreBitch(self):
		"""
		Ghost is not afraid anymore.
		"""
		if self.state == UAG.GhostAfraid:
			self.state = UAG.GhostAlive
			self.countdownFear = 0.0
		else: print "The ghost %s is not afraid, he cann't be not afraid anymore." %self.ID

	def die(self):
		"""
		Change ghost's state to GhostDead.
		"""
		if self.state == UAG.GhostAfraid:
			self.state = UAG.GhostDead
			self.countdownFear = 0.0
		else: print "The ghost %s is not afraid, he can't die." %self.ID

	def resurect(self):
		"""
		Change ghost's state to GhostAlive and make him turn back.
		"""
		if self.state != UAG.GhostAlive:
			self.state = UAG.GhostAlive
			# Turn back
			if self.mvt == UAG.MovementUp: self.mvt = UAG.MovementDown
			elif self.mvt == UAG.MovementDown: self.mvt = UAG.MovementUp
			elif self.mvt == UAG.MovementRight: self.mvt = UAG.MovementLeft
			else: self.mvt = UAG.MovementRight
		else:
			print "The ghost %s is not dead or afraid, he can't resurect." %self.ID

	def respawn(self):
		"""
		Re-initialize ghost.
		"""
		self.state = UAG.GhostAlive
		self.countdownFear = 0.0
		self.mvt = UAG.MovementUp

# ===============================
#    ===   Class GhostAI   ===
# ===============================

class GhostAI(threading.Thread):
	"""
	Object controlling the Artificial Intelligence of Ghosts.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, threadID, threadName, queue, queueLock, speed, nbGhost):
		# Init thread module in this class
		threading.Thread.__init__(self)
		
		self.threadID = threadID
		self.threadName = threadName
		self.queue = queue
		self.queueLock = queueLock
		self.speed = speed
		self.dAuthorizedMoves = {UAG.MovementUp:[UAG.MovementUp, UAG.MovementRight, UAG.MovementLeft],
		                         UAG.MovementDown:[UAG.MovementDown, UAG.MovementRight, UAG.MovementLeft],
		                         UAG.MovementRight:[UAG.MovementRight, UAG.MovementUp, UAG.MovementDown],
		                         UAG.MovementLeft:[UAG.MovementLeft, UAG.MovementUp, UAG.MovementDown]}
		
		self.dGhosts = self._initGhost(nbGhost)

	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _initGhost(self, n):
		"""
		Initiate Ghosts objects.
		"""
		return {i:Ghost(i, 1, "\033[5;3%sm" %i) for i in range(n)}

	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	def fearThem(self):
		"""
		The Pacman took a power, set all ghosts states to GhostAfraid.
		"""
		for g in self.dGhosts.values(): g.booh()

	# ----------------------------------
	# --- Move functions
	# ----------------------------------
	def randomMove(self, direction, lCellAuthorizedMoves):
		"""
		Return the new direction for a ghost.
		'direction': current ghost direction
		'lCellAuthorizedMoves': list of authorized moves from the current cell
		"""
		lDirection = list( set(self.dAuthorizedMoves[direction]) & set(lCellAuthorizedMoves) )
		# If it's a dead-end, go back
		if lDirection: return random.choice(lDirection)
		else: return lCellAuthorizedMoves[0]

	def predatorMove(self, direction, lCellAuthorizedMoves, lCellPacmanDistance):
		"""
		Return the new direction for a ghost, which is predating the Pacman.
		'direction': current ghost direction
		'lCellAuthorizedMoves': list of authorized moves from the current cell
		'lCellPacmanDistance': list of distance of cell's neighbors.
		"""
		predatorDirection = min(lCellPacmanDistance, key=lambda x: x[0])
		# Return predator move
		if predatorDirection[0] <= UAG.GhostSmell:
			return predatorDirection[1]
		# Return random move
		return self.randomMove(direction, lCellAuthorizedMoves)

	# ----------------------------------
	# --- Run
	# ----------------------------------
	def run(self):
		while not UAG.ExitFlag:
#			print "[GhostAI] 1 - Ghosts ask to move"
			self.queueLock.acquire()
			for g in self.dGhosts.values():
				query = [UAG.CellCharacterGhost, g]
#				print "[GhostAI] 2 - Ghost %s put movement in queue" %g.ID
				self.queue.put(query)
			self.queueLock.release()
			time.sleep(self.speed)

