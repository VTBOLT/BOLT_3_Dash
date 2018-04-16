############################################################################################################
## Description: State machine for the startup process. Thread for reading from GPIO pins from the pi
## Written for: BOLT Senior Design Team
## Author: Alex Tsai
## Written: Spring 2018
## Notes
############################################################################################################

import RPi.GPIO as GPIO
import sys, time
from enum import Enum
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal, Qt
from stateMachine import StateMachine as states

ACC_SWITCH = 24
IGN_SWITCH = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(ACC_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IGN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class GPIOThread(QThread):
        accessoryPress = pyqtSignal(int)
        ignitionPress = pyqtSignal(int)
        #estop = pyqtSignal(int)
	def __init__(self):
                self.ACC_FLAG = False
                self.IGN_FLAG = False
		QThread.__init__(self)
	def run(self):
		print("GPIO Thread Started", self.currentThread())
		while(True):
			if states.current_state == 'IDLE':
				if GPIO.input(ACC_SWITCH) and !(self.ACC_FLAG):
                                        self.accessoryPress.emit(1)
                                        self.ACC_FLAG = True
				elif not GPIO.input(ACC_SWITCH) and self.ACC_FLAG:
					self.accessoryPress.emit(0)
					self.ACC_FLAG = False
			elif states.current_state == 'ACC_ON':
				if GPIO.input(IGN_SWITCH) and !(self.IGN_FLAG):
                                        self.ignitionPress.emit(1)
                                        self.IGN_FLAG = True
				elif not GPIO.input(IGN_SWITCH) and self.IGN_FLAG:
					self.ignitionPress.emit(0)
					self.IGN_FLAG = False
			time.sleep(.1)
			#elif self.currentState.name == State.PRECHARGE and self.vsmState == 2:
                                #if self.vsmState == 3:
                                    #self.currentState == State.PRECHARGE_DONE
                        #elif self.currentState.name == State.PRECHARGE_DONE
                                #self.raceMode.emit()
		self.exec()
       #@pyqtSlot(int)
       #def vsmUpdate(self, value):
           #self.vsmState = value
