# -*- coding:utf-8 -*-

# Cyril Fournier
# 19/01/2016

import os,sys
import tty,termios # for getch

import wx
from UtilsAndGlobal import *

from Utility.MyToolbox import MyToolbox as MTB
from Utility.Colors import *

# ===========================
#    ===   Class UI   ===
# ===========================

class UI():
	"""
	Object controlling the interaction with the user: User Interface.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self):
		self.a = 1
	
	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _getch(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(3)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
	# ----------------------------------
	# --- Get functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Set functions
	# ----------------------------------
	
	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def movement(self):
		"""
		Check if the movement is valid (key pressed is ok).
		"""
		key = self._getch()
		if   key == '\x1b[A': return MovementUp
		elif key == '\x1b[B': return MovementDown
		elif key == '\x1b[C': return MovementRight
		elif key == '\x1b[D': return MovementLeft
		return False
