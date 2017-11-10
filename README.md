# BOLT_3_Dash
# Author:
# Updated:

--------------------
Purpose
--------------------


--------------------
Files
--------------------
Files Includes With This Project (16):
.dash.py.swp    dash.py           gpsGauge.py         rpmGauge.py
.gitignore      debug.py          gpsReader.py        socGauge.py
args.psy        debugGps.py       lapTimePannel.py    spatial Reader.c
canReader.py    fileWriter.py     main.py             tempGauge.py



-------------------------
Design Decisions & Issues
-------------------------



Class Hierachy

		|-------------------------|             |------------|
                |     BinarySearchTree    |--has-a----->|   BSTNode  |
                |-------------------------|             |------------|
                           ^    ^                           ^  ^
                          /      \                          |  |
                       is-a     is-a                        |  |
                        /          \                        |  |
                       /           |--------------|         |  |
                      /            |  SplayTree   |-has-a---|  |
                     /             |--------------|            |
                    /                                        is-a 
                   /                                           |
    |----------------|                                  |------------|
    |     AVLTree    |--has-a-------------------------->| AVLNode    |
    |----------------|                                  |------------|
   
