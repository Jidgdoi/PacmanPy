# -*- coding:utf-8 -*-

# Cyril Fournier
# 13/01/2016

import os,sys
import numpy as np

from UtilsAndGlobal import *
<<<<<<< HEAD
from Cell import Cell

from datetime import datetime
from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *
=======
from Cell import *

from datetime import datetime
from Toolbox.MyToolbox import MyToolbox as MTB
from Toolbox.Colors import *
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6

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
	def __init__(self, mapFile=''):
<<<<<<< HEAD
		if mapFile: self.grid = self.loadGrid()
		else:       self.grid = self._createBasicMap()
		self.size = (len(self.grid), len(self.grid[0]))
		
		self.pacmanPosition = (15,9)
		self.dColor = {CellItemNone: color()(" "),
					   CellItemPoint: color(fgColor="yellow", bold=True)("o"),
					   CellItemPower: color(fgColor="purple")("s"),
					   CellCharacterPacman: color(fgColor="blue")("P"),
					   CellCharacterGhost: color(fgColor="red", bold=True)("G"),
					   CellTypeWall: color(fgColor="black", bgColor="black", bold=False)("W"),
					   CellTypeGlass: color(bgColor="blue")(" "),
					   CellTypePath: color(fgColor="black")(" ")}
	
	def __repr__(self):
		return '\n'.join( [' '.join( [self.dColor[j.toPrint()] for j in i] ) for i in self.grid] )
=======
		if mapFile:
			self.grid = self.loadGrid()
			self.size = (len(self.grid), len(self.grid[0]))
		else:
			self.grid = self._createBasicMap()
		
		self.dColor = {CellItemNone: color()(" "),
					   CellItemPacman: color(fgColor="yellow")("P"),
					   CellItemPoint: color(fgColor="yellow", bold=True)("o"),
					   CellItemPower: color(fgColor="purple")("s"),
					   CellItemGhost: color(fgColor="red", bold=True)("G"),
					   CellTypeWall: color(fgColor="black", bgColor="black", bold=False)("W")}
	
	def __repr__(self):
		return '\n'.join([' '.join([self.dColor[j.toPrint()] for j in i]) for i in self.grid])
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _initEmptyGrid(self, size):
		"""
		Return the grid of the game, of size 'size' (a list of lists).
		"""
		grid = [[Cell() for line in range(size[1])] for column in range(size[0])]
		return grid

	def _createBasicMap(self):
		"""
		Create the basic map.
		"""
		size = (21,19)
		grid = self._initEmptyGrid(size)
		
		# --- Border
		# Top
		for col in range(size[1]): grid[0][col] = Cell(cellType=CellTypeWall)
		# Bottom
		for col in range(size[1]): grid[size[0]-1][col] = Cell(cellType=CellTypeWall)
		# Left
		for line in range(size[0]): grid[line][0] = Cell(cellType=CellTypeWall)
		# Right
		for line in range(size[0]): grid[line][size[1]-1] = Cell(cellType=CellTypeWall)
		
		# --- Ghost spawn
		center = (9,9)
		for line in range(center[0] -1, center[0]+2):
			for col in range(center[1] -2, center[1]+3):
				grid[line][col] = Cell(cellType=CellTypeWall)
<<<<<<< HEAD
		for col in range(center[1] -1, center[1]+2): grid[center[0]][col] = Cell(cellType=CellTypePath, character=CellCharacterGhost)
		grid[center[0]-1][center[1]] = Cell(cellType=CellTypeGlass, character=CellCharacterGhost)
		
		# --- Pacman spawn
		grid[15][9] = Cell(cellType=CellTypePath, character=CellCharacterPacman)
=======
		for col in range(center[1] -1, center[1]+2): grid[center[0]][col] = Cell(cellType=CellTypePath, item=CellItemGhost)
		grid[center[0]-1][center[1]] = Cell(cellType=CellTypeGlass, item=CellItemGhost)
		
		# --- Pacman spawn
		grid[15][9] = Cell(cellType=CellTypePath, item=CellItemPacman)
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
		
		# --- Power
		grid[2][1] = grid[2][17] = grid[15][1] = grid[15][17] = Cell(cellType=CellTypePath, item=CellItemPower)
		
		# --- Obstacles/walls
		for col in [9]:									grid[1][col] = Cell(cellType=CellTypeWall)
		for col in [2,3,5,6,7,9,11,12,13,15,16]:		grid[2][col] = Cell(cellType=CellTypeWall)
		for col in [2,3,5,7,8,9,10,11,13,15,16]:		grid[4][col] = Cell(cellType=CellTypeWall)
		for col in [5,9,13]:							grid[5][col] = Cell(cellType=CellTypeWall)
		for col in [1,2,3,5,6,7,9,11,12,13,15,16,17]:	grid[6][col] = Cell(cellType=CellTypeWall)
		for col in [1,2,3,5,13,15,16,17]:				grid[7][col] = Cell(cellType=CellTypeWall)
		for col in [1,2,3,5,13,15,16,17]:				grid[8][col] = Cell(cellType=CellTypeWall)
		for col in [1,2,3,5,13,15,16,17]:				grid[10][col] = Cell(cellType=CellTypeWall)
		for col in [1,2,3,5,13,15,16,17]:				grid[11][col] = Cell(cellType=CellTypeWall)
		for col in [1,2,3,5,7,8,9,10,11,13,15,16,17]:	grid[12][col] = Cell(cellType=CellTypeWall)
		for col in [9]:									grid[13][col] = Cell(cellType=CellTypeWall)
		for col in [2,3,5,6,7,9,11,12,13,15,16]:		grid[14][col] = Cell(cellType=CellTypeWall)
		for col in [3,15]:								grid[15][col] = Cell(cellType=CellTypeWall)
		for col in [1,3,5,7,8,9,10,11,13,15,17]:		grid[16][col] = Cell(cellType=CellTypeWall)
		for col in [5,9,13]:							grid[17][col] = Cell(cellType=CellTypeWall)
		for col in [2,3,4,5,6,7,9,11,12,13,14,15,16]:	grid[18][col] = Cell(cellType=CellTypeWall)
		
		# -- Doors
		grid[9][0] = grid[9][18] = Cell(cellType=CellTypePath)
		
		# --- Food
		for line in range(len(grid)):
			for col in range(len(grid[line])):
<<<<<<< HEAD
				if grid[line][col].getType() == CellTypePath and\
				   grid[line][col].getItem() == CellItemNone and\
				   grid[line][col].getCharacter() == CellCharacterNone:
=======
				print grid[line][col]
				if grid[line][col].getItem() == CellItemNone and grid[line][col].getType() == CellTypePath:
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
					grid[line][col].setItem(CellItemPoint)
		
		return grid

<<<<<<< HEAD
	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	def getPacmanPosition(self):
		return self.pacmanPosition

	def getCell(self, pos):
		if (pos[0] >= 0 and pos[0] < self.size[0]) and (pos[1] >= 0 and pos[1] < self.size[1]):
			return self.grid[pos[0]][pos[1]]
		return False

	def getNextCellPos(self, pos, direction):
		"""
		Return the coordinates of the next cell.
		'pos': tuple of int - the position
		'direction': direction movement (MovementUp, MovementDown, MovementRight, MovementLeft).
		"""
		if direction == MovementUp:      return ((pos[0] -1)%self.size[0], pos[1])
		elif direction == MovementDown:  return ((pos[0] +1)%self.size[0], pos[1])
		elif direction == MovementRight: return (pos[0], (pos[1] +1)%self.size[1])
		elif direction == MovementLeft:  return (pos[0], (pos[1] -1)%self.size[1])
		return False

	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	def setPacmanPosition(self, pos):
		self.pacmanPosition = pos

	# ----------------------------------
	# --- Common functions
	# ----------------------------------
=======
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
	def loadGrid(self, mapFile):
		"""
		Load a predefine map.
		"""
		f = open(mapFile, 'r')
		# --- Get map size
		nLine, nCol = map(int, f.readline().strip().split())
		# --- Fill the grid
		grid = self._initEmptyGrid((nLine, nCol))
		l = f.readline()
		while l:
			v = map(int, l.strip().split())
			grid[v[0]][v[1]] = v[2]
		f.close()
		return grid

<<<<<<< HEAD
	def isMovePossible(self, who, From, To):
		"""
		Check if the movement of 'who' is possible from a cell position to another.
		'who': Cell character ID
		'From': position of a Cell
		'To': position of a cell
		"""
		# If Cells aren't neighbor, the move isn't possible
		if abs(From[0]%self.size[0] - To[0]%self.size[0]) > 1: return False
		if abs(From[1]%self.size[1] - To[1]%self.size[1]) > 1: return False
		
		# If Cell is of type wall, the move isn't possible
		if self.getCell(To).getType() == CellTypeWall: return False
		
		if who == CellCharacterPacman:
			if self.getCell(To).getType() == CellTypeGlass: return False
		
		# -- Move is possible
		return True

	def moveAction(self, who, From, To):
		"""
		Return the action caused by the movement.
		"""
		ToCell = self.getCell(To)
		# --- Pacman actions
		if who == CellCharacterPacman:
			# There is a ghost
			if ToCell.getCharacter() == CellCharacterGhost: return ActionDie
			# There is a point
			if ToCell.getItem() == CellItemPoint: return ActionPoint
			# There is a power
			if ToCell.getItem() == CellItemPower: return ActionPower
		# --- Ghost actions
		else:
			# There is Pacman
			if ToCell.getCharacter() == CellCharacterPacman: return ActionDie
		# --- For all others cases: no actions
		return None

	def makeMove(self, From, To, action):
		"""
		Make a pre-verified move of 'who' from a position to another.
		'who': Cell character ID
		'From': position of a Cell
		'To': position of a cell
		"""
		FromCell = self.getCell(From)
		ToCell = self.getCell(To)
		
		# --- Pacman dies
		if action == ActionDie: return True
		# --- Any other action: the character moves
		ToCell.setCharacter(FromCell.getCharacter())
		FromCell.setCharacter(CellCharacterNone)
		# --- If there is an item
		if action in [ActionPoint, ActionPower]: ToCell.setItem(CellItemNone)
		# --- It it's pacman moving:
		if ToCell.getCharacter() == CellCharacterPacman:
			self.setPacmanPosition(To)






=======
	def changeCellType(self, coord, newType):
		"""
		Change the cell's type to 'newType' if it is possible.
		"""
		if self.grid[coord[0],coord[1]] != 4:
			self.grid[coord[0],coord[1]] = newType
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
