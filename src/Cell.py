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
	def __init__(self, pos, cellType=UAG.CellTypePath, item=UAG.CellItemNone, dCharactersObj={}):
		self.pos = pos
		self.type = cellType
		self.item = item
		self.dCharactersObj = dCharactersObj
		self.dAuthorizedMoves = {}
		self.dGhostResurectionDistance = {}
		self.dGhostResurectionDirection = {}

	def __repr__(self):
		t, i, c = MTB.getKey(vars(UAG), [self.type, self.item, self.character])
		return "(%s,%s,%s)" %(t, i, c)

	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	def getType(self):
		return self.type

	def getItem(self):
		return self.item

	def getCharactersType(self, mostImportant=False):
		"""
		Return the list of characters present on this cell.
		'mostImportant': if pacman and ghost(s) are present, return pacman.
		"""
		if self.dCharactersObj.has_key(UAG.CellCharacterNone): return [UAG.CellCharacterNone]
		elif mostImportant and self.dCharactersObj.has_key(UAG.CellCharacterPacman): return [UAG.CellCharacterPacman]
		else: return list(set([c.character for c in self.dCharactersObj.values()]))

	def getCharactersObj(self, key=''):
		if key: return self.dCharacters[key]
		return self.dCharactersObj

	def getAuthorizedMoves(self, Who):
		if Who == UAG.CellCharacterGhost:
			return self.dAuthorizedMoves[UAG.CellCharacterGhost]
		return self.dAuthorizedMoves[UAG.CellCharacterPacman]

	def getGhostResurectionDistance(self, ghostID):
		"""
		Return the resurection distance of this cell for this ghost.
		"""
		if self.dGhostResurectionDistance.has_key(ghostID): return self.dGhostResurectionDistance[ghostID]
		return UAG.CellDefaultResDist

	def getGhostResurectionDirection(self, ghostID):
		"""
		Return the direction to take for the ghost to return to his spawn.
		"""
		return self.dGhostResurectionDirection[ghostID]

	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	def setItem(self, new):
		if self.type != UAG.CellTypeWall:
			self.item = new

	def addCharacter(self, new):
		self.dCharactersObj[new.ID] = new

	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def deleteItem(self):
		self.setItem(UAG.CellItemNone)

	def popCharacter(self, ID):
		return self.dCharactersObj.pop(ID)

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

	def updateResurectionDirection(self, ghostID, lResurectionDistance):
		"""
		Update the dictionary 'self.dGhostResurectionDirection', which contain the direction to take for dead ghost.
		"""
		
		index = lResurectionDistance.index(min( lResurectionDistance ))
		if index == 0:
			self.dGhostResurectionDirection[ghostID] = UAG.MovementUp
		elif index == 1:
			self.dGhostResurectionDirection[ghostID] = UAG.MovementDown
		elif index == 2:
			self.dGhostResurectionDirection[ghostID] = UAG.MovementRight
		else:
			self.dGhostResurectionDirection[ghostID] = UAG.MovementLeft

	def toPrint(self):
		"""
		Return the principle GLOBAL ID to print (pacman, point, wall ...)
		Character > Item > Cell type
		"""
		if self.dCharactersObj.keys():
			if self.dCharactersObj.has_key(UAG.CellCharacterPacman): return UAG.CellCharacterPacman
			else: return self.dCharactersObj.values()[0].state
		elif self.item != UAG.CellItemNone:
			return self.item
		else:
			return self.type
