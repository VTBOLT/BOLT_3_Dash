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

IGN_SWITCH = 26
DASH_IMD = 19
DASH_PRES = 16
DASH_BMSDE = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(ACC_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IGN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DASH_IMD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DASH_PRES, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DASH_BMSDE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class GPIOThread(QThread):
        ignSignal = pyqtSignal(int)
	imdSignal = pyqtSignal(int)
	presSignal = pyqtSignal(int)
	bmsdeSignal = pyqtSignal(int)
        #estop = pyqtSignal(int)
	def __init__(self):
                self.IGN_FLAG = False
		self.IMD_FLAG = False
		self.PRES_FLAG = False
		self.BMSDE_FLAG = False
		QThread.__init__(self)
	def run(self):
		print("GPIO Thread Started", self.currentThread())
		while(True):
			if GPIO.input(IGN_SWITCH) and !(self.IGN_FLAG):
				print("IGN_SWITCH ON")
                        	self.ignSignal.emit(1)
                        	self.IGN_FLAG = True
			elif not GPIO.input(IGN_SWITCH) and self.IGN_FLAG:
				print("IGN_SWITCH OFF")
				self.ignSignal.emit(0)
				self.IGN_FLAG = False
			if GPIO.input(DASH_IMD) and !(self.IMD_FLAG):
				print("DASH_IMD ON")
				self.imdSignal.emit(1)
				self.IMD_FLAG = True
			elif not GPIO.input(DASH_IMD) and self.IMD_FLAG):
				print("DASH_IMD OFF")
				self.imdSignal.emit(0)
				self.IMD_FLAG = False
			if GPIO.input(DASH_PRES) and !(self.PRES_FLAG):
				print("DASH_PRES ON")
				self.presSignal.emit(1)
				self.PRES_FLAG = True
			elif not GPIO.input(DASH_PRES) and self.PRES_FLAG):
				print("DASH_PRES OFF")
				self.presSignal.emit(0)
				self.PRES_FLAG = False
			if GPIO.input(DASH_BMSDE) and !(self.BMSDE_FLAG):
				print("DASH_BMSDE ON")
				self.bmsdeSignal.emit(1)
				self.BMSDE_FLAG = True
			elif not GPIO.input(DASH_BMSDE) and self.BMSDE_FLAG):
				print("DASH_BMSDE OFF")
				self.bmsdeSignal.emit(0)
				self.BMSDE_FLAG = False
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
