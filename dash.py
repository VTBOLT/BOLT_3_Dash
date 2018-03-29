###################################################################################################################
## Description: Creates main window, places all gauges in main window, displays errors to rider, handles file menu options
## Values displayed: rpmGuage, socGauge, tempGuage, lapTimePannel (currently removed) debug window, gpsDebug window
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
## Notes:
####################################################################################################################

import sys
import time
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QAction, QPushButton
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QThread, pyqtSlot
from PyQt5.QtGui import QKeyEvent
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
from stateMachineGUI import StateMachine

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
    precharge = pyqtSignal(int)
    estop = pyqtSignal(int)
    raceMode = pyqtSignal()

    def __init__(self, parent=None):
        super(Dash, self).__init__(parent)

        self.setWindowTitle('BOLT DASH')
        self.setMinimumWidth(DASH_WIDTH)
        self.setMinimumHeight(DASH_HEIGHT)
        self.initGUI()

    def initGUI(self):
        self.setAutoFillBackground(True)
        self.arguments = Arg_Class()
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        p.setColor(self.foregroundRole(), Qt.white)

        self.setPalette(p)
        ######################################################
        ###state machine starts here
        self.stateMachine = StateMachine(self)
        self.stateMachine.move(DASH_WIDTH/2-200,DASH_HEIGHT/2-100)
        self.stateMachine.resize(300,200)
        ## call function that sets the text of each of the startup screens based on what gpio signals are high
        ## once startup is complete call these to setup dash in race mode
        self.rpmGauge = Rpm(self)
        self.rpmGauge.move(0, 16.0)
        self.rpmGauge.resize(DASH_WIDTH,RPM_HEIGHT)

        #self.rpmGauge.hide()

        self.socGauge = Soc(self)
        self.socGauge.move(500,GAUGE_VPOS - 150.0)
        self.socGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*3.0)

        self.tempGauge = Temp(self)
        self.tempGauge.move(660,GAUGE_VPOS - 180.0)
        self.tempGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2.5)

        self.debug = Debug(self)
        self.debugGps = DebugGPS(self)
        self.debug.hide()
        self.debugGps.hide()

        self.errorGauge = Error(self)
        self.errorGauge.move(20, 340)
        self.errorGauge.resize(GAUGE_WIDTH*2.5, GAUGE_HEIGHT)

        self.stateMachine.show()
        self.socGauge.hide()
        self.tempGauge.hide()
        self.rpmGauge.hide()
        self.errorGauge.hide()

        if self.arguments.Args.debug:
            self.debug.show()

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

#______________________________________________________________________#
# System State Machine
# Each of the following pyqtSlots represenents a state in the system
# state machine.

    @pyqtSlot()
    def idol_state(self):
        """TODO(chrise92):Show 'Turn on Accessory Switch' screen
        and wait for acc GPIO pin to go HI"""
        pass

    @pyqtSlot()
    def acc_on_state(self):
        """TODO(chrise92): Show "Pump Good, BMS Good, Turn on Ignition Switch' screen
        and wait for ign GPIO pin to go HI
        - check for all required signals, ACC, PRESSURE_OK, IMD_OK, BMS_DE
        - display errors if they exist
        """
        pass

    @pyqtSlot()
    def ign_on_state(self):
        """TODO(chrise92):
        - if CAN does not say MC on say 'Precharging...''
        - if CAN does say MC on say 'Precharge complete! Press Start Button'
        - if there is a POST FAULT, go to POST_FAULT_STATE
        """
        pass

    @pyqtSlot()
    def motor_enabled_state(self):
        """TODO(chrise92):
        - show racing screen
        - check for faults
        - go to run_fault_state if one is found
        """
        pass

    @pyqtSlot()
    def run_fault_state(self):
        """TODO(chrise92):
        - determine criticality of the fault
        - report the fault
        - go to interter_disabled_state if MC turned off, or if criticality is high
        - go back to interter_enabled_state if MC still running
        """
        pass

    @pyqtSlot()
    def post_fault_state(self):
        """TODO(chrise92):
        - report fault and go to inverter_disabled_state
        """
        pass

    @pyqtSlot()
    def inverter_disabled_state(self):
        """TODO(chrise92)
        - Show blue screen of death, display error, and instruct rider for next actions
        depending on reason for disabled state
        - Go back to acc_on state once ignition is switched off
        """
        pass
#________________________________________________________________________#


    def keyPressEvent(self, event):
        if (type(event) == QKeyEvent and event.key() == 0x41):
            self.accessoryPress.emit(1)
            print("Accessory Pressed")
        elif (type(event) == QKeyEvent and event.key() == 0x49):
            self.ignitionPress.emit(2)
            print("Ignition Pressed")
            print("Pre-charge start")
            time.sleep(3)
            print("Pre-charge complete")
            self.raceMode.emit()
        elif (type(event) == QKeyEvent and event.key() == 0x45):
            self.estop.emit(0)
            print("Emergency Stop")

    @pyqtSlot(int, int, int, int)
    def error_update(self, v1, v2, v3, v4):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        p.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(p)
        self.update()
        print("ERROR, Post Lo:", v1, "Post Hi:", v2, "Run Lo:", v3, "Run Hi:", v4)

    @pyqtSlot()
    def race(self):
        self.stateMachine.hide()
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
