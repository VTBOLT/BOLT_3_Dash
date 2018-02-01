############################################################################################################
## Description: Logs data to a file
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
## Notes: Currently saves data in memory for 10 seconds then writes to file
## TODO: Find faster way of writing to file and log more often
##       Also write data to mongodb
############################################################################################################
import sys
import time
from datetime import datetime as dt
from pathlib import Path
import subprocess
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from args import Arg_Class

class FileWriter(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):

        print("file worker thread:", self.currentThread())
        
        arguments = Arg_Class()

        self.rpm = 0.0
        self.soc = 0.0
        self.mcTemp = 0.0
        self.motorTemp = 0.0
        self.highMotorTemp = 0.0
        self.highCellTemp = 0.0
        self.lowCellTemp = 0.0
        self.DCL = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.gForce = 0.0
        self.bodyAccelx = 0.0
        self.bodyAccely = 0.0
        self.bodyAccelz = 0.0
        self.velx = 0.0
        self.vely = 0.0
        self.velz = 0.0

        self.error = 0
        
        if arguments.Args.log:
            
            vbox_path = '/home/vbox/logs/'
            pi_path = '/home/pi/logs/'
            alex_path = '/home/alex/pi/logs/'
            
            if Path(pi_path).exists():
                path = pi_path
            elif Path(vbox_path).exists():
                path = vbox_path
            elif Path(alex_path).exists():
                path = alex_path
            
            filename_time = 'dash_log_'+str(dt.now().year)+'_'+str(dt.now().month)+'_'+str(dt.now().day)+'_'+str(dt.now().hour)+'_'+str(dt.now().minute)+'.csv'

            self.filename = path+filename_time
            #use traditional file writing, the python csv libary is slow
            csvWriter = open(self.filename, 'a')
            
            self.startTime = time.time()
            pastTime = 0
            currentTime = 0

            count = 0
            temp = ""

            #creates a header
            temp = 'currentTime, '+ 'rpm, '+ 'soc, '+ 'mcTemp, '+ 'motorTemp, '+ 'highMotorTemp, '+ 'highestCellTemp, '+'lowestCellTemp, '+'DCL, '+'latitude, '+ 'longitude, '+'roll, '+ 'pitch, '+ 'gForce, '+ 'bodyAccelx, '+ 'bodyAccely, '+ 'bodyAccelz, '+ 'velx, '+ 'vely, '+ 'velz, '
            
            while True:
                startTimer = time.time()
                self.currentTime = "{0:.2f}".format(float(time.time())-self.startTime) #reduces precision of time and sets up time from start
                if self.currentTime != pastTime:
                    self.currentTime = "{0:.2f}".format(float(time.time())-self.startTime)
                    pastTime = currentTime
                    if count < 20:#waits for a block of 20 data collections before writing to the file
                        temp = temp + str(self.currentTime)+','+str(self.rpm)+','+str(self.soc)+','+str(self.mcTemp)+','+str(self.motorTemp)+','+str(self.highMotorTemp)+','+str(self.highCellTemp)+','+str(self.lowCellTemp)+','+str(self.DCL)+','+str(self.latitude)+','+str(self.longitude)+','+str(self.roll)+','+str(self.pitch)+','+str(self.gForce)+','+str(self.bodyAccelx)+','+str(self.bodyAccely)+','+str(self.bodyAccelz)+','+str(self.velx)+','+str(self.vely)+','+str(self.velz)+'\n'
                        count=count+1
                    else:
                        csvWriter.write(temp)
                        count = 0
                        temp = ""
                time.sleep(.5)# slows down file writing to reduce lag
        self.exec()
                                                                                    
    @pyqtSlot(int)
    def rpm_write(self, value):
        if value < 0:
            value = 0
        self.rpm = value        
            
    @pyqtSlot(float)
    def soc_write(self, value):
        self.soc = value
        
    @pyqtSlot(float)
    def mcTemp_write(self, value):
        self.mcTemp = value
        
    @pyqtSlot(float)
    def motorTemp_write(self, value):
        self.motorTemp = value

    @pyqtSlot(float)
    def highMotorTemp_write(self, value):
        self.highMotorTemp = value
        
    @pyqtSlot(float)
    def highCellTemp_write(self, value):
        self.highCellTemp = value
    @pyqtSlot(float)
    def lowCellTemp_write(self, value):
        self.lowCellTemp = value
    @pyqtSlot(float)
    def DCL_write(self, value):
        self.DCL = value
    @pyqtSlot(float)
    def lat_write(self, value):
        self.latitude = value
        
    @pyqtSlot(float)
    def long_write(self, value):
        self.longitude = value
        
    @pyqtSlot(float)
    def roll_write(self, value):
        self.roll = value
        
    @pyqtSlot(float)
    def pitch_write(self, value):
        self.pitch = value
        
    @pyqtSlot(float)
    def gForce_write(self, value):
        self.gForce = value
        
    @pyqtSlot(float, float, float)
    def bodyAccel_write(self, x, y, z):
        self.bodyaccelx = x
        self.bodyaccely = y
        self.bodyaccelz = z
        
    @pyqtSlot(float, float, float)
    def vel_write(self, x, y, z):
        self.velx = x
        self.vely = y
        self.velz = z
        
    @pyqtSlot(int, int, int, int)
    def error_write(self, v1, v2, v3, v4):
        self.error = v1
        temp = "ERROR," + str(self.currentTime)+','+str(v1)+','+str(v2)+','+str(v3)+','+str(v4)+'\n'
        #print("Error from CAN bus:", v1, v2, v3, v4)
        csvWriter_error = open(self.filename, 'a')
        csvWriter_error.write(temp)

        
