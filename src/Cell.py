# -*- coding:utf-8 -*-

# Cyril Fournier
# 15/01/2016

import os,sys

from UtilsAndGlobal import *

from Toolbox.MyToolbox import MyToolbox as MTB
from Toolbox.Colors import *

# ===========================
#    ===   Class Cell   ===
# ===========================

class Cell():
	"""
	Object representing a cell from the map, containing the cell type 
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, cellType=CellTypePath, item=CellItemNone):
		self.type = cellType
		self.item = item
	
	def __repr__(self):
		t, i = MTB.getKey(globals(), [self.type, self.item])
		return "(%s,%s)" %(t, i)
	
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
	
	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	def setItem(self, new):
		if self.type != CellTypeWall:
			self.item = new
	
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def deleteItem(self):
		self.item = None
	
	def toPrint(self):
		if self.item != CellItemNone:
			return self.item
		else:
			return self.type
