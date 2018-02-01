##############################################################################################
## Description: displays tempature values
## Values displayed: Motor controller, motor, highest motor temp, and highest cell tempatures
## Units: Celsius
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
##############################################################################################

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from args import Arg_Class

class Temp(QWidget):
    def __init__(self, parent):

        super(Temp, self).__init__(parent)

        self.arguments = Arg_Class()
        
        self.mcTempValue = 0
        self.motorTempValue = 0
        self.highMotorTempValue = 0
        self.highCellTempValue = 0
        self.lowCellTempValue = 0
        
        self.mcTempGauge = QLCDNumber(self)
        self.mcTempGauge.display(str(self.mcTempValue).zfill(1))
        self.mcTempGauge.move(0,0)
        self.mcTempGauge.resize(100,80)
        self.mcTempGauge.setFrameShape(QFrame.NoFrame)
        self.mcTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.mcTemplabel = QLabel(self)
        self.mcTemplabel.setText("highest mc temp: ")
        self.mcTemplabel.move(0,0)

        self.motorTempGauge = QLCDNumber(self)
        self.motorTempGauge.display(str(self.motorTempValue).zfill(1))
        self.motorTempGauge.move(0,60)
        self.motorTempGauge.resize(100,80)
        self.motorTempGauge.setFrameShape(QFrame.NoFrame)
        self.motorTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.motorTemplabel = QLabel(self)
        self.motorTemplabel.setText("motor temp: ")
        self.motorTemplabel.move(0,60)

        self.highMotorTempGauge = QLCDNumber(self)
        self.highMotorTempGauge.display(str(self.highMotorTempValue).zfill(1))
        self.highMotorTempGauge.move(0,120)
        self.highMotorTempGauge.resize(100,80)
        self.highMotorTempGauge.setFrameShape(QFrame.NoFrame)
        self.highMotorTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.highMotorTemplabel = QLabel(self)
        self.highMotorTemplabel.setText("highest motor temp: ")
        self.highMotorTemplabel.move(0,120)

        self.highCellTempGauge = QLCDNumber(self)
        self.highCellTempGauge.display(str(self.highCellTempValue).zfill(1))
        self.highCellTempGauge.move(0,180)
        self.highCellTempGauge.resize(100,80)
        self.highCellTempGauge.setFrameShape(QFrame.NoFrame)
        self.highCellTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.highCellTemplabel = QLabel(self)
        self.highCellTemplabel.setText("highest cell temp: ")
        self.highCellTemplabel.move(0,180)

        self.lowCellTempGauge = QLCDNumber(self)
        self.lowCellTempGauge.display(str(self.lowCellTempValue).zfill(1))
        self.lowCellTempGauge.move(0,240)
        self.lowCellTempGauge.resize(100,80)
        self.lowCellTempGauge.setFrameShape(QFrame.NoFrame)
        self.lowCellTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.lowCellTemplabel = QLabel(self)
        self.lowCellTemplabel.setText("lowest cell temp: ")
        self.lowCellTemplabel.move(0,240)

    @pyqtSlot(float)
    def mcTemp_update(self, value):
        self.mcTempGauge.display(value)
    @pyqtSlot(float)
    def motorTemp_update(self, value):
        self.motorTempGauge.display(value)
    @pyqtSlot(float)
    def highMotorTemp_update(self, value):
        self.highMotorTempGauge.display(value)
    @pyqtSlot(float)
    def highCellTemp_update(self, value):
        self.highCellTempGauge.display(value)
    @pyqtSlot(float)
    def lowCellTemp_update(self, value):
        self.lowCellTempGauge.display(value)
