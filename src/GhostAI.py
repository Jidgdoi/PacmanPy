# -*- coding:utf-8 -*-

# Cyril Fournier
# 19/01/2016

import random
import threading
import Queue
import time

import UtilsAndGlobal as UAG

from Utility.MyToolbox import MyToolbox as MTB

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
		if self.state == GhostAlive:
			self.state = GhostAfraid
			# Turn back
			if self.mvt == UAG.MovementUp: self.mvt = UAG.MovementDown
			elif self.mvt == UAG.MovementDown: self.mvt = UAG.MovementUp
			elif self.mvt == UAG.MovementRight: self.mvt = UAG.MovementLeft
			else: self.mvt = UAG.MovementRight
		else:
			print "The ghost %s is not alive, he can't be afraid." %self.ID

	def die(self):
		"""
		Change ghost's state to GhostDead.
		"""
		if self.state == UAG.GhostAfraid: self.state = UAG.GhostDead
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
	def __init__(self, threadID, threadName, queue, queueLock, speed):
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
		
		self.dGhosts = self._initGhost(4)

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
		for g in self.dGhosts.values: g.booh()

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

	def shortestPathTo(self, target):
		"""
		Return the shortest path (list of movement) to the target.
		"""
		return

	def directionFollowingState(self, ghost, lCellAuthorizedMoves):
		"""
		Return the new direction for a ghost following his state.
		"""
		if ghost.state == UAG.GhostAlive:
			return self.randomMove(ghost.mvt, lCellAuthorizedMoves)
		elif ghost.state == UAG.GhostAfraid:
			return self.randomMove(ghost.mvt, lCellAuthorizedMoves)
		else:
			return self.objGhostAI.shortestPathTo(ghostPos)

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

