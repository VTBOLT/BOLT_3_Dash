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
        p.setColor(self.foregroundRole(), Qt.red)

        self.setPalette(p)

        self.rpmGauge = Rpm(self)
        self.rpmGauge.move(0,0)
        self.rpmGauge.resize(DASH_WIDTH,RPM_HEIGHT)

        self.socGauge = Soc(self)
        self.socGauge.move(0,GAUGE_VPOS)
        self.socGauge.resize(GAUGE_WIDTH+200,GAUGE_HEIGHT)

        self.tempGauge = Temp(self)
        self.tempGauge.move(800,GAUGE_VPOS-150)
        self.tempGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2.5)
        self.tempGauge.show()

        self.debug = Debug(self)
        self.debugGps = DebugGPS(self)
        self.debug.hide()
        self.debugGps.hide() 

        if self.arguments.Args.debug:
            self.debug.show()

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
        p.setColor(self.foregroundRole(), Qt.black)
        self.setPalette(p)
        self.update()
        print("ERROR:", v1, v2, v3, v4)

    @pyqtSlot()
    def temp_close(self):
        self.tempGauge.hide()
    @pyqtSlot()
    def temp_open(self):
        self.tempGauge.show()
        
