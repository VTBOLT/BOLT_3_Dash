import sys
import time
from datetime import datetime as dt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

class FileWriter(QWidget):
    def __init__(self, parent):
        super(FileWriter, self).__init__(parent)
        
        filename = 'dash_log_'+str(dt.now().year)+'_'+str(dt.now().month)+'_'+str(dt.now().day)+'_'+str(dt.now().hour)+'_'+str(dt.now().minute)

        self.f = open('/home/vbox/logs/'+filename, 'w')
        
    @pyqtSlot(float)
    def rpm_write(self, value):
        self.f.write("rpm, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float)
    def soc_write(self, value):
        self.f.write("soc, "+str(time.time())+', '+str(value)+'\n')

    ## tempatures
    @pyqtSlot(float)
    def mcTemp_write(self, value):
        self.f.write("mcTemp, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float)
    def motorTemp_write(self, value):
        self.f.write("motorTemp, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float)
    def cellTemp_write(self, value):
        self.f.write("cellTemp, "+str(time.time())+', '+str(value)+'\n')

    ## GPS values
    @pyqtSlot(float)
    def lat_write(self, value):
        self.f.write("lat, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float)
    def long_write(self, value):
        self.f.write("long, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float)
    def roll_write(self, value):
        self.f.write("roll, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float)
    def pitch_write(self, value):
        self.f.write("pitch, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float)
    def gForce_write(self, value):
        self.f.write("gForce, "+str(time.time())+', '+str(value)+'\n')
    @pyqtSlot(float, float, float)
    def accel_write(self, x, y, z):
        self.f.write("accelerometer, "+str(time.time())+', '+str(x)+', '+str(y)+', '+str(z)+'\n')
    @pyqtSlot(float, float, float)
    def gyro_write(self, x, y, z):
        self.f.write("gyroscope, "+str(time.time())+', '+str(x)+', '+str(y)+','+str(z)+'\n')
    @pyqtSlot(float, float, float)
    def vel_write(self, x, y, z):
        self.f.write("velocity, "+str(time.time())+', '+str(x)+', '+str(y)+','+str(z)+'\n')
