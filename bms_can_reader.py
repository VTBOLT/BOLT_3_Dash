import os, sys
import time
import subprocess
#import can


#os.system('sudo ifconfig vcan0 down')
#os.system('sudo ip link set vcan0 up type can bitrate 500000000')
#os.system('sudo ifconfig vcan0 txqueuelen 100')
#os.system('sudo ifconfig vcan0 up')	

#cmd = "/home/$USER/BOLT_3_Dash/canInteface"
cmd = "/home/$USER/Desktop/BOLT/BOLT_3_Dash/canInterface"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
buf = ""
for out in iter(lambda: p.stdout.read(1), ''):
	if out.decode() != '\n':
		buf = buf + str(out.decode())
	else:
		if buf.split(':')[0] == 'bms':
			bms = buf.split(':')[1]
			# signifies BMS message was received
			#os.system('cansend vcan0 123#deadbeef')
			print("Request found")


