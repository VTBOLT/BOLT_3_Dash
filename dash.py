import sys
import time
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QAction, QPushButton
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QThread, pyqtSlot
import argparse

from socGauge import Soc
from rpmGauge import Rpm
from lapTimePannel import LastLapTime, CurrentLapTime, BestLapTime
from tempGauge import Temp
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug
from debugGps import DebugGPS
from fileWriter import FileWriter

DASH_WIDTH = 800
DASH_HEIGHT = 480

RPM_HEIGHT = (2/3)*DASH_HEIGHT
GAUGE_VPOS = 340
GAUGE_HEIGHT = 140
GAUGE_WIDTH = 200

DEMO = False
DEBUG = False
LOG = False

if len(sys.argv) > 1:
    if any("-demo" in s for s in sys.argv):
        DEMO = True
    if any("-debug" in s for s in sys.argv):
        DEBUG = True
    if any("-log" in s for s in sys.argv):
        LOG = True
        
class Dash(QMainWindow):
    def __init__(self, parent=None):
        super(Dash, self).__init__(parent)

        self.setWindowTitle('BOLT DASH')
        self.setMinimumWidth(DASH_WIDTH)
        self.setMinimumHeight(DASH_HEIGHT)
        self.initGUI()
        
    def initGUI(self):
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        p.setColor(self.foregroundRole(), Qt.red)

        self.setPalette(p)

        self.rpmGauge = Rpm(self)
        self.rpmGauge.move(0,0)
        self.rpmGauge.resize(DASH_WIDTH,RPM_HEIGHT)

        self.socGauge = Soc(self)
        self.socGauge.move(0,GAUGE_VPOS)
        self.socGauge.resize(GAUGE_WIDTH+100,GAUGE_HEIGHT)

        self.currentLapTimeGauge =  CurrentLapTime(self)
        self.currentLapTimeGauge.resize(GAUGE_WIDTH+100,GAUGE_HEIGHT)

        if DEMO:
            self.currentLapTimeGauge.move(GAUGE_WIDTH*2,GAUGE_VPOS)
        else:
            self.currentLapTimeGauge.move(GAUGE_WIDTH*2,GAUGE_VPOS-40)

        self.lastLapTimeGauge = LastLapTime(self)
        self.lastLapTimeGauge.move(GAUGE_WIDTH,GAUGE_VPOS)
        self.lastLapTimeGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT/2)        
        self.lastLapTimeGauge.hide()
        
        self.bestLapTimeGauge = BestLapTime(self)
        self.bestLapTimeGauge.move(GAUGE_WIDTH,GAUGE_VPOS+GAUGE_HEIGHT/2)
        self.bestLapTimeGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT/2)
        self.bestLapTimeGauge.hide()
        
        self.tempGauge = Temp(self)
        self.tempGauge.move(GAUGE_WIDTH*3,GAUGE_VPOS)
        self.tempGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT)
        self.tempGauge.hide()

        if DEMO:
            self.tempGauge.show()
            self.lastLapTimeGauge.show()
            self.bestLapTimeGauge.show()

        self.debug = Debug(self)
        self.debugGps = DebugGPS(self)
        self.debug.hide()
        self.debugGps.hide()
        
        self.mainMenu = self.menuBar()
        
        self.mainMenu.setStyleSheet("QMenuBar::item { color: rgb(255,0,0);}")
        self.mainMenu.setStyleSheet("QMenuBar::item { background-color: rgb(255,255,255);}")


        self.fileMenu = self.mainMenu.addMenu('Debug')
        open = QAction("Open Debug Window", self)
        
        self.fileMenu.addAction(open)
        open.triggered.connect(self.debug.debug_open)            

        self.open_gps = QAction("Open GPS Window", self)
        self.fileMenu.addAction(self.open_gps)
        self.open_gps.triggered.connect(self.debugGps.debug_open)
        
        self.analyzeMenu = self.mainMenu.addMenu('Analyze')
        self.graphRpm = QAction("Graph RPM", self)
        self.graphSoc = QAction("Graph SOC", self)
        self.analyzeMenu.addAction(self.graphRpm)
        self.analyzeMenu.addAction(self.graphSoc)
        
        self.tempMenu = self.mainMenu.addMenu('Temp')
        self.setting = QAction("Settings", self)
        
        if DEBUG:
            #self.debug.show()
            self.debugGps.show()

        if LOG:
            self.fileWriter = FileWriter(self)
        
    @pyqtSlot()
    def error_update(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        p.setColor(self.foregroundRole(), Qt.black)
        self.setPalette(p)
        self.update()
        print("ERROR")
