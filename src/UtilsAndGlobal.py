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

CellDefaultResDist = 1e10

# --- Pacman state
PacmanSafe = 1

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
ActionPower = 777
ActionLoseLife = 165
ActionGetLife = 117
ActionWin = 42

# --- Threads
ExitFlag = 0

# --- Game control
PacmanDelay = 0.2
GhostSpeed = 0.3
FearTime = 10
EventTextTime = 3
LifeBonusThresh = 500
PointReward = 1
PowerReward = 10
KillReward = 100

# --- ASCII art
# "Language": Ivrit
# Source: http://www.patorjk.com/software/taag/#p=display&f=Ivrit&t=Type%20Something%20
GameOver="""
   ____                                              
  / ___| __ _ _ __ ___   ___      _____   _____ _ __ 
 | |  _ / _` | '_ ` _ \ / _ \    / _ \ \ / / _ \ '__|
 | |_| | (_| | | | | | |  __/   | (_) \ V /  __/ |   
  \____|\__,_|_| |_| |_|\___|    \___/ \_/ \___|_|   
                                                     
"""
GameWin="""
            __     __   __             __        ___           _      __           
  _____ ____\ \    \ \ / /__  _   _    \ \      / (_)_ __     | |    / /____ _____ 
 |_____|_____\ \    \ V / _ \| | | |    \ \ /\ / /| | '_ \    | |   / /_____|_____|
 |_____|_____/ /     | | (_) | |_| |     \ V  V / | | | | |   |_|   \ \_____|_____|
            /_/      |_|\___/ \__,_|      \_/\_/  |_|_| |_|   (_)    \_\           
                                                                                   
"""
Plus10Points="""
          _  ___      ____       _       _       
    _    / |/ _ \    |  _ \ ___ (_)_ __ | |_ ___ 
  _| |_  | | | | |   | |_) / _ \| | '_ \| __/ __|
 |_   _| | | |_| |   |  __/ (_) | | | | | |_\__ \
   |_|   |_|\___/    |_|   \___/|_|_| |_|\__|___/
                                                 
"""
Plus100Points="""
          _  ___   ___      ____       _       _       
    _    / |/ _ \ / _ \    |  _ \ ___ (_)_ __ | |_ ___ 
  _| |_  | | | | | | | |   | |_) / _ \| | '_ \| __/ __|
 |_   _| | | |_| | |_| |   |  __/ (_) | | | | | |_\__ \
   |_|   |_|\___/ \___/    |_|   \___/|_|_| |_|\__|___/
                                                       
"""
GhostKilledYou="""
   ____ _               _       _    _ _ _          _                       
  / ___| |__   ___  ___| |_    | | _(_) | | ___  __| |    _   _  ___  _   _ 
 | |  _| '_ \ / _ \/ __| __|   | |/ / | | |/ _ \/ _` |   | | | |/ _ \| | | |
 | |_| | | | | (_) \__ \ |_    |   <| | | |  __/ (_| |   | |_| | (_) | |_| |
  \____|_| |_|\___/|___/\__|   |_|\_\_|_|_|\___|\__,_|    \__, |\___/ \__,_|
                                                          |___/             
"""
Plus1LifeBonus="""
          _     _     _  __          _                           
    _    / |   | |   (_)/ _| ___    | |__   ___  _ __  _   _ ___ 
  _| |_  | |   | |   | | |_ / _ \   | '_ \ / _ \| '_ \| | | / __|
 |_   _| | |   | |___| |  _|  __/   | |_) | (_) | | | | |_| \__ \
   |_|   |_|   |_____|_|_|  \___|   |_.__/ \___/|_| |_|\__,_|___/
                                                                 
"""



