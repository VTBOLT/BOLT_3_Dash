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
        arguments = Arg_Class()
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

        self.tempGauge = Temp(self)
        self.tempGauge.move(800,GAUGE_VPOS-150)
        self.tempGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2)
        self.tempGauge.hide()
        #if arguments.Args.demo:
        self.tempGauge.show()

        self.debug = Debug(self)
        self.debugGps = DebugGPS(self)
        self.debug.hide()
        self.debugGps.hide() 

        if arguments.Args.debug:
            self.debug.show()

        self.mainMenu = self.menuBar()        
        self.mainMenu.setStyleSheet("QMenuBar::item { color: rgb(255,0,0);}") #sets text color
        self.mainMenu.setStyleSheet("QMenuBar::item { background-color: rgb(255,255,255);}") # sets button color


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
        
        if arguments.Args.debug:
            #self.debug.show()
            self.debugGps.show()

        #if arguments.Args.log:
        self.fileWriter = FileWriter(self)
        
    @pyqtSlot()
    def error_update(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        p.setColor(self.foregroundRole(), Qt.black)
        self.setPalette(p)
        self.update()
        print("ERROR")
