############################################################################################################
## Description: Reads GPS information written to standard out by spatialReader.c, sends to gpsGauge.py
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
## Notes: 
## TODO: needs error checking if spatialReader executable does not exist
############################################################################################################

import sys
import time
import subprocess
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from args import Arg_Class

class GpsReader(QThread):

    currentLapTimeValue = pyqtSignal(int, int, int)

    latValue = pyqtSignal(float)
    longValue = pyqtSignal(float)
    rollValue = pyqtSignal(float)
    pitchValue = pyqtSignal(float)
    gForceValue = pyqtSignal(float)
    bodyAccelValue = pyqtSignal(float, float, float)
    velValue = pyqtSignal(float, float, float)
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        arguments = Arg_Class()
        print("gps worker thread:", self.currentThread())
        current_min = 0
        current_sec = 0
        current_msec = 100
        latitude = 37.0
        longitude = 38.0
        roll = 0.0 # degrees
        if arguments.Args.dev:
            while True:
                time.sleep(.1)
                self.currentLapTimeValue.emit(current_min, current_sec, current_msec) 
                self.latValue.emit(latitude)
                self.longValue.emit(longitude)
                self.rollValue.emit(roll)
                self.pitchValue.emit(0)
                self.gForceValue.emit(roll)
                self.bodyAccelValue.emit(0,0,0)
                self.velValue.emit(0,0,0)
                
                if current_msec >= 999:
                    current_sec=current_sec+1
                    current_msec = 0
                elif current_sec > 60:
                    current_min=current_min+1
                    
                current_msec = current_msec+100
                latitude = latitude+.001
                longitude = longitude+.025
                roll = roll+.05
            self.processEvents()
        else:
            print("Reading from GPS")
            #This runs a .c executable which writes to std-out,
            #subprocess reads from that
            #should use boost or embedding and exending

            #cmd = './spatialReader'        
            cmd = '/home/pi/BOLT_3_Dash/spatialReader'
            if not Path(cmd).exists():
                #if Path('./spatialReader').exists():
                cmd = './spatialReader'            
            
            #    else:
            #        exit(0)
            #else:
            #    exit(0)
            
            #need to add error checking to make sure the executable exitsts
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            buf = ""
            for out in iter(lambda: p.stdout.read(1), ''):
                if out.decode() != '\n':
                    buf = buf + str(out.decode())
                else:
                    if buf.split(':')[0] == 'lat':
                        latitude = buf.split(':')[1]
                        self.latValue.emit(float(latitude))                        
                    elif buf.split(':')[0] == 'long':
                        longitude = buf.split(':')[1]
                        self.longValue.emit(float(longitude))
                    elif buf.split(':')[0] == 'roll':
                        roll = buf.split(':')[1]
                        self.rollValue.emit(float(roll))
                    elif buf.split(':')[0] == 'pitch':
                        pitch = buf.split(':')[1]                        
                        self.pitchValue.emit(float(pitch))
                    elif buf.split(':')[0] == 'gForce':
                        gForce = buf.split(':')[1]
                        self.gForceValue.emit(float(gForce))
                    elif buf.split(':')[0] == 'body_accel':
                        accelX = buf.split(':')[1]
                        accelY = buf.split(':')[2]
                        accelZ = buf.split(':')[3]
                        self.bodyAccelValue.emit(float(accelX), float(accelY), float(accelZ))
                    elif buf.split(':')[0] == 'velocity':
                        velX = buf.split(':')[1]
                        velY = buf.split(':')[2]
                        velZ = buf.split(':')[3]
                        self.velValue.emit(float(velX), float(velY), float(velZ))
                    else:
                        print("ERROR: Parsing missed:", buf)
                    buf = ""

        self.exec()
                                                                                    
