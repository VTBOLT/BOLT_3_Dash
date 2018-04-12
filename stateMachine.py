############################################################################################################
## Description: State machine for the startup process. Thread for reading from GPIO pins from the pi
## Written for: BOLT Senior Design Team
## Author: Alex Tsai
## Written: Spring 2018
## Notes
############################################################################################################

import RPi.GPIO as GPIO
from enum import Enum
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

ACC_SWITCH = 24
IGN_SWITCH = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(ACC_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IGN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class State(Enum):
	IDLE = 1
	ACCON = 2
	MCON = 3
	PRECHARGE = 4
	INVERTER = 5 #Probably will not need here since this is only reading GPIO
	MCFAULT = 6 #Probably will not need here since this is only reading GPIO
	IMDFAULT = 7 #Probably will not need here since this is only reading GPIO
	PRESSUREFAULT = 8 #Probably will not need here since this is only reading GPIO
	BMSFAULT = 9 #Probably will not need here since this is only reading GPIO
	ESTOP = 10 

class stateMachine(QThread):
	def __init__(self):
		self.currentState = State.IDLE
		QThread.__init__(self)
	def run(self):
		print("State Machine Thread Started", self.currentThread())
		print("Current State: IDLE")
		while(True):
			if self.currentState.name == State.IDLE:
				if GPIO.input(ACC_SWITCH):
					print("Current State: Accessory On") #will emit signal to a slot in dash.py when GUI is implemented
					self.currentState = State.ACCON
			elif self.currentState.name == State.ACCON:
				if GPIO.input(IGN_SWITCH):
					print("Current State: Motor Controller On") #will emit signal to a slot in dash.py when GUI is implemented
					self.currentState = State.MCON
			elif self.currentState.name == State.MCON:
				print("Current State: Pre-charge begins") #will emit signal to a slot in dash.py when GUI is implemented
				self.currentState = State.PRECHARGE
			elif self.currentState.name == State.PRECHARGE:
