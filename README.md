# BOLT_3_Dash
# Author: VT BOLT: Controls Sub-Team
# Updated: December 2017

--------------------
Purpose
--------------------
The dash board’s purpose is to display information to the rider of the motorcycle. At high speed the rider needs to see rpm, soc, and error information. The dash is also used to display debugging values during testing.


--------------------
TO RUN:
--------------------
sudo python3 main.py
     -demo			opens demo mode
     -canoff 		don't start canthreads
     -gpsoff		don't start canthreads
     -dev			reads from real devices rather than displaying fake data
     -log			turns logging on
     -fullscreen 	starts the dash in fullscreen mode

For riding use (Dec 2017) : sudo python3 main.py -dev -log -fullscreen

--------------------
Files
--------------------
Files Includes With This Project (16):
dash.py           gpsGauge.py         rpmGauge.py
debug.py          gpsReader.py        socGauge.py
args.psy        debugGps.py       lapTimePannel.py    spatial Reader.c
canReader.py    fileWriter.py     main.py             tempGauge.py

-------------------
DEPENDENCIES
------------------
pyqt5: graphics
subprocess: communication between c and python
socketCan: reading from can bus
boost: reading from spatial gps

------------------------
Description of each file
------------------------
------------------------
------------------------

-------------------
main.py
-------------------
runs all the necessary threads
creates all the necessary connections between signals and slots

-------------------
dash.py
-------------------
Creates the main window and application displayed on the touch screen
Places all the gauges in the window 
Creates menu options
Displays error messages in the form of changing the background color

-------------------
canReader.py
-------------------
Reads from the physical can bus connected to the raspberry pi through a pican2 shield. The can values are read in and processed in a state machine based on the CAN ID. Then each value is written to standard out with the format <label>:<value> or <label>:<x value>:<y value>:<z value>

-------------------
gpsReader.py
-------------------
Reads in gps data from the advanced navigation gps unit and sends the information to various gauges.
Creates a thread separate from dash that only reads gps messages and emits qt signals. 
Calls the spatialReader executable using subprocess reads from standard out, pareses it based on the label and emits a qt signal.
Subprocess is used to communicate between c and python

-------------------
fileWriter.py
-------------------
Has slots for all CAN bus and GPS signals. As new signals are received a large string is created in memory. The string is then written to memory every ten seconds. It is written in bulk because writing to a file is a slow operation that creates lag in the entire system.

-------------------
args.py
-------------------
Sets up a python library called argparse that handles command line arguments

--------------------------------------------------------
rpmGauge.py, socGauge.py, tempGauge.py, lapTimePannel.py
--------------------------------------------------------
Display various values to the rider

---------------------
debug.py, gpsDebug.py
---------------------
Create sepearte windows to display debugging values during testing

