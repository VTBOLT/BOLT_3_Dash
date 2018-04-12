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

class TestThread(QThread):
    rpmUpdateValue = pyqtSignal(float)

    def __init__(self):

        self.exitFlag = False
        self.socValue = 0.0
        self.rpmValue = 0.0
        self.mcTempValue = 0.0
        self.motorTempValue = 0.0
        self.highCellTempValue = 0.0
        self.lowCellTempValue = 0.0
        self.DCLValue = 0.0
        self.ErrorValue = ""

        QThread.__init__(self)
    def run(self):
        self.arguments = Arg_Class()
        #self.highMotorTempUpdateValue.emit(highM)

        while self.exitFlag == False:
            print("running11")
            print("Testing interface for BOLT 3 Dash:")
            print("   1. Test canReader.py")
            print("   2. Test gpsReader.py")
            print("   3. Test GPIO interface")
            print("   4. Run Dash.py")
            print("   5. Test fileWriter")
            print("   6. Exit")
            userInput = input("   Enter option: ")
        
            if userInput == '1':
                print("Starting CAN thread")
                # setup vcan interface

                os.system('sudo modprobe vcan')#use subprocess to supress error output
                os.system('sudo ip link add name vcan0 type vcan')
                os.system('sudo ip link set up vcan0')
                
                #os.system('cansend vcan0 123#deadbeef')# properly formated can message
                #subprocess.call(['gnome-terminal', '-x', '/home/vbox/BOLT_3_Dash_V3/canInterface'])
                #os.system('sudo /home/vbox/BOLT_3_Dash_V3/canInterface')
                print("Sending: mcTemp Value: 3")
                time.sleep(0.5)
                os.system('cansend vcan0 0A0#1E.00.0B.00.0C.00.0D.00')
                print("Sending: motorTemp Value: 3")
                time.sleep(0.5)
                os.system('cansend vcan0 0A2#63.00.63.00.1E.00.63.00')
                print("Sending: rpm Value: 3")
                time.sleep(0.5)
                os.system('cansend vcan0 0A5#63.00.03.00.63.00.63.00')
                print("Sending: highCellTemp Value: 3")
                time.sleep(0.5)
                os.system('cansend vcan0 181#63.1E.00.00.0F.00.63.00')
                print("Sending: DCL Value: 3")
                time.sleep(0.5)
                os.system('cansend vcan0 111#03.00.63.00.63.00.63.00')
                print("Sending: SOC Value: 3")
                time.sleep(0.5)
                os.system('cansend vcan0 183#63.00.63.00.06.00.63.00')
                print("Sending: MCStates Value: 1:2:3:4:5:6:7")
                time.sleep(0.5)
                os.system('cansend vcan0 0AA#01.00.02.03.04.05.06.07')
                print("Sending: Error Value: 1:2:3:4")
                time.sleep(0.5)
                os.system('cansend vcan0 0AB#01.00.02.00.03.00.04.00')
                time.sleep(1)
                
                failureCount = 0
                if self.rpmValue != 3:
                    print(self.rpmValue)
                    print("Error: rpm", self.rpmValue)
                    failureCount+=1
                if self.socValue != 3:
                    print("Error: soc", self.socValue)
                    failureCount+=1
                if self.mcTempValue != 3:
                    print("Error: mcTemp", self.mcTempValue)
                    failureCount+=1
                if self.motorTempValue != 3:
                    print("Error: motorTemp", self.motorTempValue)
                    failureCount+=1
                if self.highCellTempValue != 3:
                    print("Error: highCellTemp", self.highCellTempValue)
                    failureCount+=1
                if self.lowCellTempValue != 1:
                    print("Error: lowCellTemp", self.lowCellTempValue)
                    failureCount+=1
                if self.DCLValue != 3:
                    print("Error: DCL", self.DCLValue)
                    failureCount+=1
                if self.ErrorValue != "1234":
                    print(self.ErrorValue)
                    print("Error: error codes")
                    failureCount+=1
                if failureCount == 0:
                    print("\n\nSucess: All tests passed")
                else:
                    print("\n\nFailure:", failureCount, "tests failed")
            elif userInput == '2':
                print("GPS")
            elif userInput == '3':
                print("GPIO")
            elif userInput == '4':
                print("Dash")
            elif userInput == '5':
                print("file")
            elif userInput == '6':
                print("Exiting- this option doesn't work yet")
            #self.exec()
    @pyqtSlot(float)
    def soc_check(self, value):
        self.socValue = value

    @pyqtSlot(float)
    def rpm_check(self, value):
        self.rpmValue = value
    @pyqtSlot(float)
    def mcTemp_check(self, value):
        self.mcTempValue = value
    @pyqtSlot(float)
    def motorTemp_check(self, value):
        self.motorTempValue = value
    @pyqtSlot(float)
    def highCellTemp_check(self, value):
        self.highCellTempValue = value
    @pyqtSlot(float)
    def lowCellTemp_check(self, value):
        self.lowCellTempValue = value
    @pyqtSlot(float)
    def DCL_check(self, value):
        self.DCLValue = value
    @pyqtSlot(int,int,int,int)
    def Error_check(self, v1,v2,v3,v4):
        self.ErrorValue = str(v1)+str(v2)+str(v3)+str(v4)


    


            
