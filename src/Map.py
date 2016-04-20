# -*- coding:utf-8 -*-

# Cyril Fournier
# 13/01/2016

import os,sys
import numpy as np

from UtilsAndGlobal import *
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
	def __init__(self, mapFile=''):
		# --- Load map
		self.size, self.pacmanPosition, self.grid = self.loadGrid(mapFile)
		
		# --- Update cells authorized moves
		self.updateCellsAuthorizedMoves()
		
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
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _initEmptyGrid(self, size):
		"""
		Return the grid of the game, of size 'size' (a list of lists).
		"""
		grid = [[Cell() for line in range(size[1])] for column in range(size[0])]
		return grid

	def _writeMap(self):
		"""
		Write the current map with the 'PacmanMap' code.
		"""
		txt = str()
		# Size
		txt += "%s,%s\n" %(self.size[0], self.size[1])
		# Pacman spawn TODO
		txt += "%s,%s\n" %(self.pacmanPosition[0], self.pacmanPosition[1])
		# Pacman position
		txt += "%s,%s\n" %(self.pacmanPosition[0], self.pacmanPosition[1])
		# Ghost spawn TODO
		# Ghost positions TODO
#		txt += "%s %s %s %s\n" %(["%s,%s" %(i.pos[0], i.pos[1]) for i in lGhostPositions])
		txt += "12,9 13,8 13,9 13,10\n"
		txt += "12,9 13,8 13,9 13,10\n"
		# Map
		for i in self.grid:
			for j in i:
				if   j.getType() == CellTypeWall: txt += 'w'
				elif j.getType() == CellTypePath: txt += 'p'
				elif j.getType() == CellTypeGlass: txt += 'g'
				# Item
				if   j.getItem() == CellItemPoint: txt += 'p'
				elif j.getItem() == CellItemPower: txt += 's'
				elif j.getItem() == CellItemNone: txt += 'n'
				# Character
				if   j.getCharacter() == CellCharacterNone: txt += 'n'
				elif j.getCharacter() == CellCharacterGhost: txt += 'g'
				elif j.getCharacter() == CellCharacterPacman: txt += 'p'
				txt += ' '
			txt = txt[:-1]
			txt += '\n'
		return txt

	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	def getPacmanPosition(self):
		return self.pacmanPosition

	def getCell(self, pos):
		return self.grid[pos[0]][pos[1]]

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
	def decodeCell(self, code):
		"""
		Decode a 3-characters string encoding a cell's description.
		"""
		# Type
		if   code[0] == 'w': Type = CellTypeWall
		elif code[0] == 'p': Type = CellTypePath
		elif code[0] == 'g': Type = CellTypeGlass
		# Item
		if   code[1] == 'p': Item = CellItemPoint
		elif code[1] == 's': Item = CellItemPower
		elif code[1] == 'n': Item = CellItemNone
		# Character
		if   code[2] == 'n': Char = CellCharacterNone
		elif code[2] == 'g': Char = CellCharacterGhost
		elif code[2] == 'p': Char = CellCharacterPacman
		
		return Cell(Type, Item, Char)
	
	def loadGrid(self, mapFile):
		"""
		Load a predefine map.
		"""
		# TODO Take care of ghosts and pacman spawn
		grid = list()
		with open(mapFile, 'r') as fh:
			# Map size:
			size = tuple( map(int, fh.next().strip().split(',')) )
			# Pacman spawn and current position
			pacmanSpawn = tuple( map(int, fh.next().strip().split(',')) )
			pacmanPosition = tuple( map(int, fh.next().strip().split(',')) )
			# Ghosts spawns and current positions
			lGhostSpawns = [map(int, i.split(',')) for i in fh.next().strip().split(' ')]
			lGhostPositions = [map(int, i.split(',')) for i in fh.next().strip().split(' ')]
			# Map
			for line in fh:
				grid.append( [self.decodeCell(code) for code in line.strip().split(' ')] )
		return size, pacmanPosition, grid
	
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
	
	def isMovePossible(self, From, move):
		"""
		Check if the movement is possible.
		'From': position of a Cell
		'move': movement direction
		"""
		print self.grid[From[0]][From[1]].getAuthorizedMoves()
		if move in self.grid[From[0]][From[1]].getAuthorizedMoves(): return True
		return False
	
	def moveAction(self, From, To):
		"""
		Return the action caused by the movement.
		'From': position of the current Cell
		'To': position of the target Cell
		"""
		FromCell = self.getCell(From)
		ToCell = self.getCell(To)
		# --- Pacman actions
		if FromCell.getCharacter() == CellCharacterPacman:
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
		'From': position of the current Cell
		'To': position of the target Cell
		'action': action caused by the movement
		"""
		FromCell = self.getCell(From)
		ToCell = self.getCell(To)
		# --- Pacman dies
		if action == ActionDie: return True
		# --- Any other action: the character moves
		ToCell.setCharacter(FromCell.getCharacter())
		FromCell.setCharacter(CellCharacterNone)
		# --- Is pacman moving:
		if ToCell.getCharacter() == CellCharacterPacman:
			self.setPacmanPosition(To)
			# There is an item
			if action in [ActionPoint, ActionPower]: ToCell.setItem(CellItemNone)





