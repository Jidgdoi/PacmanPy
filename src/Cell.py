# -*- coding:utf-8 -*-

# Cyril Fournier
# 15/01/2016

import os,sys

from UtilsAndGlobal import *

from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ============================
#    ===   Class Cell   ===
# ============================

class Cell():
	"""
	Object representing a cell from the map, containing the cell type.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, cellType=CellTypePath, item=CellItemNone, character=CellCharacterNone):
		self.type = cellType
		self.item = item
		self.character = character
	
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
	
	def getCharacter(self):
		return self.character
	
	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	def setItem(self, new):
		if self.type != CellTypeWall:
			self.item = new
	
	def setCharacter(self, new):
		if self.type != CellTypeWall:
			self.character = new
	
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def deleteItem(self):
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
