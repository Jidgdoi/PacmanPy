# -*- coding:utf-8 -*-

# Cyril Fournier
# 15/01/2016

import os,sys

from UtilsAndGlobal import *

<<<<<<< HEAD
from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ============================
#    ===   Class Cell   ===
# ============================

class Cell():
	"""
	Object representing a cell from the map, containing the cell type.
=======
from Toolbox.MyToolbox import MyToolbox as MTB
from Toolbox.Colors import *

# ===========================
#    ===   Class Cell   ===
# ===========================

class Cell():
	"""
	Object representing a cell from the map, containing the cell type 
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
<<<<<<< HEAD
	def __init__(self, cellType=CellTypePath, item=CellItemNone, character=CellCharacterNone):
		self.type = cellType
		self.item = item
		self.character = character
=======
	def __init__(self, cellType=CellTypePath, item=CellItemNone):
		self.type = cellType
		self.item = item
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
	
	def __repr__(self):
		t, i = MTB.getKey(globals(), [self.type, self.item])
		return "(%s,%s)" %(t, i)
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	def getType(self):
		return self.type
	
	def getItem(self):
		return self.item
	
<<<<<<< HEAD
	def getCharacter(self):
		return self.character
	
	# ----------------------------------
	# --- Set functions
=======
	# ----------------------------------
	# --- Get functions
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
	# ----------------------------------
	def setItem(self, new):
		if self.type != CellTypeWall:
			self.item = new
	
<<<<<<< HEAD
	def setCharacter(self, new):
		if self.type != CellTypeWall:
			self.character = new
	
=======
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def deleteItem(self):
<<<<<<< HEAD
		self.item = CellItemNone
	
	def toPrint(self):
		"""
		Return the principle GLOBAL ID to print (pacman, point, wall ...)
		Character > Item > Cell type
		"""
		if self.character != CellCharacterNone:
			return self.character
		elif self.item != CellItemNone:
			return self.item
		else:
			return self.type
	
	def isMovePossible(self, obj):
		"""
		Return True if the movement for the Pacman or Ghost is possible.
		"""
		if self.type == CellTypeWall: return False
		elif self.type == CellTypeGlass and obj == CellCharacterGhost: return True
		elif self.type == CellTypePath: return True
		return False
=======
		self.item = None
	
	def toPrint(self):
		if self.item != CellItemNone:
			return self.item
		else:
			return self.type
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
