# -*- coding:utf-8 -*-

# Cyril Fournier
# 13/01/2016

import os,sys
import numpy as np

import UtilsAndGlobal as UAG
from Cell import Cell

from datetime import datetime
from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ===========================
#    ===   Class Map   ===
# ===========================

class Map():
	"""
	Object representing the game map, where the pacman, ghost etc. will move.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, mapFile):
		self.grid = list()
		self.pacmanPosition = list()
		self.pacmanSpawn = list()
		self.dGhostPositions = dict()
		self.dGhostSpawns = dict()
		
		# --- Load Map + Pacman/ghosts spawn|position
		self.loadMapFile(mapFile)
		
		# --- Update cells authorized moves
		self.updateCellsAuthorizedMoves()
		
		self.dColor = {UAG.CellItemNone: color()(" "),
					   UAG.CellItemPoint: color(fgColor="yellow", bold=True)("o"),
					   UAG.CellItemPower: color(fgColor="purple")("s"),
					   UAG.CellCharacterPacman: color(fgColor="blue")("P"),
					   UAG.CellCharacterGhost: color(fgColor="red", bold=True)("G"),
					   UAG.CellTypeWall: color(fgColor="black", bgColor="black", bold=False)("W"),
					   UAG.CellTypeGlass: color(bgColor="blue")(" "),
					   UAG.CellTypePath: color(fgColor="black")(" ")}

	def __repr__(self):
		return '\n'.join( [' '.join( [self.dColor[j.toPrint()] for j in i] ) for i in self.grid] )

	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _writeMap(self):
		"""
		Write the current map with the 'PacmanMap' code.
		"""
		txt = str()
		# Size
		txt += "%s,%s\n" %(self.size[0], self.size[1])
		# Pacman spawn and position
		txt += "%s,%s\n" %(self.pacmanSpawn[0], self.pacmanSpawn[1])
		txt += "%s,%s\n" %(self.pacmanPosition[0], self.pacmanPosition[1])
		# Ghost spawns and positions
		txt += "%s\n" %' '.join((["%s,%s" %(k, v[0], v[1]) for k,v in self.dGhostSpawns.items()]))
		txt += "%s\n" %' '.join((["%s,%s" %(k, v[0], v[1]) for k,v in self.dGhostPositions.items()]))
		# Map
		for i in self.grid:
			for j in i:
				if   j.getType() == UAG.CellTypeWall: txt += 'w'
				elif j.getType() == UAG.CellTypePath: txt += 'p'
				elif j.getType() == UAG.CellTypeGlass: txt += 'g'
				# Item
				if   j.getItem() == UAG.CellItemPoint: txt += 'p'
				elif j.getItem() == UAG.CellItemPower: txt += 's'
				elif j.getItem() == UAG.CellItemNone: txt += 'n'
				# Character
				if   j.getCharacter() == UAG.CellCharacterNone: txt += 'n'
				elif j.getCharacter() == UAG.CellCharacterGhost: txt += 'g'
				elif j.getCharacter() == UAG.CellCharacterPacman: txt += 'p'
				txt += ' '
			txt = txt[:-1]
			txt += '\n'
		return txt

	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	def getPacmanPosition(self):
		return self.pacmanPosition

	def getGhostPosition(self, ID):
		return self.dGhostPositions[ID]

	def getCell(self, pos):
		return self.grid[pos[0]][pos[1]]

	def getNextCellPos(self, pos, direction):
		"""
		Return the coordinates of the next cell.
		'pos': tuple of int - the position
		'direction': direction movement (MovementUp, MovementDown, MovementRight, MovementLeft).
		"""
		if direction == UAG.MovementUp:      return ((pos[0] -1)%self.size[0], pos[1])
		elif direction == UAG.MovementDown:  return ((pos[0] +1)%self.size[0], pos[1])
		elif direction == UAG.MovementRight: return (pos[0], (pos[1] +1)%self.size[1])
		elif direction == UAG.MovementLeft:  return (pos[0], (pos[1] -1)%self.size[1])
		return False

	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	def setPacmanPosition(self, pos):
		self.pacmanPosition = pos

	def setGhostPosition(self, ID, pos):
		self.dGhostPositions[ID] = pos

	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def decodeCell(self, code):
		"""
		Decode a 3-characters string encoding a cell's description.
		"""
		# Type
		if   code[0] == 'w': Type = UAG.CellTypeWall
		elif code[0] == 'p': Type = UAG.CellTypePath
		elif code[0] == 'g': Type = UAG.CellTypeGlass
		# Item
		if   code[1] == 'p': Item = UAG.CellItemPoint
		elif code[1] == 's': Item = UAG.CellItemPower
		elif code[1] == 'n': Item = UAG.CellItemNone
		# Character
		if   code[2] == 'n': Char = UAG.CellCharacterNone
		elif code[2] == 'g': Char = UAG.CellCharacterGhost
		elif code[2] == 'p': Char = UAG.CellCharacterPacman
		
		return Cell(Type, Item, Char)

	def loadMapFile(self, mapFile):
		"""
		Load a predefine map.
		"""
		# TODO Take care of ghosts and pacman spawn
		self.grid = list()
		with open(mapFile, 'r') as fh:
			# Map size:
			self.size = tuple( map(int, fh.next().strip().split(',')) )
			# Pacman spawn and current position
			self.pacmanSpawn = tuple( map(int, fh.next().strip().split(',')) )
			self.pacmanPosition = tuple( map(int, fh.next().strip().split(',')) )
			# Ghosts spawns and current positions
#			self.dGhostPositions = {map(int, i.split(',')) for i in fh.next().strip().split(' ')}
			for i in fh.next().strip().split(' '):
				tmp = map(int, i.split(','))
				self.dGhostPositions[tmp[0]] = tuple(tmp[1:])
			for i in fh.next().strip().split(' '):
				tmp = map(int, i.split(','))
				self.dGhostPositions[tmp[0]] = tuple(tmp[1:])
			# Map
			for line in fh:
				self.grid.append( [self.decodeCell(code) for code in line.strip().split(' ')] )
		return True

	def updateCellsAuthorizedMoves(self):
		"""
		For each cell of the grid, update his authorized moves.
		"""
		for l in range(self.size[0]):
			for c in range(self.size[1]):
				# Get cell's neighbors
				cellUp = self.grid[(l-1)%self.size[0]][c].getType()
				cellDown = self.grid[(l+1)%self.size[0]][c].getType()
				cellRight = self.grid[l][(c+1)%self.size[1]].getType()
				cellLeft = self.grid[l][(c-1)%self.size[1]].getType()
				# Update authorized moves
				self.grid[l][c].updateAuthorizedMoves(cellUp, cellDown, cellRight, cellLeft)

	def isMovePossible(self, From, direction):
		"""
		Check if the movement is possible.
		'From': position of a Cell
		'direction': movement direction
		"""
		if direction in self.grid[From[0]][From[1]].getAuthorizedMoves(UAG.CellCharacterPacman): return True
		return False

	def moveAction(self, Who, To):
		"""
		Return the action caused by the movement.
		'Who': ID of the character
		'To': position of the target Cell
		"""
		ToCell = self.getCell(To)
		if (Who == UAG.CellCharacterGhost and ToCell.getCharacter() == UAG.CellCharacterPacman) or (Who == UAG.CellCharacterPacman and ToCell.getCharacter() == UAG.CellCharacterGhost):
			# Pacman meet a ghost
			return UAG.ActionDie
		# --- Pacman specials actions
		if Who == UAG.CellCharacterPacman:
			# There is a point
			if ToCell.getItem() == UAG.CellItemPoint: return UAG.ActionPoint
			# There is a power
			if ToCell.getItem() == UAG.CellItemPower: return UAG.ActionPower
		# --- For all others cases: no actions
		return None

	def makeMove(self, From, To, Action, GhostID=None):
		"""
		Make a pre-verified move of 'who' from a position to another.
		'From': position of the current Cell
		'To': position of the target Cell
		'Action': action caused by the movement
		'GhostID': ghost ID
		"""
		FromCell = self.getCell(From)
		ToCell = self.getCell(To)
		# --- Update positions
		if ToCell.getCharacter() == UAG.CellCharacterPacman:
			# Pacman
			self.setPacmanPosition(To)
			# There is an item
			if Action in [UAG.ActionPoint, UAG.ActionPower]: ToCell.setItem(UAG.CellItemNone)
		else:
			# Ghost
			self.setGhostPosition(GhostID, To)
		
		# --- Update cell character
		ToCell.setCharacter(FromCell.getCharacter())
		#TODO Verify if From and Ghosts positions are both tuples
		if From not in self.dGhostPositions.values():
			FromCell.setCharacter(UAG.CellCharacterNone)





