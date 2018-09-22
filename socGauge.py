############################################################################################################
## Description: displays State of Charge values
## Values displayed: SOC, battery level gauge
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
############################################################################################################

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from args import Arg_Class

class Soc(QWidget):
    def __init__(self, parent):

        super(Soc, self).__init__(parent)

        self.arguments = Arg_Class()

        self.socValue = 0.0

        self.socLCD = QLCDNumber(self)
        self.socLCD.display(str(int(self.socValue)).zfill(4)+'.'+str((self.socValue - int(self.socValue))*10).zfill(4))
        self.socLCD.setFrameShape(QFrame.NoFrame)
        self.socLCD.setSegmentStyle(QLCDNumber.Flat)
        #self.socLCD.move(30,100)
        self.socLCD.move(0,20)
        self.socLCD.resize(70,80)

        self.socLabel = QLabel(self)
        self.socLabel.setText("soc: ")
        self.socLabel.move(10,10)
        self.socLCD.show()
        self.socLabel.show()

    @pyqtSlot(float)
    def soc_update(self, value):
        self.socLCD.display(value)
        self.socValue = value
        self.update()
        #self.socGauge.display(str(int(self.socValue)).zfill(2)+'.'+ str((self.socValue - int(self.socValue))*10).zfill(2))

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)

        qp.drawRect(70,20, 70, 180)
        qp.drawRect(96,10, 20, 10)
        if self.socValue < 0:
            self.socValue = 0
        if self.socValue < 20:
            qp.setBrush(Qt.red)
        else:
            qp.setBrush(Qt.green)

        qp.drawRect(70, 20+(180*(1-(self.socValue/100))), 70, ((180*self.socValue/100)))
        #qp.drawRect(60+(150*(1-(self.socValue/100))), 40, ((150*self.socValue/100)),60)#horizontal bar


