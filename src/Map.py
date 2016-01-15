# -*- coding:utf-8 -*-

# Cyril Fournier
# 13/01/2016

import os,sys
import numpy as np

from UtilsAndGlobal import *
from Cell import *

from datetime import datetime
from Toolbox.MyToolbox import MyToolbox as MTB
from Toolbox.Colors import *

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
		for col in range(center[1] -1, center[1]+2): grid[center[0]][col] = Cell(cellType=CellTypePath, item=CellItemGhost)
		grid[center[0]-1][center[1]] = Cell(cellType=CellTypeGlass, item=CellItemGhost)
		
		# --- Pacman spawn
		grid[15][9] = Cell(cellType=CellTypePath, item=CellItemPacman)
		
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
				print grid[line][col]
				if grid[line][col].getItem() == CellItemNone and grid[line][col].getType() == CellTypePath:
					grid[line][col].setItem(CellItemPoint)
		
		return grid

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

	def changeCellType(self, coord, newType):
		"""
		Change the cell's type to 'newType' if it is possible.
		"""
		if self.grid[coord[0],coord[1]] != 4:
			self.grid[coord[0],coord[1]] = newType
