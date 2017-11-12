# BOLT_3_Dash
# Author: VT Students
# Updated: November 2017

--------------------
Purpose
--------------------

--------------------
TO RUN:
--------------------
sudo python3 main.py
     -demo	opens demo mode
     -canoff 	don't start can/gps threads
     -gpsoff
     -dev	reads from real devices rather than displaying fake data
     -log	turns logging on

For riding use: sudo python3 main.py -dev -log

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
boost: serial reading
subprocess: communication between c and python
socketCan: reading from can bus

-------------------
Description of each file
-------------------

-------------------
dash.py
-------------------
Description of dash.py

-------------------
canReader.py
Description of canReader