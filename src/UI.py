# -*- coding:utf-8 -*-

# Cyril Fournier
# 19/01/2016

import sys
import tty,termios # for getch
import threading
import time
import Queue
import wx

import UtilsAndGlobal as UAG

# ==================================
#    ===   Class UICatcher   ===
# ==================================

class UICatcher(threading.Thread):
	"""
	Windows catching user's keyboard event.
	"""
	def __init__(self, threadID, threadName, objApp, objUI):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.threadName = threadName
		self.objApp = objApp
		self.objUI = objUI

	def run(self):
		self.objUI.Show()
		self.objApp.MainLoop()

# ===========================
#    ===   Class UI   ===
# ===========================

class UI(threading.Thread, wx.Frame):
	"""
	Object controlling the interaction with the user: User Interface.
	This class use one thread.
	"""
	# ----------------------------------
	# --- Built-in functions
	# ----------------------------------
	def __init__(self, threadID, threadName, queue, queueLock, delay):
		self.direction = "Wait"
		# ========
		# Thread init: send user's direction to the Pacman object.
		# ========
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.threadName = threadName
		self.queue = queue
		self.queueLock = queueLock
		self.delay = delay
		
		# ========
		# Frame init: windows catching user's keyboard event.
		# ========
		wx.Frame.__init__(self, None, wx.ID_ANY, "Pacman game", size=(0,0))
		panel = wx.Panel(self, wx.ID_ANY)
		btn = wx.TextCtrl(panel, value="")
		btn.SetFocus()
		btn.Bind(wx.EVT_CHAR, self.onCharEvent)

	# ----------------------------------
	# --- Catch functions
	# ----------------------------------
	def onCharEvent(self, event):
		"""
		Catch keyboard event. Use WX library.
		"""
		keycode = event.GetKeyCode()
		controlDown = event.CmdDown()
		altDown = event.AltDown()
		shiftDown = event.ShiftDown()
		
		if keycode == UAG.MovementUp: self.direction = UAG.MovementUp
		elif keycode == UAG.MovementDown: self.direction = UAG.MovementDown
		elif keycode == UAG.MovementRight: self.direction = UAG.MovementRight
		elif keycode == UAG.MovementLeft: self.direction = UAG.MovementLeft
		else: self.direction = "Quit"
		event.Skip()

	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def run(self):
		time.sleep(1)
		while self.direction and not UAG.ExitFlag:
			if self.direction != "Wait":
				query = [UAG.CellCharacterPacman, self.direction]
				self.queueLock.acquire()
				print "[objUI] 2 - Put movement in queue: [%s, %s]" %(query[0], query[1])
				self.queue.put(query)
				self.queueLock.release()
				self.direction = "Wait"
			time.sleep(self.delay)
		# Close frame
		self.Close()
