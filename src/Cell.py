# -*- coding:utf-8 -*-

# Cyril Fournier
# 15/01/2016

import os,sys

import UtilsAndGlobal as UAG

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
	def __init__(self, cellType=UAG.CellTypePath, item=UAG.CellItemNone, character=UAG.CellCharacterNone):
		self.type = cellType
		self.item = item
		self.character = character
		self.dAuthorizedMoves = {}
	
	def __repr__(self):
		t, i, c = MTB.getKey(vars(UAG), [self.type, self.item, self.character])
		return "(%s,%s,%s)" %(t, i, c)
	
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
	
	def getAuthorizedMoves(self, Who):
		if Who == UAG.CellCharacterGhost:
			return self.dAuthorizedMoves[UAG.CellCharacterGhost]
		return self.dAuthorizedMoves[UAG.CellCharacterPacman]
	
	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	def setItem(self, new):
		if self.type != UAG.CellTypeWall:
			self.item = new
	
	def setCharacter(self, new):
		if self.type != UAG.CellTypeWall:
			self.character = new
	
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def deleteItem(self):
		self.item = UAG.CellItemNone
	
	def updateAuthorizedMoves(self, cellUpType, cellDownType, cellRightType, cellLeftType):
		"""
		Update the list variable 'self.lAuthorizedMove', which contain the authorized move around the cell.
		"""
		self.dAuthorizedMoves[UAG.CellCharacterPacman] = list()
		self.dAuthorizedMoves[UAG.CellCharacterGhost] = list()
		# Walls can't have authorized move
		if self.type == UAG.CellTypeWall: return
		# Others
		for t,d in [(cellUpType,UAG.MovementUp), (cellDownType,UAG.MovementDown), (cellRightType, UAG.MovementRight), (cellLeftType, UAG.MovementLeft)]:
			if t == UAG.CellTypePath:
				self.dAuthorizedMoves[UAG.CellCharacterPacman].append(d)
				self.dAuthorizedMoves[UAG.CellCharacterGhost].append(d)
			elif t == UAG.CellTypeGlass:
				self.dAuthorizedMoves[UAG.CellCharacterGhost].append(d)
		return
	
	def toPrint(self):
		"""
		Return the principle GLOBAL ID to print (pacman, point, wall ...)
		Character > Item > Cell type
		"""
		if self.character != UAG.CellCharacterNone:
			return self.character
		elif self.item != UAG.CellItemNone:
			return self.item
		else:
			return self.type
