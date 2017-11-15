import sys
import time
import subprocess

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

from args import Arg_Class

class CanReader(QThread):
    rpmUpdateValue = pyqtSignal(int)
    socUpdateValue = pyqtSignal(float)
    mcTempUpdateValue = pyqtSignal(float)
    motorTempUpdateValue = pyqtSignal(float)
    highMotorTempUpdateValue = pyqtSignal(float)
    cellTempUpdateValue = pyqtSignal(float)
    errorSignal = pyqtSignal()

    highMotorTemp = 0
    
    def __init__(self):
        QThread.__init__(self)
    def run(self):
        self.arguments = Arg_Class()
        if self.arguments.Args.dev:
            print("can worker thread:", self.currentThread())
            i = 0
            j = 98.0
            k = 98.0
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
                self.mcTempUpdateValue.emit(k)
                i=i+10
                j=j-0.1
                k = k+0.01
            self.processEvents()
        else:
            #ALTERNATE METHOD
            cmd = "./canreader"
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            buf = ""
            for out in iter(lambda: p.stdout.read(1), ''):
                if out.decode() != '\n':
                    buf = buf + str(out.decode())
                else:
                    if buf.split(":")[0] == 'rpm':
                        rpm = buf.split(':')[1]
                        self.rpmUpdateValue.emit(float(rpm))
                    elif buf.split(":")[0] == 'soc':
                        soc = buf.split(':')[1]
                        self.socUpdateValue.emit(float(soc))
                    elif buf.split(":")[0] == 'mcTemp':
                        mcTemp = buf.split(':')[1]
                        self.mcTempUpdateValue.emit(float(mcTemp))
                    elif buf.split(":")[0] == 'motorTemp':
                        motorTemp = buf.split(':')[1]
                        self.motorTempUpdateValue.emit(float(motorTemp))
                        #sets the highest temp
                        if motorTemp > highMotorTemp:
                            highMotorTemp = motorTemp
                        self.highMotorTempUpdateValue.emit(float(highMotorTemp))                        
                    elif buf.split(":"[0] == 'highCellTemp'):
                        cellTemp = buf.split(':')[1]
                        self.cellTempUpdateValue.emit(float(cellTemp))
                    else:
                        print("ERROR: Parsing missed:", buf)
                    buf = ""
        

            
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
                                                                                    
