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
	def __init__(self, mapFile='', objMap=None, objGraphical=None, objUI=None):
		self.objMap = objMap or Map(mapFile)
		self.objGraphical = objGraphical or Graphical()
		self.objUI = objUI or UI()
		self.points = 0

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
		if self.objMap.isMovePossible(From=pacmanPos, move=direction):
			action = self.objMap.moveAction(From=pacmanPos, To=nextCellPos)
			self.objMap.makeMove(From=pacmanPos, To=nextCellPos, action=action)
			if action in [ActionPoint, ActionPower]: self.points += 1
			#TODO
			# Following the action, add a point, give power and die: update Graphical interface
	
	def ghostMovement(self, direction):
		"""
		Make all modifications and actions to move the ghost to his new position.
		"""
		



	# ----------------------------------
	# --- RUN
	# ----------------------------------
	def run(self):
		mvt = True
		while mvt:
			print self.objMap
			mvt = self.objUI.movement()
			print "Movement: %s" %mvt
			print "Points: %s" %self.points
			self.pacmanMovement(mvt)
		return

if __name__=='__main__':
	print "="*23
	print "Welcome".center(23)
	print "To the PacmanPy game !".center(23)
	print "="*23
	rootDir = os.sep.join(os.path.realpath(sys.argv[0]).split(os.sep)[:-2])
	mapFile = ''
	if len(sys.argv) == 2: mapFile = sys.argv[1]
	game = Pacman(mapFile)
	game.run()

