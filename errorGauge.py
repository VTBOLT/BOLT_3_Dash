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
from enum import IntEnum
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from args import Arg_Class

class Error(QWidget):
    class FaultLevel(IntEnum):
        LOW = 0
        MID = 1
        HIGH = 2
    fault_set = set()
    # run faults (low byte) dict
    run_lo_fault_dict = {
                        0x0001: ('Motor Over-speed Fault', FaultLevel.LOW),
                        0x0002: ('Over-current Fault', FaultLevel.HIGH),
                        0x0004: ('Over-voltage', FaultLevel.HIGH),
                        0x0008: ('Inverter Over-temperature Fault', FaultLevel.MID),
                        0x0010: ('Accelerator Input Shorted Fault', FaultLevel.MID),
                        0x0020: ('Accelerator Input Open Fault', FaultLevel.MID),
                        0x0080: ('Inverter Response Time-out Fault', FaultLevel.LOW),
                        0x0100: ('Hardware Gate/Desaturation Fault', FaultLevel.HIGH),
                        0x0200: ('Hardware Over-current Fault', FaultLevel.HIGH),
                        0x0400: ('Under-voltage Fault', FaultLevel.MID),
                        0x0800: ('CAN Command Message Lost Fault', FaultLevel.MID),
                        0x1000: ('Motor Over-temerature Fault', FaultLevel.MID)
                    }

    # run faults (high byte) dict
    run_hi_fault_dict = {
                        0x0001: ('Brake Input Shorted Fault', FaultLevel.LOW),
                        0x0002: ('Brake Input Open Fault', FaultLevel.LOW),
                        0x0004: ('Module A Over-temperature Fault', FaultLevel.MID),
                        0x0008: ('Module B Over-temperature Fualt', FaultLevel.MID),
                        0x0010: ('Module C Over-temperature Fault', FaultLevel.MID),
                        0x0020: ('PCB Over-temperature Fault', FaultLevel.MID),
                        0x0040: ('Gate Drive Board 1 Over-temperature Fault', FaultLevel.MID),
                        0x0080: ('Gate Drive Board 2 Over-temperature Fault', FaultLevel.MID),
                        0x0100: ('Gate Drive Board 3 Over-temperature Fault', FaultLevel.MID),
                        0x0200: ('Current Sensor Fault', FaultLevel.MID),
                        0x4000: ('Resolver Not Connected', FaultLevel.MID)
                    }

    # post faults (low byte) dict
    post_lo_fault_dict = {
                        0x0001: ('Hardware Gate/Desaturation Fault', FaultLevel.LOW),
                        0x0002: ('HW Over-current Fault', FaultLevel.MID),
                        0x0004: ('Accelerator Shorted', FaultLevel.HIGH),
                        0x0008: ('Accelerator Open', FaultLevel.HIGH),
                        0x0010: ('Current Sensor Low', FaultLevel.LOW),
                        0x0020: ('Current Sensor High', FaultLevel.LOW),
                        0x0040: ('Module Temperature Low', FaultLevel.LOW),
                        0x0080: ('Module Temperature High', FaultLevel.LOW),
                        0x0100: ('Control PCB Temperature Low', FaultLevel.LOW),
                        0x0200: ('Control PCB Temperature High', FaultLevel.LOW),
                        0x0400: ('Gate Drive PCB Temperature Low', FaultLevel.LOW),
                        0x0800: ('Gate Drive PCB Temperature High', FaultLevel.LOW),
                        0x1000: ('5V Sense Voltage Low', FaultLevel.LOW),
                        0x2000: ('5V Sense Voltage High', FaultLevel.LOW),
                        0x4000: ('12V Sense Voltage Low', FaultLevel.LOW),
                        0x8000: ('12V Sense Voltage High', FaultLevel.LOW)
                    }

    # post faults (low byte) dict
    post_hi_fault_dict = {
                        0x0001: ('2.5V Sense Voltage Low', FaultLevel.LOW),
                        0x0002: ('2.5V Sense Voltage High', FaultLevel.LOW),
                        0x0004: ('1.5V Sense Voltage Low', FaultLevel.LOW),
                        0x0008: ('1.5V Sense Voltage High', FaultLevel.LOW),
                        0x0010: ('DC Bus Voltage High', FaultLevel.LOW),
                        0x0020: ('DC Bus Voltage Low', FaultLevel.LOW),
                        0x0040: ('Pre-charge Timeout', FaultLevel.MID),
                        0x0080: ('Pre-charge Voltage Failure', FaultLevel.LOW),
                        0x0100: ('EEPROM Checksum Invalid', FaultLevel.LOW),
                        0x0200: ('EEPROM Data Out of Range', FaultLevel.LOW),
                        0x0400: ('EEPROM Update Required', FaultLevel.LOW),
                        0x4000: ('Brake Shorted', FaultLevel.HIGH),
                        0x8000: ('Brake Open', FaultLevel.HIGH)
                    }
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

        self.errorlabel = QLabel(self)
        self.errorlabel.setText("Error: ")
        self.errorlabel.move(0,0)

        self.currErrorLabel = QLabel(self)
        self.currErrorLabel.setText("\t\t\t\t")
        self.currErrorLabel.move(0,20)

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

    @pyqtSlot()
    def error_update(self):
        curr_fault = max(self.fault_set, key=lambda x:x[1])
        self.currErrorLabel.setText(curr_fault[0])        
