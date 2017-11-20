#!/usr/bin/env python
import sys

from PyQt5.QtWidgets import QApplication

from dash import Dash
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug
from args import Arg_Class
from fileWriter import FileWriter

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

        canWorker.mcTempUpdateValue.connect(dash.tempGauge.mcTemp_update)
        canWorker.motorTempUpdateValue.connect(dash.tempGauge.motorTemp_update)
        canWorker.highMotorTempUpdateValue.connect(dash.tempGauge.motorTemp_update)
        canWorker.cellTempUpdateValue.connect(dash.tempGauge.cellTemp_update)
        
        canWorker.errorSignal.connect(dash.error_update)
        #if arguments.Args.log == True:
        if 0:
            canWorker.rpmUpdateValue.connect(dash.fileWriter.rpm_write)
            canWorker.socUpdateValue.connect(dash.fileWriter.soc_write)
            canWorker.mcTempUpdateValue.connect(dash.fileWriter.mcTemp_write)
            canWorker.motorTempUpdateValue.connect(dash.fileWriter.motorTemp_write)
            canWorker.highMotorTempUpdateValue.connect(dash.fileWriter.motorTemp_write)
            canWorker.cellTempUpdateValue.connect(dash.fileWriter.cellTemp_write)
            
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
        
        #if arguments.Args.log == True:
        if 0:
            gpsWorker.latValue.connect(dash.fileWriter.lat_write)
            gpsWorker.longValue.connect(dash.fileWriter.long_write)
            gpsWorker.rollValue.connect(dash.fileWriter.roll_write)
            gpsWorker.pitchValue.connect(dash.fileWriter.pitch_write)
            gpsWorker.gForceValue.connect(dash.fileWriter.gForce_write)
            gpsWorker.bodyAccelValue.connect(dash.fileWriter.bodyAccel_write)
            gpsWorker.velValue.connect(dash.fileWriter.vel_write)
    if arguments.Args.log:
        fileWriter = FileWriter()
        fileWriter.start()
        if arguments.Args.canoff == True:
            canWorker.rpmUpdateValue.connect(fileWriter.rpm_write)
            canWorker.socUpdateValue.connect(fileWriter.soc_write)
            canWorker.mcTempUpdateValue.connect(fileWriter.mcTemp_write)
            canWorker.motorTempUpdateValue.connect(fileWriter.motorTemp_write)
            canWorker.cellTempUpdateValue.connect(fileWriter.cellTemp_write)
        if arguments.Args.gpsoff == True:
            gpsWorker.latValue.connect(fileWriter.lat_write)
            gpsWorker.longValue.connect(fileWriter.long_write)
            gpsWorker.rollValue.connect(fileWriter.roll_write)
            gpsWorker.pitchValue.connect(fileWriter.pitch_write)
            gpsWorker.gForceValue.connect(fileWriter.gForce_write)
            gpsWorker.bodyAccelValue.connect(fileWriter.bodyAccel_write)
            gpsWorker.velValue.connect(fileWriter.vel_write)
        
    app.processEvents()
    sys.exit(app.exec_())
                                                                
