# -*- coding:utf-8 -*-

# Cyril Fournier
# 13/01/2016

# ===========================
#    ===   Class Map   ===
# ===========================

import os,sys
import numpy as np
from datetime import datetime

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
			self.grid = self._createMap((21,21))
	
	def __repr__(self):
		return '\n'.join([' '.join(map(str,i)) for i in self.grid])
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _initEmptyGrid(self, size):
		"""
		Return the grid of the game, of size 'size' (a list of lists).
		"""
		grid = [[1 for line in range(size[1])] for column in range(size[0])]
		return grid

	def _createMap(self, size):
		"""
		Create a new map.
		"""
		grid = self._initEmptyGrid(size)
		
		# --- Border
		# Top
		for col in range(size[1]): grid[0][col] = 4
		# Bottom
		for col in range(size[1]): grid[size[0]-1][col] = 4
		# Left
		for line in range(size[0]): grid[line][0] = 4
		# Right
		for line in range(size[1]): grid[line][size[1]-1] = 4
		
		# --- Ghost spawn
		center = (size[0]/2, size[1]/2)
		for line in range(center[0] -1, center[0]+2):
			for col in range(center[1] -3, center[1]+3):
				grid[line][col] = 4
		for col in range(center[1] -2, center[1]+2): grid[center[0]][col] = 8
		for col in range(center[1] -1, center[1]+1): grid[center[0]-1][col] = 1
		
		# --- Pacman spawn
		pacmanLine = int((size[0]*3.0)/4)
		grid[pacmanLine][center[1]] = 0
		
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
