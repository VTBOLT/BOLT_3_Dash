import sys
import time
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

#option to use fake data instaed of reading from gps
DEV = True #should default to False
if len(sys.argv) > 1:
    if any("-dev" in s for s in sys.argv):
        DEV = False

class GpsReader(QThread):
    #lastLapTime = pyqtSignal(int, int, int)
    #bestLapTime = pyqtSignal(int, int, int)
    currentLapTime = pyqtSignal(int, int, int)
    def __init__(self):
        QThread.__init__(self)
    def run(self):
        print("gps worker thread:", self.currentThread())
        current_min = 0
        current_sec = 0
        current_msec = 100
        if DEV:
            while True:
                time.sleep(.1)
                #self.lastLapTime.emit(last_min, last_sec, last_msec)
                self.currentLapTime.emit(current_min, current_sec, current_msec)
                #self.bestLapTime.emit(best_min, best_sec, best_msec)
                #print(current_min, current_sec, current_msec)

                if current_msec >= 999:
                    current_sec=current_sec+1
                    current_msec = 0
                elif current_sec > 60:
                    current_min=current_min+1
                    
                current_msec = current_msec+100
            self.processEvents()
        else:
            print("in gps reader")
        #ADD GPS READING HERE
        
        self.exec()
                                                                                    
