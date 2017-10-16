import sys
import time
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

DEV = True
if len(sys.argv) > 1:
    if sys.argv[1] == '-d':
        DEV = True
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
            i = 1
            j = 99.0
            k = 93.0
            while True:
                time.sleep(.5)
                if i >= 100:
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
                i=i+1
                j=j-1
                k = k+.01
        #else:
            #while True:
                
                    
        self.processEvents()
        self.exec()
                                                                                    
