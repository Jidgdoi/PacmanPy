# -*- coding:utf-8 -*-

# Cyril Fournier
# 15/01/2016

from wx import WXK_UP, WXK_DOWN, WXK_RIGHT, WXK_LEFT

######################
# GLOBAL VARIABLES
######################
# --- Cell type
CellTypePath = 11760
CellTypeGlass = 17977
CellTypeWall = 12701
# --- Cell item
CellItemNone = 19725
CellItemPoint = 14759
CellItemPower = 10799
# --- Cell character
CellCharacterNone = 12568
CellCharacterPacman = 18419
CellCharacterGhost = 13012

# --- Pacman state
PacmanSafe = 1
PacmanOverPower = 42

# --- Ghost state
GhostAlive = 1
GhostAfraid = 2
GhostDead = 0

# --- Movement
MovementUp = WXK_UP
MovementDown = WXK_DOWN
MovementRight = WXK_RIGHT
MovementLeft = WXK_LEFT

# --- Action
ActionLose = 507317
ActionGhostDie = 666
ActionPoint = 117
ActionPower = 777

# --- Threads
ExitFlag = 0

# --- Game control
PacmanDelay = 0.2
GhostSpeed = 1.0
Lives = 3
PowerTime = 10


