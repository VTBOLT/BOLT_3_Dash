# Reads from the CAN bus and writes values to corresponding objects
# Written for: BOLT Senior Design Team
# Author: Khang Lieu
# Written: Fall 2018


class CanReader

    bool abort

    int soc

    def __init__(self):
    

    def initialize(self):

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

        while(this.abort == true)

    def openPort(self,int port):
    
    def max(a, b, c, d):
        int max = 0
        if(a >= max)
            max = a
        else if(b >= max)
            max = b
        else if(c >= max)
            max = c
        else if(d >= max)
            max = d
        return max
