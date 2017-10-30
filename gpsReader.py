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
        latitude = 1.0
        longitude = 0.0
        roll = 90.0 # degrees
        if DEV:
            while True:
                time.sleep(.1)
                self.currentLapTimeValue.emit(current_min, current_sec, current_msec) 
                self.latValue.emit(latitude)
                self.longValue.emit(longitude)
                self.rollValue.emit(roll)
                
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

            cmd = './spatialReader'
            MESSAGE_LENGTH = 100
            #need to add error checking to make sure the executable exitsts
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            #for out in iter(lambda: p.stdout.read(MESSAGE_LENGTH), '\n'):
            for out in iter(lambda: p.stdout.read(1), ''):
                #print(out.decode().split(':')) 
                if out.decode().split(':')[0] == 'lat':#spits identifier from string, .decode() convers from bytes to string
                    print(out.decode().split(':')[1])
                    latitude = out.decode().split(':')[1]
                    self.latValue.emit(float(latitude))
                elif out.decode().split(':')[0] == 'long':
                    longitude = out.decode().split(':')[1]
                    self.longValue.emit(float(longitude))
                elif out.decode().split(':')[0] == 'roll':
                    print("roll:", out.decode().split(':')[1])
                    roll = out.decode().split(':')[1]
                    self.rollValue.emit(float(roll))
                
        self.exec()
                                                                                    
