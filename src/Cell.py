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
		self.lAuthorizedMoves = []
	
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
	
	def getAuthorizedMoves(self):
		return self.lAuthorizedMoves
	
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
	
	def updateAuthorizedMoves(self, cellUpType, cellDownType, cellRightType, cellLeftType):
		"""
		Update the list variable 'self.lAuthorizedMove', which contain the authorized move around the cell.
		"""
		lMoves = list()
		# Walls can't have authorized move
		if self.type == CellTypeWall:
			self.lAuthorizedMoves = lMoves
			return
		if cellUpType == CellTypePath: lMoves.append(MovementUp)
		if cellDownType == CellTypePath: lMoves.append(MovementDown)
		if cellRightType == CellTypePath: lMoves.append(MovementRight)
		if cellLeftType == CellTypePath: lMoves.append(MovementLeft)
		# Update list
		self.lAuthorizedMoves = lMoves
		return
	
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
