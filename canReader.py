############################################################################################################
## Description: Reads CAN data from standard out which canInterface wrote to std out, sends to gauges
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
## Notes
############################################################################################################

import os, sys
import time
import subprocess
import can
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

from args import Arg_Class

class CanReader(QThread):
    rpmUpdateValue = pyqtSignal(float)
    socUpdateValue = pyqtSignal(float)
    DCLUpdateValue = pyqtSignal(float)
    mcTempUpdateValue = pyqtSignal(float)
    motorTempUpdateValue = pyqtSignal(float)
    highMotorTempUpdateValue = pyqtSignal(float)
    highCellTempUpdateValue = pyqtSignal(float)
    lowCellTempUpdateValue = pyqtSignal(float)
    errorSignal = pyqtSignal(int, int, int, int)

    highMotorTemp = 0
    
    def __init__(self):
        self.highMotorTemp = 0.0
        QThread.__init__(self)
    def run(self):
        self.arguments = Arg_Class()
        if self.arguments.Args.dev:
            print("can worker thread:", self.currentThread())
            i = 1000
            j = 92.0
            k = 98.0
            m = 30.0
            highM = 0.0
            temp = 0
            self.socUpdateValue.emit(92)
            self.mcTempUpdateValue.emit(98)
            self.motorTempUpdateValue.emit(39)
            while True:
                time.sleep(.1)
                if i >= 8500:
                    i = 0
                    #self.errorSignal.emit(1,2,3,4)
                if j <= 0:
                    j = 99.0
                if k <= 0:
                    k = 93.0
                self.rpmUpdateValue.emit(i)
                #time.sleep(.001)
                i=i+100
                if temp > 50:
                    self.socUpdateValue.emit(j)
                    self.mcTempUpdateValue.emit(k)
                    self.motorTempUpdateValue.emit(m)
                    j=j-0.1
                    k = k+0.01
                    m = m+1
                    temp = 0
                temp=temp+1
                if m > highM:
                    highM = m
                if m > 40:
                    m = 10
                self.highMotorTempUpdateValue.emit(highM)
            self.processEvents()
        else:
            C = True # Flag for which can do use, python or c++, defualts to c++
            if C == True:
                os.system('sudo ifconfig can0 down')
                os.system('sudo ip link set can0 up type can bitrate 500000000')
                os.system('sudo ifconfig can0 txqueuelen 100')#sets buffer size
                os.system('sudo ifconfig can0 up')
                cmd = "/home/pi/BOLT_3_Dash/canInterface"
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                buf = ""
                for out in iter(lambda: p.stdout.read(1), ''):
                    if out.decode() != '\n':
                        buf = buf + str(out.decode())
                    else:
                        if buf.split(':')[0] == 'rpm':
                            rpm = buf.split(':')[1]
                            self.rpmUpdateValue.emit(float(rpm))
                        elif buf.split(':')[0] == 'soc':
                            soc = buf.split(':')[1]
                            self.socUpdateValue.emit(float(soc))
                        elif buf.split(':')[0] == 'DCL':
                            DCL = buf.split(':')[1]
                            self.DCLUpdateValue.emit(float(DCL))
                        elif buf.split(':')[0] == 'mcTemp':
                            mcTemp = buf.split(':')[1]
                            self.mcTempUpdateValue.emit(float(mcTemp))
                        elif buf.split(':')[0] == 'motorTemp':
                            motorTemp = buf.split(':')[1]
                            self.motorTempUpdateValue.emit(float(motorTemp))
                            #sets the highest temp
                            if float(motorTemp) > float(self.highMotorTemp):
                                self.highMotorTemp = motorTemp
                            self.highMotorTempUpdateValue.emit(float(self.highMotorTemp))
                        elif buf.split(':')[0] == 'highCellTemp':
                            highCellTemp = buf.split(':')[1]
                            self.highCellTempUpdateValue.emit(float(highCellTemp))
                        elif buf.split(':')[0] == 'lowCellTemp':
                            lowCellTemp = buf.split(':')[1]
                            self.lowCellTempUpdateValue.emit(float(lowCellTemp))
                        elif buf.split(':')[0] == 'states':
                            VSM_state = buf.split(':')[1]
                            inverter_state = buf.split(':')[2]
                            relay_state = buf.split(':')[3]
                            inverter_run_state = buf.split(':')[4]
                            inverter_cmd_state = buf.split(':')[5]
                            inverter_enable_state = buf.split(':')[6]
                            direction_state = buf.split(':')[7]
                        elif buf.split(':')[0] == 'ERROR':
                            post_lo_fault = buf.split(':')[1]
                            post_hi_fault = buf.split(':')[2]
                            run_lo_fault = buf.split(':')[3]
                            run_hi_fault = buf.split(':')[4]
                            self.errorSignal.emit(post_lo_fault, post_hi_fault, run_lo_fault, run_hi_fault)
                        #else:
                            #print("ERROR: Parsing missed:", buf)
                        buf = ""
            else:                
                #while True:                      
                    #sudo modprobe can
                    # Create a can network interface with a specific name
                    #sudo ip link add dev can0 type can
                    #sudo ip link set can0 up
                    #sudo ip link set can0 up type can bitrate 500000000 #5k bitrate
                    #sudo ifconfig can0 txqueuelen 100                    

                can_interface = 'can0'
                def producer(id):
                    bus = can.interface.Bus(can_interface, bustype='socketcan_native')
                producer(0x183)
                idFilterList = [{'rpm': 0xA5, 'can_mask': 0x11},
                                {'soc': 0x183, 'can_mask': 0x11}, 
                                {'cellTemp': 0x181, 'can_mask': 0x11}]  #in order RPM, SOC, highcellTemp
                              
                can0.set_filters(idFilterList) 

                while True:
                    message = can0.recv(0.0) # choose a timeout in seconds, 0.0 means non-blocking

                    if message is None: 
                        print('Timeout occured, no data from can bus.')
                    else:
                        
                        if message is idFilterList["rpm"]: #RPM

                            self.rpmUpdateValue.emit()

                        elif message is idFilterList["soc"]: #SOC
                            self.socUpdateValue.emit()

                        elif message is idFilterList["cellTemp"]: #highCellTemp
                            self.tempUpdateValue.emit()
            
        self.exec()
                                                                                    
