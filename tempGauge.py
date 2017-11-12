import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from args import Arg_Class

class Temp(QWidget):
    def __init__(self, parent):

        super(Temp, self).__init__(parent)
                 
        self.mcTempValue = 0
        self.motorTempValue = 0
        self.cellTempValue = 0
        
        self.mcTempGauge = QLCDNumber(self)
        self.mcTempGauge.display(str(self.mcTempValue).zfill(1))
        self.mcTempGauge.move(0,0)
        self.mcTempGauge.resize(100,100)
        self.mcTempGauge.setFrameShape(QFrame.NoFrame)
        self.mcTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.mcTemplabel = QLabel(self)
        self.mcTemplabel.setText("highest mc temp: ")
        self.mcTemplabel.move(0,0)

        self.motorTempGauge = QLCDNumber(self)
        self.motorTempGauge.display(str(self.motorTempValue).zfill(1))
        self.motorTempGauge.move(0,80)
        self.motorTempGauge.resize(100,100)
        self.motorTempGauge.setFrameShape(QFrame.NoFrame)
        self.motorTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.motorTemplabel = QLabel(self)
        self.motorTemplabel.setText("motor temp: ")
        self.motorTemplabel.move(0,80)

        self.highMotorTempGauge = QLCDNumber(self)
        self.highMotorTempGauge.display(str(self.motorTempValue).zfill(1))
        self.highMotorTempGauge.move(0,180)
        self.highMotorTempGauge.resize(100,100)
        self.highMotorTempGauge.setFrameShape(QFrame.NoFrame)
        self.highMotorTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.highMotorTemplabel = QLabel(self)
        self.highMotorTemplabel.setText("highest motor temp: ")
        self.highMotorTemplabel.move(0,180)

        self.cellTempGauge = QLCDNumber(self)
        self.cellTempGauge.display(str(self.cellTempValue).zfill(1))
        self.cellTempGauge.move(0,280)
        self.cellTempGauge.resize(100,100)
        self.cellTempGauge.setFrameShape(QFrame.NoFrame)
        self.cellTempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.cellTemplabel = QLabel(self)
        self.cellTemplabel.setText("highest cell temp: ")
        self.cellTemplabel.move(0,280)
        
    @pyqtSlot(float)
    def mcTemp_update(self, value):
        self.mcTempGauge.display(value)
    @pyqtSlot(float)
    def motorTemp_update(self, value):
        self.motorTempGauge.display(vale)
    @pyqtSlot(float)
    def cellTemp_update(self, value):
        self.cellTempGauge.display(value)
        
    '''
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        qp.drawRect(20,110,100,20)
        qp.drawLine(70, 104, 70, 136)
        qp.drawLine(90, 104, 90, 136)

        qp.setBrush(Qt.green)
        qp.drawRect(80,110,5,20)
    '''
