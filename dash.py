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

DASH_WIDTH = 1000
DASH_HEIGHT = 550

RPM_HEIGHT = (2/3)*DASH_HEIGHT
GAUGE_VPOS = 340
GAUGE_HEIGHT = 140
GAUGE_WIDTH = 200

class Dash(QMainWindow):
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

        ## call function that sets the text of each of the startup screens based on what gpio signals are high
        
        ## once startup is complete call these to setup dash in race mode
        self.rpmGauge = Rpm(self)
        self.rpmGauge.move(0, 16.0)
        self.rpmGauge.resize(DASH_WIDTH,RPM_HEIGHT)

        self.socGauge = Soc(self)
        self.socGauge.move(600,GAUGE_VPOS - 150.0)
        self.socGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2.5)

        self.tempGauge = Temp(self)
        self.tempGauge.move(850,GAUGE_VPOS - 150.0)
        self.tempGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2.5)
        self.tempGauge.show()

        self.debug = Debug(self)
        self.debugGps = DebugGPS(self)
        self.debug.hide()
        self.debugGps.hide()

        self.errorGauge = Error(self)
        self.errorGauge.move(20, 400)
        self.errorGauge.resize(GAUGE_WIDTH*2.5, GAUGE_HEIGHT)
        self.errorGauge.show()

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

    @pyqtSlot(int, int, int, int)
    def error_update(self, v1, v2, v3, v4):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        p.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(p)
        self.update()
        print("ERROR, Post Lo:", v1, "Post Hi:", v2, "Run Lo:", v3, "Run Hi:", v4)

    @pyqtSlot()
    def temp_close(self):
        self.tempGauge.hide()
    @pyqtSlot()
    def temp_open(self):
        self.tempGauge.show()
