##############################################################################################
## Description: displays error values and dcl
## Values displayed: errors and dcl
## Units: amps
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Spring 2018
## Modified: Spring 2018
##############################################################################################

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from args import Arg_Class

class Error(QWidget):
    def __init__(self, parent):

        super(Error, self).__init__(parent)

        self.arguments = Arg_Class()

        p = self.palette()
        p.setColor(self.foregroundRole(), Qt.blue)
        self.setPalette(p)

        self.rpmCutValue = 0
        self.rpmCutValuePrev = 0
        self.cutFlag = 0
        
        self.DCLValue = 0
        
        self.DCLGauge = QLCDNumber(self)
        self.DCLGauge.display(str(self.DCLValue).zfill(1))
        self.DCLGauge.move(200,0)
        self.DCLGauge.resize(80,80)
        self.DCLGauge.setFrameShape(QFrame.NoFrame)
        self.DCLGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.DCLlabel = QLabel(self)
        self.DCLlabel.setText("DCL: ")
        self.DCLlabel.move(200,0)

        self.PL1ErrorGauge = QLCDNumber(self)
        self.PL1ErrorGauge.display(str(0).zfill(1))
        self.PL1ErrorGauge.move(0,0)
        self.PL1ErrorGauge.resize(80,80)
        self.PL1ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.PL1ErrorGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.PL2ErrorGauge = QLCDNumber(self)
        self.PL2ErrorGauge.display(str(0).zfill(1))
        self.PL2ErrorGauge.move(20,0)
        self.PL2ErrorGauge.resize(80,80)
        self.PL2ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.PL2ErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.PH1ErrorGauge = QLCDNumber(self)
        self.PH1ErrorGauge.display(str(0).zfill(1))
        self.PH1ErrorGauge.move(40,0)
        self.PH1ErrorGauge.resize(80,80)
        self.PH1ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.PH1ErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.PH2ErrorGauge = QLCDNumber(self)
        self.PH2ErrorGauge.display(str(0).zfill(1))
        self.PH2ErrorGauge.move(60,0)
        self.PH2ErrorGauge.resize(80,80)
        self.PH2ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.PH2ErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.RL1ErrorGauge = QLCDNumber(self)
        self.RL1ErrorGauge.display(str(0).zfill(1))
        self.RL1ErrorGauge.move(0,25)
        self.RL1ErrorGauge.resize(80,80)
        self.RL1ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.RL1ErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.RL2ErrorGauge = QLCDNumber(self)
        self.RL2ErrorGauge.display(str(0).zfill(1))
        self.RL2ErrorGauge.move(20,25)
        self.RL2ErrorGauge.resize(80,80)
        self.RL2ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.RL2ErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.RH1ErrorGauge = QLCDNumber(self)
        self.RH1ErrorGauge.display(str(0).zfill(1))
        self.RH1ErrorGauge.move(40,25)
        self.RH1ErrorGauge.resize(80,80)
        self.RH1ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.RH1ErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.RH2ErrorGauge = QLCDNumber(self)
        self.RH2ErrorGauge.display(str(0).zfill(1))
        self.RH2ErrorGauge.move(60,25)
        self.RH2ErrorGauge.resize(80,80)
        self.RH2ErrorGauge.setFrameShape(QFrame.NoFrame)
        self.RH2ErrorGauge.setSegmentStyle(QLCDNumber.Flat)
        # self.RH2ErrorGauge.setDigitCount(4)
        
        self.errorlabel = QLabel(self)
        self.errorlabel.setText("Error code: ")
        self.errorlabel.move(0,0)

        self.rpmCutGauge = QLCDNumber(self)
        self.rpmCutGauge.display(str(self.DCLValue).zfill(1))
        self.rpmCutGauge.move(300,0)
        self.rpmCutGauge.resize(100,100)
        self.rpmCutGauge.setFrameShape(QFrame.NoFrame)
        self.rpmCutGauge.setSegmentStyle(QLCDNumber.Flat)
        self.rpmCutGauge.hide()
        
        self.rpmCutLabel = QLabel(self)
        self.rpmCutLabel.setText("RPM Before Cut: ")
        self.rpmCutLabel.move(300,0)
        self.rpmCutLabel.hide()


    @pyqtSlot(float)
    def DCL_update(self, value):
        self.DCLGauge.display(value)

    @pyqtSlot(float)
    def RPMCut_update(self, value):
        rpmCutValue = value
        if value > 10 and self.cutFlag == 0:
            self.rpmCutGauge.hide()
            #self.rpmCutGauge.display(value)
            self.rpmCutValuePrev = value
        else:
            self.rpmCutGauge.display(self.rpmCutValuePrev)
            self.rpmCutGauge.show()
            self.rpmCutLabel.show()
            self.cutFlag = 1

    @pyqtSlot(int, int, int, int)
    def error_update(self, value1, value2, value3, value4):
        self.PL1ErrorGauge.display(value1 >> 8)
        self.PL2ErrorGauge.display(value1 & 0xFF)
        self.PH1ErrorGauge.display(value2 >> 8)
        self.PH2ErrorGauge.display(value2 & 0xFF)
        self.RL1ErrorGauge.display(value3 >> 8)
        self.RL2ErrorGauge.display(value3 & 0xFF)
        self.RH1ErrorGauge.display(value4 >> 8)
        self.RH2ErrorGauge.display(value4 & 0xFF)
        
