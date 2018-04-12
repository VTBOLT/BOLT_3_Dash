#!/usr/bin/env python

############################################################################################################
## Description: starts all threads, creates connections between signals and slots
## Threads: dash, can, gps, and filewritter threads
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
## Notes:
############################################################################################################

import sys

from PyQt5.QtWidgets import QApplication
from dash import Dash
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug
from args import Arg_Class
from fileWriter import FileWriter
from testThread import TestThread

if __name__ == '__main__':
    app = QApplication(sys.argv)
    arguments = Arg_Class()
    dash = Dash()
    print("Dash thread started:", app.instance().thread())
    if arguments.Args.fullscreen:
        dash.showFullScreen()
    else:
        dash.show()
        
    if arguments.Args.canoff == True:
        canWorker =CanReader()
        canWorker.start()

        canWorker.rpmUpdateValue.connect(dash.rpmGauge.rpm_update)
        canWorker.socUpdateValue.connect(dash.socGauge.soc_update)
        canWorker.DCLUpdateValue.connect(dash.errorGauge.DCL_update)

        canWorker.mcTempUpdateValue.connect(dash.tempGauge.mcTemp_update)
        canWorker.motorTempUpdateValue.connect(dash.tempGauge.motorTemp_update)
        canWorker.highMotorTempUpdateValue.connect(dash.tempGauge.highMotorTemp_update)
        canWorker.highCellTempUpdateValue.connect(dash.tempGauge.highCellTemp_update)
        canWorker.lowCellTempUpdateValue.connect(dash.tempGauge.lowCellTemp_update)
        
        canWorker.errorSignal.connect(dash.error_update)
        canWorker.errorSignal.connect(dash.errorGauge.error_update)        
        canWorker.rpmUpdateValue.connect(dash.errorGauge.RPMCut_update)
        #signal/slot connections for debug screen
        canWorker.rpmUpdateValue.connect(dash.debug.c1.channel_update)
        canWorker.socUpdateValue.connect(dash.debug.c2.channel_update)
        canWorker.mcTempUpdateValue.connect(dash.debug.c3.channel_update)
        canWorker.motorTempUpdateValue.connect(dash.debug.c4.channel_update)
        canWorker.highCellTempUpdateValue.connect(dash.debug.c5.channel_update)
        canWorker.lowCellTempUpdateValue.connect(dash.debug.c6.channel_update)
        canWorker.highMotorTempUpdateValue.connect(dash.debug.c7.channel_update)
        canWorker.DCLUpdateValue.connect(dash.debug.c8.channel_update)        

    if arguments.Args.gpsoff == True:
        try:
            gpsWorker = GpsReader()
            gpsWorker.start()
        except:   # not exiting correctly
            exit(0)
        #gpsWorker.currentLapTimeValue.connect(dash.currentLapTimeGauge.currentLapTime_update)
        gpsWorker.latValue.connect(dash.debugGps.gpsGauge.lat_update)
        gpsWorker.longValue.connect(dash.debugGps.gpsGauge.long_update)
        gpsWorker.rollValue.connect(dash.debugGps.gpsGauge.roll_update)
        gpsWorker.pitchValue.connect(dash.debugGps.gpsGauge.pitch_update)
        gpsWorker.gForceValue.connect(dash.debugGps.gpsGauge.gForce_update)
        
    if arguments.Args.log:
        fileWriter = FileWriter()
        fileWriter.start()
        if arguments.Args.canoff == True:
            canWorker.rpmUpdateValue.connect(fileWriter.rpm_write)
            canWorker.socUpdateValue.connect(fileWriter.soc_write)
            canWorker.mcTempUpdateValue.connect(fileWriter.mcTemp_write)
            canWorker.motorTempUpdateValue.connect(fileWriter.motorTemp_write)
            canWorker.highMotorTempUpdateValue.connect(fileWriter.highMotorTemp_write)
            canWorker.highCellTempUpdateValue.connect(fileWriter.highCellTemp_write)
            canWorker.lowCellTempUpdateValue.connect(fileWriter.lowCellTemp_write)
            canWorker.DCLUpdateValue.connect(fileWriter.DCL_write)
            canWorker.errorSignal.connect(fileWriter.error_write)
        if arguments.Args.gpsoff == True:
            gpsWorker.latValue.connect(fileWriter.lat_write)
            gpsWorker.longValue.connect(fileWriter.long_write)
            gpsWorker.rollValue.connect(fileWriter.roll_write)
            gpsWorker.pitchValue.connect(fileWriter.pitch_write)
            gpsWorker.gForceValue.connect(fileWriter.gForce_write)
            gpsWorker.bodyAccelValue.connect(fileWriter.bodyAccel_write)
            gpsWorker.velValue.connect(fileWriter.vel_write)


    if arguments.Args.test == True and arguments.Args.canoff == True:
        tester = TestThread()
        tester.start()
        canWorker.rpmUpdateValue.connect(tester.rpm_check)
        canWorker.socUpdateValue.connect(tester.soc_check)
        canWorker.mcTempUpdateValue.connect(tester.mcTemp_check)
        canWorker.motorTempUpdateValue.connect(tester.motorTemp_check)
        canWorker.highCellTempUpdateValue.connect(tester.highCellTemp_check)
        canWorker.lowCellTempUpdateValue.connect(tester.lowCellTemp_check)
        canWorker.DCLUpdateValue.connect(tester.DCL_check)
        canWorker.errorSignal.connect(tester.Error_check)
            
    app.processEvents()
    sys.exit(app.exec_())
                                                                
