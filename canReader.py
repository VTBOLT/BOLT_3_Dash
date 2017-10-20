import sys
import time
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
#option to use fake data instead of reading from can bus
DEV = True #should default to False
if len(sys.argv) > 1:
    if any("-dev" in s for s in sys.argv):
       DEV = False

class CanReader(QThread):
    rpmUpdateValue = pyqtSignal(int)
    socUpdateValue = pyqtSignal(float)
    tempUpdateValue = pyqtSignal(float)
    errorSignal = pyqtSignal()
    def __init__(self):
        QThread.__init__(self)
    def run(self):
        if DEV:
            print("can worker thread:", self.currentThread())
            i = 0
            j = 99.0
            k = 93.0
            while True:
                time.sleep(.1)
                if i >= 8000:
                    i = 0
                    self.errorSignal.emit()
                if j <= 0:
                    j = 99.0
                if k <= 0:
                    k = 93.0
                self.rpmUpdateValue.emit(i)
                time.sleep(.001)
                self.socUpdateValue.emit(j)
                self.tempUpdateValue.emit(k)
                i=i+100
                j=j-0.1
                k = k+0.01
            self.processEvents()
        else:
            print("in can reader")
            #ADD CAN READING HERE
            #while True:
                
                    

        self.exec()
                                                                                    
