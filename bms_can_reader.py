import os, sys
import time
import subprocess
#import can

class BmsCanReader():
	def __init__(self):
        	#todo
		x = 1
	def run(self):
		os.system('sudo ifconfig can0 down')
		os.system('sudo ip link set can0 up type can bitrate 500000000')
		os.system('sudo ifconfig can0 txqueuelen 100')
		os.system('sudo ifconfig can0 up')	

		cmd = "/home/$USER/BOLT_3_Dash/canInteface"
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		buf = ""
		for out in iter(lamda in p.stdout.read(1), ''):
			if out.decode() != '\n':
				buf = buf + str(out.decode())
			else:
				if buf.split(':')[0] == 'bms':
					bms = buf.split(':')[1]
					# signifies BMS message was received
					os.system('cansend can0 123#deadbeef')
	
