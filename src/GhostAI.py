# -*- coding:utf-8 -*-

# Cyril Fournier
# 19/01/2016

import os,sys
import random

from UtilsAndGlobal import *

from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ===============================
#    ===   Class GhostAI   ===
# ===============================

class GhostAI():
	"""
	Object controlling the Artificial Intelligence of Ghosts.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, ID=GhostIDRed):
		self.ID = ID
		self.mvt = MovementUp
		self.dAuthorizedMoves = {MovementUp:[MovementUp, MovementRight, MovementLeft],
		                         MovementDown:[MovementDown, MovementRight, MovementLeft],
		                         MovementRight:[MovementRight, MovementUp, MovementDown],
		                         MovementLeft:[MovementLeft, MovementUp, MovementDown]}
	
	def __repr__(self):
		return "Ghost %s" %self.ID
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	def getID(self):
		return self.ID
	
	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	
	def randomMove(self):
		"""
		Return the next move of the ghost.
		"""
		return random.choice(self.dAuthorizedMoves[self.mvt])
	
	def shortestPathTo(self, target):
		"""
		Return the shortest path (list of movement) to the target.
		"""
		return
