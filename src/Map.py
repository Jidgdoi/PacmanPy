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
		self.nPoints = int()
		self.playerPoints = int()
		self.playerLives = int()
		
		# --- Load Map + Pacman/ghosts spawn/position + count points
		self.loadMapFile(mapFile)
		
		# --- Update cells authorized moves
		self.updateCellsAuthorizedMoves()
		
		# --- Update cells resurection paths
		self.updateCellResurectionPath()
		
		self.dColor = {UAG.CellItemPoint: color(fgColor="yellow", bold=True)("o"),
					   UAG.CellItemPower: color(fgColor="purple")("s"),
					   UAG.CellCharacterPacman: color(fgColor="blue")("P"),
					   UAG.GhostAlive: color(fgColor="red", bold=True)("G"),
					   UAG.GhostAfraid: color(fgColor="blue", bold=True)("G"),
					   UAG.GhostDead: color(fgColor="white", bold=True)("G"),
					   UAG.CellTypeWall: color(fgColor="black", bgColor="black", bold=False)("W"),
					   UAG.CellTypeGlass: color(bgColor="blue")(" "),
					   UAG.CellTypePath: color()(" ")}

	def __repr__(self):
#		return '\n'.join( [' '.join( [self.dColor[j.toPrint()] for j in i] ) for i in self.grid] )
		txt = ''
		for line in self.grid:
			previousCellType = False
			for cell in line:
				if previousCellType:
					# Space between 2 walls: set features wall for the space
					if previousCellType == UAG.CellTypeWall and cell.getType() == UAG.CellTypeWall: txt += self.dColor[UAG.CellTypeWall]
					# A glass: set both sides of glass as glass features
					elif previousCellType == UAG.CellTypeGlass or cell.getType() == UAG.CellTypeGlass: txt += self.dColor[UAG.CellTypeGlass]
					# Just a space
					else: txt += ' '
				txt += self.dColor[cell.toPrint()]
				previousCellType = cell.getType()
			txt += '\n'
		return txt

	# ----------------------------------
	# --- PacmanMap functions
	# ----------------------------------
	def decodeCell(self, line, col, code):
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
		# Characters will be placed later
		return Cell((line,col), Type, Item, {})

	def loadMapFile(self, mapFile):
		"""
		Load a 'PacmanMap' file.
		"""
		# TODO Take care of ghosts and pacman spawn
		self.grid = list()
		fh = open(mapFile, 'r')
		l = fh.readline()
		while l:
			while l:
				print "2nd while"
				if l[0] == "#":
					header = l.strip()[1:]
					break
				else:
					l = fh.readline()
			print "header: %s" %header
			print l
			# Map size:
			if header == "Size":
				self.size = tuple( map(int, fh.readline().strip().split(',')) )
			# Pacman spawn and current position
			elif header == "PacmanSpawn":
				self.pacmanSpawn = tuple( map(int, fh.readline().strip().split(',')) )
			elif header == "PacmanPosition":
				self.pacmanPosition = tuple( map(int, fh.readline().strip().split(',')) )
			# Ghosts spawns and current positions
			elif header == "GhostSpawns":
				for i in fh.readline().strip().split(' '):
					tmp = map(int, i.split(','))
					self.dGhostSpawns[tmp[0]] = tuple(tmp[1:])
			elif header == "GhostPositions":
				for i in fh.readline().strip().split(' '):
					tmp = map(int, i.split(','))
					self.dGhostPositions[tmp[0]] = tuple(tmp[1:])
			# Map
			elif header == "Map":
				print range(self.size[0])
				for i in range(self.size[0]):
					words = fh.readline().strip().split(' ')
					self.grid.append( [self.decodeCell(l, c, words[c]) for c in range(len(words))] )
			elif header == "PlayerPoints":
				self.playerPoints = int(fh.readline().strip())
			elif header == "PlayerLives":
				self.playerLives = int(fh.readline().strip())
			else:
				print "\033[1;31m[Map] Map loading error: '%s' header unknown." %header
				sys.exit()
			l = fh.readline()
		fh.close()
		# Count number of points
		self.nPoints = sum( [sum([1 if cell.getItem() == UAG.CellItemPoint else 0 for cell in line]) for line in self.grid] )
		return True

	def writePacmanMap(self, fileName, points, lives):
		"""
		Write the current map with the 'PacmanMap' code.
		"""
		txt = str()
		# Size
		txt += "#Size\n%s,%s\n" %(self.size[0], self.size[1])
		# Pacman spawn and position
		txt += "#PacmanSpawn\n%s,%s\n" %(self.pacmanSpawn[0], self.pacmanSpawn[1])
		txt += "#PacmanPosition\n%s,%s\n" %(self.pacmanPosition[0], self.pacmanPosition[1])
		# Ghost spawns and positions
		txt += "#GhostSpawns\n%s\n" %' '.join((["%s,%s,%s" %(k, v[0], v[1]) for k,v in self.dGhostSpawns.items()]))
		txt += "#GhostPositions\n%s\n" %' '.join((["%s,%s,%s" %(k, v[0], v[1]) for k,v in self.dGhostPositions.items()]))
		# Map
		txt += "#Map\n"
		for i in self.grid:
			for j in i:
				# Type
				if   j.getType() == UAG.CellTypeWall: txt += 'w'
				elif j.getType() == UAG.CellTypePath: txt += 'p'
				elif j.getType() == UAG.CellTypeGlass: txt += 'g'
				# Item
				if   j.getItem() == UAG.CellItemPoint: txt += 'p'
				elif j.getItem() == UAG.CellItemPower: txt += 's'
				elif j.getItem() == UAG.CellItemNone: txt += 'n'
				# Character
				if   j.getCharactersType(mostImportant=True) == UAG.CellCharacterGhost: txt += 'g'
				elif j.getCharactersType(mostImportant=True) == UAG.CellCharacterPacman: txt += 'p'
				else : txt += 'n'
				txt += ' '
			txt = txt[:-1]
			txt += '\n'
		# Player points
		txt += "#PlayerPoints\n%s\n" %points
		# Player lives
		txt += "#PlayerLives\n%s\n" %lives
		# Open and write to fileName
		fh = open(fileName, 'w')
		fh.write(txt)
		fh.close()

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

	def getCellNeighborsResurectionPath(self, pos, ghostID):
		"""
		Return for each neighbor's cell of the given one, the resurection path value for the given ghost.
		"""
		values = [(pos, self.getCell(self.getNextCellPos(pos, i)).getGhostResurectionPath(ghostID)) for i in self.getCell(pos).getAuthorizedMoves(UAG.CellCharacterGhost)]
		return sorted(values, key = lambda x: x[1])

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

	def updateCellResurectionPath(self):
		"""
		For each cell of the grid, update his resurection path according to each ghost spawn.
		"""
		for ID,spawn in self.dGhostSpawns.items():
			lCellToUpdate = [(spawn, 0)]
			while lCellToUpdate:
				tmp = []
				for c in lCellToUpdate:
					currCell = self.getCell(c[0])
					# check if cell has been already updated for this ghost
					if currCell.dGhostResurectionPath.has_key(ID):
						continue
					else:
						# update cell resurection path for ghost 'ID'
						currCell.dGhostResurectionPath[ID] = c[1]
						# add all neighbors cells to the tmp CellToUpdate
						tmp.extend([(self.getNextCellPos(c[0],i), c[1]+1) for i in currCell.getAuthorizedMoves(UAG.CellCharacterGhost)])
				lCellToUpdate = tmp

	def updateCellResurectionDirection(self):
		"""
		For each cell of the grid, update his resurection direction according to his neighbor.
		"""

	def isMovePossible(self, From, direction):
		"""
		Check if the movement is possible.
		'From': position of a Cell
		'direction': movement direction
		"""
		if direction in self.grid[From[0]][From[1]].getAuthorizedMoves(UAG.CellCharacterPacman): return True
		return False

	def actionCaused(self, Who, To):
		"""
		Return the action caused by the movement.
		'Who': Pacman object or Ghost object
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

