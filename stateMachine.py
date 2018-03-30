"""------------------------------------------------------------------
 Description: BOLT III system state machine implementation
 Written for: BOLT Spring 2018
 Author: Alex Tsai, Chris Evers
 Notes: TODO(chrise92): Finish implementing the state transitions
---------------------------------------------------------------------
"""

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

class StateMachine(QThread):

	idle_state = pyqtSignal(int)
	acc_on_state = pyqtSignal(int)
	ign_on_state = pyqtSignal(int)
	motor_enabled_state = pyqtSignal(int)
	inverter_disabled_state = pyqtSignal(int)

	def __init__(self):
		QThread.__init__(self)

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

	def run(self):
		"""Checks conditions and determines next state"""
		print("State Machine Thread Started", self.currentThread())
		self.current_state = self.next_state
		if self.current_state == 'IDLE':
			print("In IDLE state...")
			self.idle_state.emit(1)
			if self.acc_on:
				self.next_state = 'ACC_ON'
			else:
				self.next_state = 'IDLE'
		elif self.current_state == 'ACC_ON':
			print("In ACC_ON state...")
			self.acc_on_state.emit(1)
			if self.ign_on:
				self.next_state = 'IGN_ON'
			else:
				self.next_state = 'ACC_ON'
		elif self.current_state == 'IGN_ON':
			self.ign_on_state.emit(1)
			if self.start_button_pressed:
				self.next_state = 'MOTOR_ENABLED'
			else:
				self.next_state = 'IGN_ON'
		elif self.current_state == 'MOTOR_ENABLED':
			self.motor_enabled_state.emit(1)
			if self.run_fault_occurred:
				self.next_state = 'INVERTER_DISABLED'
			else:
				self.next_state = 'MOTOR_ENABLED'
		elif self.current_state == 'INVERTER_DISABLED':
			self.inverter_disabled_state.emit(1)
			if not self.run_fault_occurred:
				self.next_state = 'ACC_ON'
			else:
				self.next_state = 'INVERTER_DISABLED'
		self.current_state = self.next_state

		self.exec()

	@pyqtSlot(int)
	def updateACC_ON(self, value):
		print("Updating acc_on value...")
		if value:
			self.acc_on = True
		else:
			self.acc_on = False
		self.run()

	@pyqtSlot(int)
	def updateBMS_DE(self, value):
		if value:
			self.bms_de = True
		else:
			self.bmd_de = False
		self.run()

	@pyqtSlot(int)
	def updateIMD_OK(self, value):
		if value:
			self.imd_ok = True
		else:
			self.imd_ok = False
		self.run()

	@pyqtSlot(int)
	def updatePRESSURE_OK(self, value):
		if value:
			self.pressure_ok = True
		else:
			self.pressure_ok = False
		self.run()

	@pyqtSlot(int)
	def updateIGN_ON(self, value):
		if value:
			self.img_on = True
		else:
			self.img_on = False
		self.run()

	@pyqtSlot(int)
	def updateSTART_BUTTON(self, value):
		if value:
			self.start_button_pressed = True
		else:
			self.start_button_pressed = False
		self.run()

	@pyqtSlot(int)
	def updatePOST_FAULT(self, value):
		if value:
			self.post_fault_occurred = True
		else:
			self.post_fault_occurred = False
		self.run()

	@pyqtSlot(int)
	def updateRUN_FAULT(self, value):
		if value:
			self.run_fault_occurred = True
		else:
			self.run_fault_occurred = False
		self.run()

	@pyqtSlot(int)
	def updateMOTOR_ENABLED(self, value):
		if value:
			self.motor_enabled = True
		else:
			self.motor_enabled = False
		self.run()

	@pyqtSlot(int)
	def updateINVERTER_DISABLED(self, value):
		if value:
			self.inverter_disabled = True
		else:
			self.inverter_disabled = False
		self.run()
