# Reads from the CAN bus and writes values to corresponding objects
# Written for: BOLT Senior Design Team
# Author: Khang Lieu
# Written: Fall 2018

import can
import socket
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0'
can.rc['bitrate'] = 500000
from can.interface import Bus

bus = Bus()



class CanReader():

    abort = False

    soc = 0

    def __init__(self):
        self.abort = False
        self.run()



    def run(self):

        RPM = 0
        SOC = 0
        DCL = 0
        mtrTemp = 0
        moduleA = 0
        moduleB = 0
        moduleC = 0
        gateDrvrBrd = 0
        highCellTemp = 0
        lowCellTemp = 0
        post_lo_fault = 0
        post_hi_fault = 0
        run_lo_fault = 0
        run_hi_fault = 0

        VSM_state = 0
        inverter_state = 0
        relay_state = 0
        inverter_run_state = 0
        inverter_cmd_state = 0
        inverter_enable_state = 0
        direction_state = 0

        while 1:
            for msg in bus:
                print(type(msg))
                if(msg.arbitration_id == 0xA0):
                    #MC Temperatures
                    print(msg.data)
                if(msg.arbitration_id == 0xA2):
                    #MC Temperatures
                    print(msg.data)

                if(msg.arbitration_id == 0xA5):
                    #Motor Position
                    print(msg.data)

                if(msg.arbitration_id == 0x180):
                    #BMS Voltages
                    #High low cell data
                    print(msg.data)

                if(msg.arbitration_id == 0x181):
                    #BMS Temperatures
                    print(msg.data)

                if(msg.arbitration_id == 0x182):
                    #BMS Isolations
                    print(msg.data)

                if(msg.arbitration_id == 0x111):
                    #BMS DCL
                    print(msg.data)

                if(msg.arbitration_id == 0x183):
                    #BMS Information
                    print(msg.data)

                if(msg.arbitration_id == 0xAA):
                    #Internal State of MC
                    print(msg.data)

                if(msg.arbitration_id == 0xAB):
                    #MC Errors
                    print(msg.data)


       



    def max(self,a, b, c, d):
        max = 0
        if(a >= max):
            max = a
        elif(b >= max):
            max = b
        elif(c >= max):
            max = c
        elif(d >= max):
            max = d
        return max


CanReader()
