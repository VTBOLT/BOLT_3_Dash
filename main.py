#!/usr/bin/env python

############################################################################################################
## Description: starts all threads, creates connections between signals and slots
## Threads: dash, can, gps, and filewritter threads
## Written for: BOLT Senior Design Team
## Authors: Henry Trease, Chris Evers
## Written: Fall 2017
## Modified: Spring 2018
## Notes:
############################################################################################################

import sys

from PyQt5.QtWidgets import QApplication
from dash import Dash
from stateMachine import StateMachine
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug
from args import Arg_Class
from fileWriter import FileWriter
from GPIOThread import GPIOThread

if __name__ == '__main__':
    app = QApplication(sys.argv)
    arguments = Arg_Class()

    dash = Dash()

    state_machine = StateMachine()
    state_machine.start()
	
    gpio_thread = GPIOThread()
    gpio_thread.start()

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

        #signal/slot connection for state machine
        dash.accessoryPress.connect(state_machine.updateACC_ON)
        dash.ignitionPress.connect(state_machine.updateIGN_ON)
        dash.startButton.connect(state_machine.updateSTART_BUTTON)

        state_machine.idle_signal.connect(dash.idle_state)
        state_machine.acc_on_signal.connect(dash.acc_on_state)
        state_machine.ign_on_signal.connect(dash.ign_on_state)
        state_machine.motor_enabled_signal.connect(dash.motor_enabled_state)
        state_machine.inverter_disabled_signal.connect(dash.inverter_disabled_state)
	
        gpio_thread.ignSignal.connect(state_machine.updateIGN_ON)
        gpio_thread.imdSignal.connect(state_machine.updateIMD_OK)
        gpio_thread.presSignal.connect(state_machine.updateACC_ON)
        gpio_thread.presSignal.connect(state_machine.updatePRESSURE_OK)
        gpio_thread.bmsdeSignal.connect(state_machine.updateBMS_DE)

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

    app.processEvents()
    sys.exit(app.exec_())

