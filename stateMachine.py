"""------------------------------------------------------------------
 Description: BOLT III system state machine implementation
 Written for: BOLT Spring 2018
 Authors: Alex Tsai, Chris Evers
 Notes: TODO(chrise92): Finish implementing the state transitions
---------------------------------------------------------------------
"""
import os, sys
import time
import subprocess
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from args import Arg_Class

class StateMachine(QThread):
	idle_signal = pyqtSignal(int)
	acc_on_signal = pyqtSignal(int)
	ign_on_signal = pyqtSignal(int)
	motor_enabled_signal = pyqtSignal(int)
	inverter_disabled_signal = pyqtSignal(int)

	def __init__(self):
		"""Initialize state transition variables"""
		self.acc_on = False
		self.bms_de = True
		self.imd_ok = True
		self.pressure_ok = True
		self.ign_on = False
		self.start_button_pressed = False
		self.post_fault_occurred = False
		self.run_fault_occurred = False
		self.motor_enabled = False
		self.inverter_disabled = False

		self.current_state = 'IDLE'
		self.next_state = 'IDLE'

		QThread.__init__(self)

	def run(self):
		"""Checks conditions and determines next state"""
		print("State Machine Thread Started", self.currentThread())
		self.current_state = self.next_state
		while True:
			self.current_state = self.next_state
			if self.current_state == 'IDLE':
				self.start_button_pressed = False
				self.idle_signal.emit(1)
				if self.acc_on:
					self.next_state = 'ACC_ON'
				else:
					self.next_state = 'IDLE'
			elif self.current_state == 'ACC_ON':
				self.start_button_pressed = False
				self.acc_on_signal.emit(1)
				if not self.acc_on:
					self.ign_on = False
					self.next_state = 'IDLE'
				elif self.ign_on:
					self.next_state = 'IGN_ON'
				else:
					self.next_state = 'ACC_ON'
			elif self.current_state == 'IGN_ON':
				self.ign_on_signal.emit(1)
				if not self.acc_on:
					self.ign_on = False
					self.next_state = 'IDLE'
				elif not self.ign_on:
					self.next_state = 'ACC_ON'
				elif self.start_button_pressed:
					self.next_state = 'MOTOR_ENABLED'
				else:
					self.next_state = 'IGN_ON'
			elif self.current_state == 'MOTOR_ENABLED':
				self.motor_enabled_signal.emit(1)
				if not self.acc_on:
					self.ign_on = False
					self.next_state = 'IDLE'
				elif not self.ign_on:
					self.next_state = 'ACC_ON'
				elif self.run_fault_occurred:
					self.next_state = 'INVERTER_DISABLED'
				else:
					self.next_state = 'MOTOR_ENABLED'
			elif self.current_state == 'INVERTER_DISABLED':
				self.inverter_disabled_signal.emit(1)
				if not self.run_fault_occurred:
					self.next_state = 'ACC_ON'
				else:
					self.next_state = 'INVERTER_DISABLED'
			time.sleep(.1)
		self.exec()

	@pyqtSlot(int)
	def updateACC_ON(self, value):
		self.acc_on = value

	@pyqtSlot(int)
	def updateBMS_DE(self, value):
		self.bms_de = value

	@pyqtSlot(int)
	def updateIMD_OK(self, value):
		self.imd_ok = value

	@pyqtSlot(int)
	def updatePRESSURE_OK(self, value):
		self.pressure_ok = value

	@pyqtSlot(int)
	def updateIGN_ON(self, value):
		self.ign_on = value

	@pyqtSlot(int)
	def updateSTART_BUTTON(self, value):
		self.start_button_pressed = value

	@pyqtSlot(int)
	def updatePOST_FAULT(self, value):
		if value:
			self.post_fault_occurred = True
		else:
			self.post_fault_occurred = False

	@pyqtSlot(int)
	def updateRUN_FAULT(self, value):
		if value:
			self.run_fault_occurred = True
		else:
			self.run_fault_occurred = False

	@pyqtSlot(int)
	def updateMOTOR_ENABLED(self, value):
		if value:
			self.motor_enabled = True
		else:
			self.motor_enabled = False

	@pyqtSlot(int)
	def updateINVERTER_DISABLED(self, value):
		if value:
			self.inverter_disabled = True
		else:
			self.inverter_disabled = False
