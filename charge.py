import sys
import time
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QAction, QPushButton, QVBoxLayout, QLabel,QHBoxLayout, QGridLayout, QTabWidget, QLCDNumber
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
from socGraph import CustomFigCanvas1
from voltgraph import CustomFigCanvas2

DASH_WIDTH = 1000
DASH_HEIGHT = 550

RPM_HEIGHT = (2/3)*DASH_HEIGHT
GAUGE_VPOS = 340
GAUGE_HEIGHT = 140
GAUGE_WIDTH = 200

class Charge(QMainWindow):
    def __init__(self, parent=None):
        super(Charge, self).__init__(parent)

        self.setWindowTitle('BOLT CHARGING SCREEN')
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
        self.layout = Layouts(self)
        self.setCentralWidget(self.layout)

        #temporary to make sure the screen is unique
        #self.socGrapher = CustomFigCanvas()
        #self.socGrapher.move(0,16.0)
        #self.socGrapher.show()
        # self.socGauge = Soc(self)
        # self.socGauge.move(850,GAUGE_VPOS-300.0)
        # self.socGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2.5)
        # self.tempGauge = Temp(self)
        # self.tempGauge.move(850,GAUGE_VPOS - 150.0)
        # self.tempGauge.resize(GAUGE_WIDTH,GAUGE_HEIGHT*2.5)
        # self.tempGauge.show()
        #SET GUAGES/GRAPHS FOR CHARGING SCREEN HERE

    #These are the slots that are called when a value is updated (connections made in main.py)
    @pyqtSlot(float)
    def soc_update(self, value):
        self.layout.data.soc_value(value) #calling these functions changes the value on the GUI
    @pyqtSlot(float)
    def highCellTemp_update(self, value):
        self.layout.data.highCellTemp_value(value)
    @pyqtSlot(float)
    def lowCellTemp_update(self, value):
        self.layout.data.lowCellTemp_value(value)


class Layouts(QWidget):
    def __init__(self, parent):
        super(Layouts, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.data = Data(self)
        #self.graph = Graph(self)
        self.graphs = graphTabs(self)
        #self.layout.addWidget(self.graph)
        self.layout.addWidget(self.graphs)
        self.layout.addWidget(self.data)
        self.setLayout(self.layout)

class Data(QWidget):
    def __init__(self,parent):
        super(Data, self).__init__(parent)
        self.data = QGridLayout(self)
        #self.setStyleSheet("background-color: grey")
        self.title = QLabel("Charging Data")
        self.title.setStyleSheet('font: bold Arial')
        self.title.setStyleSheet('color: white')

        self.SoC = QLabel("State of Charge:")
        self.SoC.setStyleSheet('color: white')

        self.hiTemp = QLabel("High Cell Temp")
        self.hiTemp.setStyleSheet('color: white')

        self.hiTempData = QLabel("(Data here)")
        self.hiTempData.setStyleSheet('color: white')

        self.hiId = QLabel("High Cell Temp ID:")
        self.hiId.setStyleSheet('color: white')

        self.lowTemp = QLabel("Low Cell Temp:")
        self.lowTemp.setStyleSheet('color: white')

        self.lowId = QLabel("Low Cell Temp ID:")
        self.lowId.setStyleSheet('color: white')

        self.voltage = QLabel("Voltage:")
        self.voltage.setStyleSheet('color: white')

        self.soc_value_charge = QLCDNumber(self)
        self.soc_value_charge.display(0.0)
        self.soc_value_charge.setFrameShape(QFrame.NoFrame)
        self.soc_value_charge.setSegmentStyle(QLCDNumber.Flat)

        self.high_cell_temp_value_charge = QLCDNumber(self)
        self.high_cell_temp_value_charge.display(0.0)
        self.high_cell_temp_value_charge.setFrameShape(QFrame.NoFrame)
        self.high_cell_temp_value_charge.setSegmentStyle(QLCDNumber.Flat)

        self.low_cell_temp_value_charge = QLCDNumber(self)
        self.low_cell_temp_value_charge.display(0.0)
        self.low_cell_temp_value_charge.setFrameShape(QFrame.NoFrame)
        self.low_cell_temp_value_charge.setSegmentStyle(QLCDNumber.Flat)

        self.title.setAlignment(Qt.AlignCenter)
        self.data.addWidget(self.title,0,0,1,2)
        self.data.addWidget(self.SoC,1,0)
        self.data.addWidget(self.soc_value_charge, 1, 1) #adding state of charge value
        self.data.addWidget(self.hiTemp,2,0)
        self.data.addWidget(self.high_cell_temp_value_charge, 2, 1) #adding the high cell temp value
        self.data.addWidget(self.hiId,3,0)
        self.data.addWidget(self.lowTemp,4,0)
        self.data.addWidget(self.low_cell_temp_value_charge, 4, 1) #adding the low cell temp value
        self.data.addWidget(self.lowId,5,0)
        self.data.addWidget(self.voltage,6,0)
        self.setLayout(self.data)

    #these functions, when called, are what actually change the value shown on the GUI
    def soc_value(self, value):
        self.soc_value_charge.display(value)
        self.value = value
        self.update()
    def highCellTemp_value(self, value):
        self.high_cell_temp_value_charge.display(value)
        self.value = value
        self.update()
    def lowCellTemp_value(self, value):
        self.low_cell_temp_value_charge.display(value)
        self.value = value
        self.update()

class Graph(QWidget):
    def __init__(self,parent):
        super(Graph, self).__init__(parent)
        self.graph = QVBoxLayout(self)
        self.setStyleSheet("background-color: green")
        self.title = QLabel("Graph Goes Here")
        self.graph.addWidget(self.title)
        self.setLayout(self.graph)


class graphTabs(QTabWidget):
    def __init__(self,parent):
        super(graphTabs,self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1,"SoC")
        self.addTab(self.tab2,"Voltage")
        self.setStyleSheet("background-color: gray")
        self.socGraph()
        self.voltGraph()

    def socGraph(self):
        self.graph = QGridLayout(self)
        self.fig = CustomFigCanvas1()
        self.graph.addWidget(self.fig)
        self.setLayout(self.graph)
        self.tab1.setLayout(self.graph)

    def voltGraph(self):

        self.graph = QGridLayout(self)
        self.fig = CustomFigCanvas2()
        self.graph.addWidget(self.fig)
        self.setLayout(self.graph)
        self.tab2.setLayout(self.graph)
