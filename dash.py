###################################################################################################################
## Description: Creates main window, places all gauges in main window, displays errors to rider, handles file menu options
## Values displayed: rpmGuage, socGauge, tempGuage, lapTimePannel (currently removed) debug window, gpsDebug window
## Written for: BOLT Senior Design Team
## Authors: Henry Trease, Chris Evers
## Written: Fall 2017
## Modified: Spring 2018
## Notes:
####################################################################################################################

import sys
import time
from enum import IntEnum
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QAction, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QThread, pyqtSlot
from PyQt5.QtGui import QKeyEvent, QPixmap, QFont, QColor
from socGauge import Soc
from rpmGauge import Rpm
from lapTimePannel import LastLapTime, CurrentLapTime, BestLapTime
from tempGauge import Temp
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug
from args import Arg_Class
from debugGps import DebugGPS
from fileWriter import FileWriter
from errorGauge import Error

DASH_WIDTH = 800
DASH_HEIGHT = 420

RPM_HEIGHT = (2/3)*DASH_HEIGHT
GAUGE_VPOS = 340
GAUGE_HEIGHT = 140
GAUGE_WIDTH = 200

class Dash(QMainWindow):

    """Signals for key presses"""
    accessoryPress = pyqtSignal(int)
    ignitionPress = pyqtSignal(int)
    startButton = pyqtSignal(int)
    errorSignal = pyqtSignal(int, int, int, int)

    """Initialize state transition variables"""
    acc_on = False
    bms_de = True
    imd_ok = True
    pressure_ok = True
    ign_on = False
    start_button_pressed = False
    post_fault_occurred = False
    run_fault_occurred = False
    motor_enabled = False
    inverter_disabled = False

    current_state = 'IDLE'
    next_state = 'IDLE'
    
    class FaultLevel(IntEnum):
        LOW = 0
        MID = 1
        HIGH = 2
    curr_fault = {'message': 'No Fault', 'level': FaultLevel.LOW}
    fault_list = []
    # run faults (low byte) list
    run_lo_fault_list = [
                            (0x0001, 'Motor Over-speed Fault', FaultLevel.LOW),
                            (0x0002, 'Over-current Fault', FaultLevel.HIGH),
                            (0x0004, 'Over-voltage', FaultLevel.HIGH),
                            (0x0008, 'Inverter Over-temperature Fault', FaultLevel.MID),
                            (0x0010, 'Accelerator Input Shorted Fault', FaultLevel.MID),
                            (0x0020, 'Accelerator Input Open Fault', FaultLevel.MID),
                            (0x0080, 'Inverter Response Time-out Fault', FaultLevel.LOW),
                            (0x0100, 'Hardware Gate/Desaturation Fault', FaultLevel.HIGH),
                            (0x0200, 'Hardware Over-current Fault', FaultLevel.HIGH),
                            (0x0400, 'Under-voltage Fault', FaultLevel.MID),
                            (0x0800, 'CAN Command Message Lost Fault', FaultLevel.MID),
                            (0x1000, 'Motor Over-temerature Fault', FaultLevel.MID)
                        ]
    
    # run faults (high byte) list
    run_hi_fault_list = [
                            (0x0001, 'Brake Input Shorted Fault', FaultLevel.LOW),
                            (0x0002, 'Brake Input Open Fault', FaultLevel.LOW),
                            (0x0004, 'Module A Over-temperature Fault', FaultLevel.MID),
                            (0x0008, 'Module B Over-temperature Fualt', FaultLevel.MID),
                            (0x0010, 'Module C Over-temperature Fault', FaultLevel.MID),
                            (0x0020, 'PCB Over-temperature Fault', FaultLevel.MID),
                            (0x0040, 'Gate Drive Board 1 Over-temperature Fault', FaultLevel.MID),
                            (0x0080, 'Gate Drive Board 2 Over-temperature Fault', FaultLevel.MID),
                            (0x0100, 'Gate Drive Board 3 Over-temperature Fault', FaultLevel.MID),
                            (0x0200, 'Current Sensor Fault', FaultLevel.MID),
                            (0x4000, 'Resolver Not Connected', FaultLevel.MID)
                        ]

    def __init__(self, parent=None):
        super(Dash, self).__init__(parent)

        self.setWindowTitle('BOLT DASH')
        self.setMinimumWidth(DASH_WIDTH)
        self.setMinimumHeight(DASH_HEIGHT)
        self.initGUI()

    def initGUI(self):
        self.setAutoFillBackground(True)
        self.arguments = Arg_Class()
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.black)
        self.p.setColor(self.foregroundRole(), QColor(255, 129, 0))
        self.setPalette(self.p)

        # This is the logo widget
        pixmap = QPixmap("BOLT3.png")
        pixmap = pixmap.scaled(DASH_WIDTH, DASH_HEIGHT)
        self.logo = QLabel(self)
        self.logo.setPixmap(pixmap)
        self.logo.move(0.0, 0.0)
        self.logo.resize(DASH_WIDTH, DASH_HEIGHT)

        # This is the title widget
        self.title_font = QFont("Helvetica", 32, QFont.Bold)
        self.title = QLabel(self)
        self.title.setText("Bolt III")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(self.title_font)
        self.title.move(0, DASH_HEIGHT * 1/4)
        self.title.resize(DASH_WIDTH, DASH_HEIGHT / 6)

        # This is the message widget
        self.msg_font = QFont("Helvetica", 16, QFont.Bold)
        self.msg = QLabel(self)
        self.msg.setText("Turn On Accessory Switch")
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setFont(self.msg_font)
        self.msg.move(0, DASH_HEIGHT * 3/4)
        self.msg.resize(DASH_WIDTH, DASH_HEIGHT / 6)

        ## call function that sets the text of each of the startup screens based on what gpio signals are high
        ## once startup is complete call these to setup dash in race mode
        self.rpmGauge = Rpm(self)
        self.rpmGauge.move(0, 16.0)
        self.rpmGauge.resize(DASH_WIDTH,RPM_HEIGHT)

        self.socGauge = Soc(self)
        self.socGauge.move(500,GAUGE_VPOS - 150.0)
        self.socGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*3.0)

        self.tempGauge = Temp(self)
        self.tempGauge.move(660,GAUGE_VPOS - 180.0)
        self.tempGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2.5)

        self.debug = Debug(self)
        self.debugGps = DebugGPS(self)

        self.errorGauge = Error(self)
        self.errorGauge.move(20, 340)
        self.errorGauge.resize(GAUGE_WIDTH*2.5, GAUGE_HEIGHT)

        if self.arguments.Args.debug:
            self.debug.show()

        self.logo.show()
        self.title.hide()
        self.msg.show()
        self.rpmGauge.hide()
        self.socGauge.hide()
        self.tempGauge.hide()
        self.debug.hide()
        self.debugGps.hide()
        self.errorGauge.hide()

        #### if an error is thrown enter error state machine defined here


        ######################################################
        #### if possible move this so its always visiable, even during startup
        #### It would be a good idea to setup a menu option to skip the startup screens
        self.mainMenu = self.menuBar()
        self.mainMenu.setStyleSheet("QMenuBar::item { color: rgb(255,0,0);}") #sets text color
        self.mainMenu.setStyleSheet("QMenuBar::item { background-color: rgb(255,255,255);}") # sets button color

        self.fileMenu = self.mainMenu.addMenu('Debug')
        self.openDebug = QAction("Open Debug Window", self)
        self.fileMenu.addAction(self.openDebug)
        self.openDebug.triggered.connect(self.debug.debug_open)

        self.openGPS = QAction("Open GPS Window", self)
        self.fileMenu.addAction(self.openGPS)
        self.openGPS.triggered.connect(self.debugGps.debug_open)

        #### Option to display graphs of data, not implemented yet
        self.analyzeMenu = self.mainMenu.addMenu('Analyze')
        self.graphRpm = QAction("Graph RPM", self)
        self.graphSoc = QAction("Graph SOC", self)
        self.analyzeMenu.addAction(self.graphRpm)
        self.analyzeMenu.addAction(self.graphSoc)

        self.tempMenu = self.mainMenu.addMenu('Temp')
        self.settingMenu = self.mainMenu.addMenu('Settings')
        ### Open temp dispaly
        self.tempOn = QAction("Open Temp Display:", self)
        self.settingMenu.addAction(self.tempOn)
        self.tempOn.triggered.connect(self.temp_open)
        ### Close temp display
        self.tempOff = QAction("Close Temp Display:", self)
        self.settingMenu.addAction(self.tempOff)
        self.tempOff.triggered.connect(self.temp_close)


        if self.arguments.Args.debug:
            #self.debug.show()
            self.debugGps.show()


        #if self.arguments.Args.log:
            #self.fileWriter = FileWriter(self)

    def keyPressEvent(self, event):
        if (type(event) == QKeyEvent and event.key() == Qt.Key_A):
            print("Acc On")
            self.accessoryPress.emit(1)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_Z):
            print("Acc Off")
            self.accessoryPress.emit(0)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_I):
            print("Ign On")
            self.ignitionPress.emit(1)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_K):
            print("Ign Off")
            self.ignitionPress.emit(0)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_S):
            print("Start button pressed")
            self.startButton.emit(1)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_F):
            print("Fault detected")
            self.errorSignal.emit(0, 0, 1, 0)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_O):
            print("Fault has been fixed")
            self.errorSignal.emit(0, 0, 0, 0)

    def changeStates(self):
        """Checks conditions and determines next state"""

        ## IDLE State transition logic
        if self.current_state == 'IDLE':
            self.start_button_pressed = False
            self.idle_state()
            if self.acc_on:
                self.current_state = 'ACC_ON'
                self.acc_on_state()

        ## ACC_ON State transition logic
        elif self.current_state == 'ACC_ON':
            self.start_button_pressed = False
            self.acc_on_state()
            if not self.acc_on:
                self.ign_on = False
                self.current_state = 'IDLE'
                self.idle_state()
            elif self.ign_on:
                self.current_state = 'IGN_ON'
                self.ign_on_state()

        ## IGN_ON State transition logic
        elif self.current_state == 'IGN_ON':
            if not self.acc_on:
                self.ign_on = False
                self.current_state = 'IDLE'
                self.idle_state()
            elif not self.ign_on:
                self.current_state = 'ACC_ON'
                self.acc_on_state()
            elif self.start_button_pressed:
                self.current_state = 'MOTOR_ENABLED'
                self.motor_enabled_state()

        ## MOTOR_ENABLED state transition logic
        elif self.current_state == 'MOTOR_ENABLED':
            self.motor_enabled_state()
            if not self.acc_on:
                self.ign_on = False
                self.current_state = 'IDLE'
                self.idle_state()
            elif not self.ign_on:
                self.current_state = 'ACC_ON'
                self.acc_on_state()
            elif self.run_fault_occurred:
                self.current_state = 'RUN_FAULT'
                self.run_fault_state()

        ## RUN_FAULT state transition logic
        elif self.current_state == 'RUN_FAULT':
            self.run_fault_state()
            if not self.run_fault_occurred:
                self.current_state = 'ACC_ON'
                self.acc_on_state()

        ## INVERTER_DISABLED state transition logic
        elif self.current_state == 'INVERTER_DISABLED':
            self.inverter_disabled_state()

    def idle_state(self):
        """TODO(chrise92):Show 'Turn on Accessory Switch' screen
        and wait for acc GPIO pin to go HI"""
        self.p.setColor(self.foregroundRole(), QColor(255, 129, 0))
        self.setPalette(self.p)

        self.msg.setText("Turn on Accessory Switch")

        self.logo.show()
        self.msg.show()

        self.title.hide()
        self.socGauge.hide()
        self.tempGauge.hide()
        self.rpmGauge.hide()
        self.errorGauge.hide()
        self.debug.hide()
        self.debugGps.hide()

    def acc_on_state(self):
        """TODO(chrise92): Show "Pump Good, BMS Good, Turn on Ignition Switch' screen
        and wait for ign GPIO pin to go HI
        - check for all required signals, ACC, PRESSURE_OK, IMD_OK, BMS_DE
        - display errors if they exist
        """
        self.p.setColor(self.foregroundRole(), QColor(255, 129, 0))
        self.setPalette(self.p)

        self.msg.setText("Turn on Ignition Switch")

        self.logo.show()
        self.msg.show()

        self.title.hide()
        self.socGauge.hide()
        self.tempGauge.hide()
        self.rpmGauge.hide()
        self.errorGauge.hide()
        self.debug.hide()
        self.debugGps.hide()

    def ign_on_state(self):
        """TODO(chrise92):
        - if CAN does not say MC on say 'Precharging...''
        - if CAN does say MC on say 'Precharge complete! Press Start Button'
        - if there is a POST FAULT, go to POST_FAULT_STATE
        """
        self.p.setColor(self.foregroundRole(), QColor(255, 129, 0))
        self.setPalette(self.p)

        self.msg.setText("Press the start button")

        self.logo.show()
        self.msg.show()

        self.title.hide()
        self.socGauge.hide()
        self.tempGauge.hide()
        self.rpmGauge.hide()
        self.errorGauge.hide()
        self.debug.hide()
        self.debugGps.hide()

    def motor_enabled_state(self):
        """TODO(chrise92):
        - show racing screen
        - check for faults
        - go to run_fault_state if one is found
        """
        self.p.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(self.p)

        self.logo.hide()
        self.msg.hide()

        self.title.hide()
        self.socGauge.show()
        self.tempGauge.hide()
        self.rpmGauge.show()
        self.errorGauge.hide()
        self.debug.hide()
        self.debugGps.hide()

    def run_fault_state(self):
        """TODO(chrise92):
        - determine criticality of the fault
        - report the fault
        - go to interter_disabled_state if MC turned off, or if criticality is high
        - go back to interter_enabled_state if MC still running
        """
        #  clear screen
        self.socGauge.hide()
        self.rpmGauge.hide()
        # blue screen of death
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        p.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(p)

        self.title.setText(self.curr_fault['message'])
        self.title.show()

    def post_fault_state(self):
        """TODO(chrise92):
        - report fault and go to inverter_disabled_state
        """
        pass

    def inverter_disabled_state(self):
        """TODO(chrise92)
        - Show blue screen of death, display error, and instruct rider for next actions
        depending on reason for disabled state
        - Go back to acc_on state once ignition is switched off
        """
        #  clear screen
        self.socGauge.hide()
        self.rpmGauge.hide()
        # blue screen of death
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        p.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(p)

        self.title.setText("INVERTER_DISABLED_STATE: TODO")
        self.title.show()

    @pyqtSlot()
    def race(self):
        #self.stateMachine.hide()
        self.rpmGauge.show()
        self.socGauge.show()
        self.tempGauge.show()
        self.errorGauge.show()

    @pyqtSlot()
    def temp_close(self):
        self.tempGauge.hide()

    @pyqtSlot()
    def temp_open(self):
        self.tempGauge.show()

    @pyqtSlot(int)
    def updateACC_ON(self, value):
        self.acc_on = value
        self.changeStates()

    @pyqtSlot(int)
    def updateBMS_DE(self, value):
        self.bms_de = value
        self.changeStates()

    @pyqtSlot(int)
    def updateIMD_OK(self, value):
        self.imd_ok = value
        self.changeStates()

    @pyqtSlot(int)
    def updatePRESSURE_OK(self, value):
        self.pressure_ok = value
        self.changeStates()

    @pyqtSlot(int)
    def updateIGN_ON(self, value):
        self.ign_on = value
        self.changeStates()

    @pyqtSlot(int)
    def updateSTART_BUTTON(self, value):
        self.start_button_pressed = value
        self.changeStates()

    @pyqtSlot(int)
    def updateMOTOR_ENABLED(self, value):
        self.motor_enabled = value
        self.changeStates()

    @pyqtSlot(int, int, int, int)
    def updateFAULT(self, v1, v2, v3, v4):
        """TODO(mathew6)
        - Set the error level (low or high)
        - Set the error message
        - let the state methods take care of changing the screen
        """
        # append new fault to fault_list
        for i in self.run_lo_fault_list:
            if i[0] & v3 and i[1:2] not in self.fault_list:
                self.fault_list.append(i[1:2])
                # set new curr_fault
                if i[2] >= self.curr_fault['level']:
                    self.curr_fault['message'] = i[1]
                    self.curr_fault['level'] = i[2]
                    self.run_fault_occurred = 1
                    print(self.curr_fault)

        self.changeStates()

    @pyqtSlot(int)
    def updatePOST_FAULT(self, value):
        self.post_fault_occurred = value
        self.changeStates()

    @pyqtSlot(int)
    def updateRUN_FAULT(self, value):
        self.run_fault_occurred = value
        self.changeStates()

        
    @pyqtSlot(int)
    def updateINVERTER_DISABLED(self, value):
        self.inverter_disabled = value
        self.changeStates()