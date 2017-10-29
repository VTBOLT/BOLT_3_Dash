import sys
import time
import subprocess
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

#option to use fake data instaed of reading from gps
DEV = True #should default to False
if len(sys.argv) > 1:
    if any("-dev" in s for s in sys.argv):
        DEV = False

class GpsReader(QThread):

    currentLapTimeValue = pyqtSignal(int, int, int)

    latValue = pyqtSignal(float)
    longValue = pyqtSignal(float)
    rollValue = pyqtSignal(float)

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
                self.currentLapTimeValue.emit(current_min, current_sec, current_msec)
                latitude = 0.0
                longitude = 0.0
                roll = 90.0 # degrees
                self.latValue.emit(latitude)
                self.longValue.emit(longitude)
                self.rollValue.emit(roll)
                
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
            print("Reading from GPS")
            #This runs a .c executable which writes to std-out,
            #subprocess reads from that
            #should use boost or embedding and exending

            cmd = './spatialReader'
            MESSAGE_LENGTH = 100
            #need to add error checking to make sure the executable exitsts
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            for out in iter(lambda: p.stdout.read(MESSAGE_LENGTH), ''):
                    print(out.split(':'))
                    '''
                if out.split(':')[0] == 'lat':
                    print(out.split(':'))
                    latitude = out.split(':')[1]
                    self.latValue.emit(latitude)
                elif out.split(':')[0] == 'long':
                    longitude = out.split(':')[1]
                    self.longValue.emit(longitude)
                elif out.split(':')[0] == 'roll':
                    roll = out.split(':')[1]
                    self.rollValue.emit(roll)
                '''
        self.exec()
                                                                                    
