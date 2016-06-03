# -*- coding:utf-8 -*-

# Cyril Fournier
# 20/01/2016

import os,sys
import wx
import threading
import Queue
import time

import UtilsAndGlobal as UAG
from Cell import Cell
from Map import Map
from UI import UI, UICatcher
from GhostAI import GhostAI
from Graphical import Graphical
from Pacman import Pacman, PacmanGame

from Utility.MyToolbox import MyToolbox as MTB
import Utility.Colors as txt

# =======================
#    ===   Main   ===
# =======================

def getRootDir():
	return os.sep.join(os.path.realpath(sys.argv[0]).split(os.sep)[:-2])

def getMapPath():
	if len(sys.argv) == 2: return sys.argv[1]
	return "%s%s%s" %(rootDir, os.sep, UAG.DefaultMap)

def askQuestion(question, lChoices):
	"""
	Ask a question to the user, and return his answer.
	"""
	mess = "\n%s\n%s" %(colorQ(question), '\n'.join([ " [%s] %s" %(colorC(i+1), lChoices[i]) for i in range(len(lChoices))]))
	mess += "\n [%s] Quit\nChoice: %s" %(colorC('Q'), txt.buildColor(fgColor="Red"))
	choice = raw_input(mess)
	sys.stdout.write(txt.reset())
	sys.stdout.flush()
	
	if choice.lower() == 'q':
		sys.exit(0)
	
	if choice not in map(str,range(1,len(lChoices)+1)):
		print "Your choice \"%s\" doesn't exist." %choice
		return askQuestion(question, lChoices)
	
	return int(choice) -1

def setDifficulty(choice):
	"""
	Set game parameters for the selected difficulty.
	"""
	if choice == 0: # Easy
		UAG.GhostSpeed = 0.5
		UAG.FearTime = 10
		UAG.GhostPredator = 0
	if choice >= 1: # Medium
		UAG.GhostPredator = 1
		UAG.GhostSmell = 5
	if choice >= 2: # Hard
		UAG.GhostSpeed *= (2/3.0)
	if choice >= 3: # Nightmare
		UAG.GhostSmell += 3
		UAG.LifeBonusThresh = 1e10
		UAG.StartLife = 1
	if choice >= 4: # Doom
		UAG.GhostSpeed == UAG.PacmanDelay

def listMap(myPath):
	"""
	Ask the user to pick a map, and return the path to this file.
	"""
	# Get files
	lFiles = [f for f in os.listdir(myPath) if os.path.splitext(f)[1] == '.map']
	print lFiles
	
	if len(lFiles) == 0:
		print "No map to load."
		return False
	
	# Ask user
	choice = askQuestion("Choose file:", lFiles)
	print choice
	return ''.join([myPath, lFiles[choice]])


def terminalVersion():
	"""
	Game in terminal.
	"""
	# --- New game or load a save
	choice = askQuestion("Menu:", ["New game", "Load game"])
	
	if choice == 0:
		# New game
		objMap = Map(listMap("%s%smap%s" %(rootDir, os.sep, os.sep)))
		# Select difficulty
		difficulty = askQuestion("Select the difficulty:",
					["Easy: slow ghost.",
					 "Medium: slow ghost, mode predator ON.",
					 "Hard: fast ghost, mode predator ON.",
					 "Nightmare: fast ghost, mode boosted predator ON, 1 life, no bonus life.",
					 "Doom: run."])
		setDifficulty(difficulty)
	elif choice == 1:
		# Load game
		objMap = Map(listMap("%s%ssave%s" %(rootDir, os.sep, os.sep)))
	
	# --- Initiate threads and the wx app
	lock = threading.Lock()
	queue = Queue.Queue(5)
	
	objApp = wx.PySimpleApp()
	objUI = UI(1, "Thread-UI", queue, lock, UAG.PacmanDelay)
	objCatcher = UICatcher(2, "Thread-UICatcher", objApp, objUI)
	objGhostAI = GhostAI(3, "Thread-Ghost", queue, lock, UAG.GhostSpeed, len(objMap.dGhostSpawns))
	
	lThreads = [objUI, objCatcher, objGhostAI]
	
	print "[PacmanGame] Initiate threads"
	for t in lThreads:
		print "\t%s" %t.threadName
		t.start()
	
	# --- Initiate game
	game = PacmanGame(objMap, queue, lock, UAG.PacmanDelay, objUI=objUI, objGhostAI=objGhostAI)
	game.run()
	
	# --- Wait for all threads to terminate before leaving
	print "[PacmanGame] Wait all threads before leaving"
	for t in lThreads:
		print "\t%s" %t.threadName
		t.join()

def asciiArtVersion():
	"""
	Game in ASCII art.
	"""
	print "ASCII-art version is currently not available."

def graphicalVersion():
	"""
	Game in a window.
	"""
	print "Window version is currently not available."


if __name__=='__main__':
#	rows, columns = map(int, os.popen('stty size', 'r').read().split())
	print """
  .-.   .-.     .--.                    |=======================|                    .--.     .-.   .-.  
 | OO| | OO|   / _.-' .-.   .-.   .''.  |        Welcome        |  .''.   .-.   .-. '-._ \   |OO | |OO | 
 |   | |   |   \  '-. '-'   '-'   '..'  | To the PacmanPy game !|  '..'   '-'   '-' .-'  /   |   | |   | 
 '^^^' '^^^'    '--'                    |=======================|                    '--'    '^^^' '^^^' 
"""
	rootDir = getRootDir()
	colorQ = txt.color(fgColor='Cyan', bold=True)
	colorC = txt.color(fgColor='Yellow', bold=True)
	
	# ===========
	# === Select the graphical output version
	gameVersion = askQuestion("Select the graphical output version you want to play with:", ["Terminal version", "ASCII-art version", "Graphical version"])
	
	mapPath = getMapPath()
	if gameVersion == 0:
		terminalVersion()
	elif gameVersion == 1:
		asciiArtVersion()
	elif gameVersion == 2:
		graphicalVersion()
	print "Exit Pacman"

#os.system("gnome-terminal --geometry=60x20+2000+2000")


