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
            self.processEvents()
        else:
            print("in can reader")
            #ADD CAN READING HERE
            #while True:
            '''          
            sudo modprobe can
            # Create a can network interface with a specific name
            sudo ip link add dev can0 type can
            sudo ip link set can0 up
            sudo ip link set can0 up type can bitrate 500000000 #5k bitrate
            #sudo ifconfig can0 txqueuelen 100

            import can
            can_interface = 'can0'
            bus = can.interface.Bus(can_interface, bustype='socketcan_native')

            idFilterList = [{'can_id': 0xA5, 'can_mask': 0x11},
                            {'can_id': 0x183, 'can_mask': 0x11}, 
                            {'can_id': 0x181, 'can_mask': 0x11}]  #in order RPM, SOC, highcellTemp
                          
            can0.set_filters(idFilterList) 

            while True:
                message = can0.recv(0.0) # choose a timeout in seconds, 0.0 means non-blocking

                if message is None: 
                    print('Timeout occured, no data from can bus.')
                else:
                    
                    if message is idFilterList["can_id"]: #RPM

                        self.rpmUpdateValue.emit()

                    elif message is idFilterList["can_id"]: #SOC
                        self.socUpdateValue.emit()

                    elif message is idFilterList["can_id"]: #highCellTemp
                        self.tempUpdateValue.emit()
                
            '''                        

        self.exec()
                                                                                    
