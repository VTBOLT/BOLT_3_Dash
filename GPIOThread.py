############################################################################################################
## Description: State machine for the startup process. Thread for reading from GPIO pins from the pi
## Written for: BOLT Senior Design Team
## Author: Alex Tsai
## Written: Spring 2018
## Notes
############################################################################################################

import RPi.GPIO as GPIO
import sys
from enum import Enum
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal, Qt

ACC_SWITCH = 24
IGN_SWITCH = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(ACC_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IGN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class State(Enum):
	IDLE = 0
	ACCON = 1
	MCON = 2
	PRECHARGE = 3
        PRECHARGE_DONE = 4
	ESTOP = 10

class GPIOThread(QThread):
        accessoryPress = pyqtSignal(int)
        ignitionPress = pyqtSignal(int)
        precharge = pyqtSignal(int)
        estop = pyqtSignal(int)
        raceMode = pyqtSignal()
	def __init__(self):
                self.ACC_FLAG = False
                self.IGN_FLAG = False
                self.vsmState = 0
		self.currentState = State.IDLE
		QThread.__init__(self)
	def run(self):
		print("State Machine Thread Started", self.currentThread())
		print("Current State: IDLE")
		while(True):
			if self.currentState.name == State.IDLE:
				if GPIO.input(ACC_SWITCH) and !(self.ACC_FLAG):
					print("Current State: Accessory On")
                                        self.accessoryPress.emit(1)
					self.currentState = State.ACCON
                                        self.ACC_FLAG = True
			elif self.currentState.name == State.ACCON:
				if GPIO.input(IGN_SWITCH) and !(self.IGN_FLAG):
					print("Current State: Motor Controller On") 
                                        self.ignitionPress.emit(2)
					self.currentState = State.MCON
                                        self.IGN_FLAG = True
			elif self.currentState.name == State.MCON:
				print("Current State: Pre-charge begins")
                                self.precharge.emit(3)
				self.currentState = State.PRECHARGE
                                print("Current State: Pre-charging")
			elif self.currentState.name == State.PRECHARGE and self.vsmState == 2:
                                if self.vsmState == 3:
                                    self.currentState == State.PRECHARGE_DONE
                        elif self.currentState.name == State.PRECHARGE_DONE
                                self.raceMode.emit()
       @pyqtSlot(int)
       def vsmUpdate(self, value):
           self.vsmState = value
