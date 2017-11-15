import sys
import time
import csv
from datetime import datetime as dt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt
from args import Arg_Class

class FileWriter(QWidget):
    def __init__(self, parent):
        super(FileWriter, self).__init__(parent)
        arguments = Arg_Class()
        
        if arguments.Args.log:
            ## Creates unique file name
            filename = 'dash_log_'+str(dt.now().year)+'_'+str(dt.now().month)+'_'+str(dt.now().day)+'_'+str(dt.now().hour)+'_'+str(dt.now().minute)

            ## Opens file for logging
            self.f = open('/home/vbox/logs/'+filename, 'w')

            #setup time to start from zero
            self.startTime = time.time()
            currentTime = time.time()-self.startTime        


    
    ######## Logging Slots ######    
    @pyqtSlot(float)
    def rpm_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("rpm, "+str(currentTime)+', '+str(value)+'\n')
    @pyqtSlot(float)
    def soc_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("soc, "+str(currentTime)+', '+str(value)+'\n')

    ## tempatures
    @pyqtSlot(float)
    def mcTemp_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("mcTemp, "+str(currentTime)+', '+str(value)+'\n')
    @pyqtSlot(float)
    def motorTemp_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("motorTemp, "+str(currenTime)+', '+str(value)+'\n')
    @pyqtSlot(float)
    def cellTemp_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("cellTemp, "+str(currentTime)+', '+str(value)+'\n')

    ## GPS values
    @pyqtSlot(float)
    def lat_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("lat, "+str(currentTime)+', '+str(value)+'\n')
    @pyqtSlot(float)
    def long_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("long, "+str(currentTime)+', '+str(value)+'\n')
    @pyqtSlot(float)
    def roll_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("roll, "+str(currentTime)+', '+str(value)+'\n')
    @pyqtSlot(float)
    def pitch_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("pitch, "+str(currentTime)+', '+str(value)+'\n')
    @pyqtSlot(float)
    def gForce_write(self, value):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("gForce, "+str(currentTime)+', '+str(value)+'\n')
    @pyqtSlot(float, float, float)
    def bodyAccel_write(self, x, y, z):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("body_accelerometer, "+str(currentTime)+', '+str(x)+', '+str(y)+', '+str(z)+'\n')
    @pyqtSlot(float, float, float)
    def vel_write(self, x, y, z):
        currentTime = '{0:.4f}'.format(float(time.time())-float(self.startTime))
        self.f.write("velocity, "+str(currentTime)+', '+str(x)+', '+str(y)+','+str(z)+'\n')
