"""------------------------------------------------------------------
 Description: BOLT III system state machine implementation
 Written for: BOLT Spring 2018
 Author: Alex Tsai, Chris Evers
 Notes: TODO(chrise92): Finish implementing the state transitions
---------------------------------------------------------------------
"""

class StateMachine(QThread):
	def __init__(self):
		super(stateMachine, self).__init__()

		"""Initialize state transition variables"""
		self.acc_on = false
		self.bms_de = true
		self.imd_ok = true
		self.pressure_ok = true
		self.ign_on = false
		self.start_button_pressed = false
		self.post_fault_occurred = false
		self.run_fault_occurred = false
		self.motor_enabled = false
		self.inverter_disabled = false

		self.current_state = 'IDLE'
		self.next_state = 'IDLE'

	def run(self):
		"""Checks conditions and determines next state"""
		print("State Machine Thread Started", self.currentThread())
		while(True):
			current_state = next_state
			if self.current_state == 'IDLE'

				if self.acc_on:
					self.next_state = 'ACC_ON'
				else:
					self.next_state = 'IDLE'
			elif self.current_state == 'ACC_ON':
				if self.ign_on:
					self.next_state = 'IGN_ON'
				else:
					self.next_state = 'ACC_ON'
			elif self.current_state == 'IGN_ON':
				if self.start_button_pressed:
					self.next_state = 'MOTOR_ENABLED'
				else:
					self.next_state = 'IGN_ON'
			elif self.current_state == 'MOTOR_ENABLED':
				if self.run_fault_occurred:
					self.next_state = 'INVERTER_DISABLED'
				else
					self.next_state = 'MOTOR_ENABLED'
			elif self.current_state == 'INVERTER_DISABLED'
				if not self.run_fault_occurred:
					self.next_state = 'ACC_ON'
				else:
					self.next_state = 'INVERTER_DISABLED'
