import sys
import time
import csv
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
        self.cellTemp = 0.0
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

        if arguments.Args.log:

            vbox_path = '/home/vbox/logs/'
            pi_path = '/home/pi/logs/'
            
            if Path(pi_path).exists():
                path = pi_path
            elif Path(vbox_path).exists():
                path = vbox_path
            
            filename = 'dash_log_'+str(dt.now().year)+'_'+str(dt.now().month)+'_'+str(dt.now().day)+'_'+str(dt.now().hour)+'_'+str(dt.now().minute)+'.csv'

            
            csvWriter = open(path + filename, 'w')
            writer = csv.writer(csvWriter, lineterminator='\n')
            
            self.startTime = time.time()
            pastTime = 0
            currentTime = 0

            ## Header
            writer.writerow(['currentTime', 'rpm', 'soc', 'mcTemp', 'motorTemp', 'highMotorTemp', 'cellTemp', 'latitude', 'longitude', 'roll', 'pitch', 'gForce', 'bodyAccelx', 'bodyAccely', 'bodyAccelz', 'velx', 'vely', 'velz'])
            
            while True:                
                #currentTime = "{0:.2f}".format(float(time.time())-self.startTime)
                currentTime = int(time.time())
                if currentTime != pastTime:
                    #currentTime = "{0:.2f}".format(float(time.time())-self.startTime)
                    currentTime = int(time.time())
                    pastTime = currentTime

                    writer.writerow([currentTime, self.rpm, self.soc, self.mcTemp, self.motorTemp, self.highMotorTemp, self.cellTemp, self.latitude, self.longitude, self.roll, self.pitch, self.gForce, self.bodyAccelx, self.bodyAccely, self.bodyAccelz, self.velx, self.vely, self.velz])
                                              
        self.exec()
                                                                                    
    @pyqtSlot(int)
    def rpm_write(self, value):
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
    def cellTemp_write(self, value):
        self.cellMotorTemp = value

    @pyqtSlot(float)
    def lat_write(self, value):
        self.latitude = value
        
    @pyqtSlot(float)
    def long_write(self, value):
        self.longititude = value
        
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
        
