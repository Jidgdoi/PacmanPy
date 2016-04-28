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

class UICatcher(wx.Frame):
	"""
	Windows catching user's keyboard event.
	"""
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Pacman game", size=(0,0))
		
		# Add a panel so it looks the correct on all platforms
		panel = wx.Panel(self, wx.ID_ANY)
		btn = wx.TextCtrl(panel, value="")
		btn.SetFocus()
		
		btn.Bind(wx.EVT_CHAR, self.onCharEvent)

	def onCharEvent(self, event):
		keycode = event.GetKeyCode()
		controlDown = event.CmdDown()
		altDown = event.AltDown()
		shiftDown = event.ShiftDown()
		
		print keycode
		if keycode == wx.WXK_UP: print "Up arrow"
		elif keycode == wx.WXK_DOWN: print "Down arrow"
		elif keycode == wx.WXK_RIGHT: print "Right arrow"
		elif keycode == wx.WXK_LEFT: print "Left arrow"
		event.Skip()

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
	def __init__(self, threadID, name, queue, queueLock, delay):
		# Init thread module in this class
		threading.Thread.__init__(self)
		
		self.threadID = threadID
		self.name = name
		self.queue = queue
		self.queueLock = queueLock
		self.delay = delay
		
		# ========
		# Frame init
		# ========
		wx.Frame.__init__(self, None, wx.ID_ANY, "Pacman game", size=(0,0))
		
		# Add a panel so it looks the correct on all platforms
		panel = wx.Panel(self, wx.ID_ANY)
		btn = wx.TextCtrl(panel, value="")
		btn.SetFocus()
		
		btn.Bind(wx.EVT_CHAR, self.onCharEvent)

	def onCharEvent(self, event):
		keycode = event.GetKeyCode()
		controlDown = event.CmdDown()
		altDown = event.AltDown()
		shiftDown = event.ShiftDown()
		
		print keycode
		if keycode == wx.WXK_UP: print "Up arrow"; self.sendQuery('\x1b[A')
		elif keycode == wx.WXK_DOWN: print "Down arrow"; self.sendQuery('\x1b[B')
		elif keycode == wx.WXK_RIGHT: print "Right arrow"; self.sendQuery('\x1b[C')
		elif keycode == wx.WXK_LEFT: print "Left arrow"; self.sendQuery('\x1b[D')
		else: print "Destroy"
		event.Skip()

	# ----------------------------------
	# --- Private functions
	# ----------------------------------
	def _getch(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(3)
		except KeyboardInterrupt: 
			ch = False
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

	# ----------------------------------
	# --- Common functions
	# ----------------------------------
	def movement(self):
		"""
		Check if the movement is valid (key pressed is ok).
		"""
		key = self._getch()
		print "[UI] Key: %s" %key
		if   key == '\x1b[A': return UAG.MovementUp
		elif key == '\x1b[B': return UAG.MovementDown
		elif key == '\x1b[C': return UAG.MovementRight
		elif key == '\x1b[D': return UAG.MovementLeft
		return False

	def sendQuery(self, direction):
		query = [UAG.CellCharacterPacman, direction]
		self.queueLock.acquire()
		self.queue.put(query)
		self.queueLock.release()
		time.sleep(self.delay)

	def run(self):
		mvt = True
		time.sleep(1)
		while mvt and not UAG.ExitFlag:
#			print "[objUI] 1 - Waiting movement"
			query = [UAG.CellCharacterPacman, self.movement()]
			self.queueLock.acquire()
#			print "[objUI] 2 - Put movement in queue"
			self.queue.put(query)
			self.queueLock.release()
			time.sleep(self.delay)
