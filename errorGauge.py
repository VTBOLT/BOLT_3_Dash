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

        self.rpmCutValue = 0
        self.rpmCutValuePrev = 0
        self.cutFlag = 0
        
        self.DCLValue = 0
        self.errorCodePL = 0 # post low
        self.errorCodePH = 0 # post high
        self.errorCodeRL = 0 # run low
        self.errorCodeRH = 0 # run high
        
        self.DCLGauge = QLCDNumber(self)
        self.DCLGauge.display(str(self.DCLValue).zfill(1))
        self.DCLGauge.move(200,0)
        self.DCLGauge.resize(100,100)
        self.DCLGauge.setFrameShape(QFrame.NoFrame)
        self.DCLGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.DCLlabel = QLabel(self)
        self.DCLlabel.setText("DCL: ")
        self.DCLlabel.move(200,0)

        self.PLErrorGauge = QLCDNumber(self)
        self.PLErrorGauge.display(str(self.errorCodePL).zfill(1))
        self.PLErrorGauge.move(0,0)
        self.PLErrorGauge.resize(100,100)
        self.PLErrorGauge.setFrameShape(QFrame.NoFrame)
        self.PLErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.PHErrorGauge = QLCDNumber(self)
        self.PHErrorGauge.display(str(self.errorCodePH).zfill(1))
        self.PHErrorGauge.move(20,0)
        self.PHErrorGauge.resize(100,100)
        self.PHErrorGauge.setFrameShape(QFrame.NoFrame)
        self.PHErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.RLErrorGauge = QLCDNumber(self)
        self.RLErrorGauge.display(str(self.errorCodeRL).zfill(1))
        self.RLErrorGauge.move(40,0)
        self.RLErrorGauge.resize(100,100)
        self.RLErrorGauge.setFrameShape(QFrame.NoFrame)
        self.RLErrorGauge.setSegmentStyle(QLCDNumber.Flat)

        self.RHErrorGauge = QLCDNumber(self)
        self.RHErrorGauge.display(str(self.errorCodeRH).zfill(1))
        self.RHErrorGauge.move(60,0)
        self.RHErrorGauge.resize(100,100)
        self.RHErrorGauge.setFrameShape(QFrame.NoFrame)
        self.RHErrorGauge.setSegmentStyle(QLCDNumber.Flat)
        
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
        self.PLErrorGauge.display(value1)
        self.PHErrorGauge.display(value2)
        self.RLErrorGauge.display(value3)
        self.RHErrorGauge.display(value4)
        
