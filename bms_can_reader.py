import os, sys
import time
import subprocess
#import can
# cansend can0 7EB#100843030AFA0AC0

#os.system('sudo ifconfig can0 down')
#os.system('sudo ip link set can0 up type can bitrate 500000000')
#os.system('sudo ifconfig can0 txqueuelen 100')
#os.system('sudo ifconfig can0 up')	

cmd = "/home/$USER/BOLT_3_Dash/canInterface"
#cmd = "/home/$USER/Desktop/BOLT/BOLT_3_Dash/canInterface"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
buf = ""
for out in iter(lambda: p.stdout.read(1), ''):
	if out.decode() != '\n':
		buf = buf + str(out.decode())
		#print(buf)
	elif out.decode() == '\n':
		if buf.split(':')[0] == 'bms':
			bms = buf.split(':')[1]
			# signifies BMS message was received
			#os.system('cansend vcan0 123#deadbeef')
			print("Request found")
		buf=''

                


