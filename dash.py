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
    prechargeUpdateValue = pyqtSignal(int)

    """Initialize state transition variables"""
    acc_on = False
    bms_de = True
    imd_ok = True
    pressure_ok = True
    ign_on = False
    start_button_pressed = False
    fault_occurred = False
    motor_enabled = False
    inverter_disabled = False
    precharge_ok = False

    current_state = 'IDLE'
    next_state = 'IDLE'
    
    # fault occurrence flag
    fault_flag = False

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
        self.set_foreground(QColor(255, 129, 0))
        self.set_background(Qt.black)

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

        self.hide_widgets()
        self.show_startup_widgets()

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
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_P):
            print("Precharge Ok")
            self.prechargeUpdateValue.emit(3)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_Q):
            print("Precharge Not Ok")
            self.prechargeUpdateValue.emit(1)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_K):
            print("Ign Off")
            self.ignitionPress.emit(0)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_S):
            print("Start button pressed")
            self.startButton.emit(1)
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_F):
            self.fault_flag = True
            print("Fault detected")
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_H):
            if self.fault_flag:
                self.errorSignal.emit(0, 0x8000, 0, 0)
                self.fault_flag = False
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_M):
            if self.fault_flag:
                self.errorSignal.emit(0, 0, 0, 0x04)
                self.fault_flag = False
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_L):
            if self.fault_flag:
                self.errorSignal.emit(0, 0x01, 0, 0)
                self.fault_flag = False
        elif (type(event) == QKeyEvent and event.key() == Qt.Key_O):
            self.errorSignal.emit(0, 0, 0, 0)
            self.fault_flag = False
            print("Fault has been fixed")

    def changeStates(self):
        """Checks conditions and determines next state"""

        ## IDLE State transition logic
        if self.current_state == 'IDLE':
            self.start_button_pressed = False
            self.idle_state()
            print("In Idle State, ", self.acc_on)
            if self.acc_on:
                self.current_state = 'ACC_ON'
                self.acc_on_state()

        ## ACC_ON State transition logic
        elif self.current_state == 'ACC_ON':
            self.start_button_pressed = False
            self.acc_on_state()
            if not self.acc_on:
                print("In ACC On, ", self.acc_on)
                self.ign_on = False
                self.current_state = 'IDLE'
                self.idle_state()
            elif self.ign_on and self.precharge_ok:
                self.current_state = 'IGN_ON'
                self.ign_on_state()

        ## IGN_ON State transition logic
        elif self.current_state == 'IGN_ON':
            if not self.acc_on:
                self.ign_on = False
                self.current_state = 'IDLE'
                self.idle_state()
            elif not self.ign_on or not self.precharge_ok:
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
            elif not self.ign_on or not self.precharge_ok:
                self.current_state = 'ACC_ON'
                self.acc_on_state()
            elif self.fault_occurred:
                self.current_state = 'FAULT'
                self.fault_state()

        ## FAULT state transition logic
        elif self.current_state == 'FAULT':
            if not self.fault_occurred:
                self.current_state = 'MOTOR_ENABLED'
                self.motor_enabled_state()
            else:
                self.fault_state()

        ## INVERTER_DISABLED state transition logic
        elif self.current_state == 'INVERTER_DISABLED':
            self.inverter_disabled_state()

    def idle_state(self):
        """TODO(chrise92):Show 'Turn on Accessory Switch' screen
        and wait for acc GPIO pin to go HI"""
        self.set_foreground(QColor(255, 129, 0))
        self.set_background(Qt.black)
        self.msg.setText("Turn on Accessory Switch")

        self.hide_widgets()
        self.show_startup_widgets()

    def acc_on_state(self):
        """TODO(chrise92): Show "Pump Good, BMS Good, Turn on Ignition Switch' screen
        and wait for ign GPIO pin to go HI
        - check for all required signals, ACC, PRESSURE_OK, IMD_OK, BMS_DE
        - display errors if they exist
        """
        self.set_foreground(QColor(255, 129, 0))
        self.set_background(Qt.black)
        self.msg.setText("Turn on Ignition Switch")

        self.hide_widgets()
        self.show_startup_widgets()

    def ign_on_state(self):
        """TODO(chrise92):
        - if CAN does not say MC on say 'Precharging...''
        - if CAN does say MC on say 'Precharge complete! Press Start Button'
        """
        self.set_foreground(QColor(255, 129, 0))
        self.set_background(Qt.black)
        self.msg.setText("Press the start button")

        self.hide_widgets()
        self.show_startup_widgets()

    def motor_enabled_state(self):
        self.set_foreground(Qt.white)
        self.set_background(Qt.black)

        self.hide_widgets()
        self.show_race_widgets()

    def fault_state(self):
        # clear screen
        self.hide_widgets()
        # choose most critical fault
        curr_fault = max(self.errorGauge.fault_set, key=lambda x:x[1])
        print("faults present: ", self.errorGauge.fault_set)
        if curr_fault[1] == self.errorGauge.FaultLevel.HIGH:
            self.show_high_fault_screen(curr_fault)
        elif curr_fault[1] == self.errorGauge.FaultLevel.MID:
            self.show_mid_fault_screen(curr_fault)
        else:
            self.show_low_fault_screen()

    def show_high_fault_screen(self, curr_fault):
        self.set_foreground(Qt.black)
        self.set_background(Qt.red)

        self.errorGauge.show()
        self.title.setText(curr_fault[0])
        self.title.show()
    
    def show_mid_fault_screen(self, curr_fault):
        self.set_foreground(Qt.black)
        self.set_background(Qt.yellow)

        self.errorGauge.show()
        self.title.setText(curr_fault[0])
        self.title.show()

    def show_low_fault_screen(self):
        self.set_foreground(Qt.white)
        self.set_background(Qt.black)

        self.errorGauge.show()
        self.show_race_widgets()

    # TODO Figure out if a separate inverter disabled state is necessary
    # def inverter_disabled_state(self):
    #     """
    #     - Show blue screen of death, display error, and instruct rider for next actions
    #     depending on reason for disabled state
    #     - Go back to acc_on state once ignition is switched off
    #     """
    #     #  clear screen
    #     self.socGauge.hide()
    #     self.rpmGauge.hide()
    #     # blue screen of death
    #     self.set_background(Qt.blue)
    #     self.set_foreground(Qt.white)

    #     self.title.setText("INVERTER_DISABLED_STATE: TODO")
    #     self.title.show()

    def set_foreground(self, qt_color):
        self.p.setColor(self.foregroundRole(), qt_color)
        self.setPalette(self.p)

    def set_background(self, qt_color):
        self.p.setColor(self.backgroundRole(), qt_color)
        self.setPalette(self.p)

    def hide_widgets(self):
        self.logo.hide()
        self.title.hide()
        self.msg.hide()
        self.rpmGauge.hide()
        self.socGauge.hide()
        self.tempGauge.hide()
        self.debug.hide()
        self.debugGps.hide()
        self.errorGauge.hide()

    def show_race_widgets(self):
        self.rpmGauge.show()
        self.socGauge.show()
        self.tempGauge.show()

    def show_startup_widgets(self):
        self.logo.show()
        self.msg.show()

    def high_bits(self, n):
        while n:
            b = n & (~n+1)
            yield b
            n ^= b

    @pyqtSlot()
    def temp_close(self):
        self.tempGauge.hide()

    @pyqtSlot()
    def temp_open(self):
        self.tempGauge.show()

    @pyqtSlot(int)
    def updateACC_ON(self, value):
        print("Emitted ACC_ON ", value)
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
    def updateFAULT(self, post_lo_fault, post_hi_fault, run_lo_fault, run_hi_fault):
        # empty fault set
        self.errorGauge.fault_set.clear()
        # get all high bits in 2-byte CAN data
        for bit in self.high_bits(run_lo_fault):
            self.errorGauge.fault_set.add(self.errorGauge.run_lo_fault_dict[bit])
        for bit in self.high_bits(run_hi_fault):
            self.errorGauge.fault_set.add(self.errorGauge.run_hi_fault_dict[bit])
        for bit in self.high_bits(post_lo_fault):
            self.errorGauge.fault_set.add(self.errorGauge.post_lo_fault_dict[bit])
        for bit in self.high_bits(post_hi_fault):
            self.errorGauge.fault_set.add(self.errorGauge.post_hi_fault_dict[bit])

        # check if there were any faults detected
        if len(self.errorGauge.fault_set) > 0:
            self.fault_occurred = 1
            curr_fault = max(self.errorGauge.fault_set, key=lambda x:x[1])
            self.errorGauge.currErrorLabel.setText(curr_fault[0])
        else:
            self.fault_occurred = 0
        self.changeStates()

    @pyqtSlot(int)
    def updatePRECHARGE(self, VSM_state):
        if VSM_state == 2 or VSM_state == 3:
            self.precharge_ok = True
        else:
            self.precharge_ok = False
        self.changeStates()

    # TODO Figure out if a separate Inverter Disabled state is necessary 
    # @pyqtSlot(int)
    # def updateINVERTER_DISABLED(self, value):
    #     self.inverter_disabled = value
    #     self.changeStates()