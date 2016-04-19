# -*- coding:utf-8 -*-

# Cyril Fournier
# 20/01/2016

import os,sys
import wx
import threading

from UtilsAndGlobal import *
from Cell import Cell
from Map import Map
from UI import UI
from GhostAI import GhostAI
from Graphical import Graphical

from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ===============================
#    ===   Class Pacman   ===
# ===============================

class Pacman():
	"""
	Main
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, objMap=None, objGraphical=None, objUI=None):
		self.objMap = objMap or Map()
		self.objGraphical = objGraphical or Graphical()
		self.objUI = objUI or UI()
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def pacmanMovement(self, direction):
		"""
		Make all modifications and actions to move Pacman to his new position.
		"""
		# --- Get both Pacman and his next cell positions
		pacmanPos = self.objMap.getPacmanPosition()
		nextCellPos = self.objMap.getNextCellPos(pacmanPos, direction)
		print "Size map: %s, %s" %(self.objMap.size[0], self.objMap.size[1])
		print "Postion: %s\tNext: %s" %(pacmanPos, nextCellPos)
		
		# If the move was correct
		if nextCellPos:
			if self.objMap.isMovePossible(who=CellCharacterPacman, From=pacmanPos, To=nextCellPos):
				action = self.objMap.moveAction(who=CellCharacterPacman, From=pacmanPos, To=nextCellPos)
				self.objMap.makeMove(From=pacmanPos, To=nextCellPos, action=action)
				#TODO
				# Following the action, add a point, gives power, and die: update Graphical interface



	# ----------------------------------
	# --- RUN
	# ----------------------------------
	def run(self):
		mvt = True
		while mvt:
			print self.objMap
			mvt = self.objUI.movement()
			print "Movement: %s" %mvt
			if mvt: self.pacmanMovement(mvt)
		return

if __name__=='__main__':
	print "=======================\n\tWelcome\n To the PacmanPy game !\n======================="
	print len("======================="), len("Welcome")
	game = Pacman()
	game.run()

