############################################################################################################
## Description: displays rpm values
## Values displayed: RPM, tachometer
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Winter 2017
## TODO: add white box around tachometer, add flag for antialiasing
############################################################################################################

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QGradient, QBrush, QLinearGradient, QConicalGradient
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QRect

from args import Arg_Class

class Rpm(QWidget):
    def __init__(self, parent):
        super(Rpm, self).__init__(parent)

        self.arguments = Arg_Class()
        
        self.rpmValue = 0
        
        self.rpmLCD = QLCDNumber(self)
        self.rpmLCD.display(str(10*int(self.rpmValue/10)).zfill(4))
        self.rpmLCD.move(250,150)
        self.rpmLCD.resize(300,200)
        self.rpmLCD.setFrameStyle(QFrame.NoFrame)
        self.rpmLCD.setSegmentStyle(QLCDNumber.Flat)
        
        self.rpmLabel = QLabel(self)
        self.rpmLabel.setText("rpm (x1000): ")
        self.rpmLabel.move(3100,130)
        self.rpmLabel.hide()

        self.rpmLabel.show()
        if self.arguments.Args.demo:
            self.rpmLabel.show()

    @pyqtSlot(int)
    def rpm_update(self, value):
        self.rpmLCD.display(str(10*int(value/10)).zfill(4))#displays rpm, reduces precision to imporve readablity 
        self.rpmValue = value        
        self.update()

            
    def paintEvent(self, event):
        qp = QPainter(self)

        #Antialiasing smooths the edges of the graphics, TODO: add a flag so its not set everytime, should help preformence 
        qp.setRenderHints(QPainter.Antialiasing)

        qp.setPen(Qt.white)
        #qp.drawArc(130, 160, 100, 150, 255*16, -135*16)
        #qp.drawArc(170, 160, 100, 150, 255*16, -135*16)
        
        QT_ANGLE_MULTI = 16 # Qt measures angles in 1/16th incraments
        MAX_RPM = 8500
        ARC_TO_TOTAL_RATIO = 2
        ARC_WIDTH = 500
        ARC_HEIGHT = 150
        ARC_HPOS = 150
        ARC_VPOS = 160
        BRUSH_WIDTH = ARC_WIDTH*.1
        GRADIENT_ANGLE = 0.0

        #Gradient Color setup
        # red-blueValue are the main color in the tachometer
        # lineStart... make the transition between the arc and line sections smooth
        gradProp = (360.0 - (90.0 - GRADIENT_ANGLE))/360.0
        redValue = 0
        greenValue = 255
        blueValue = 0
        lineStartRed = redValue + (( 255-redValue) * (1.0-gradProp))
        lineStartGreen = greenValue + (( 255-greenValue) * (1.0-gradProp))
        lineStartBlue = blueValue + (( 255-blueValue) * (1.0-gradProp))
        
        startAngle = 225*QT_ANGLE_MULTI # completly arbitary but it looks decent
        spanAngle = -( (self.rpmValue / MAX_RPM*ARC_TO_TOTAL_RATIO)*135 ) * QT_ANGLE_MULTI # Span angle is the amount of an ellipse that is drawn, if set to 360 a full ellipse is drawn, if 360/4 a quarter is drawn
        # 135 is another arbirtary value
        
        if spanAngle > 0:
            spanAngle = 0
        elif spanAngle < -(135*QT_ANGLE_MULTI):
            spanAngle = -(135*QT_ANGLE_MULTI)

        rectLength = ((self.rpmValue-MAX_RPM*.5) / MAX_RPM*2)*ARC_WIDTH
        if rectLength < 0:
            rectLength = 0

        gradArc = QConicalGradient(ARC_HPOS+50, ARC_VPOS+50, 0)
        if self.rpmValue > 6500:
            gradArc.setColorAt(0, QColor(redValue,greenValue,blueValue))
            gradArc.setColorAt(1, QColor(255,255,255))
        else:
            gradArc.setColorAt(0, QColor(redValue,greenValue,blueValue))
            gradArc.setColorAt(1, QColor(255,255,255))

        arcPen = QPen(QBrush(gradArc), BRUSH_WIDTH)# color and thickness, TODO: QBrush should be set to a graident 
        arcPen.setCapStyle(Qt.FlatCap)
        qp.setPen(arcPen)

        qp.drawArc(ARC_HPOS, ARC_VPOS, ARC_WIDTH/4, ARC_HEIGHT, startAngle, spanAngle)
        
        gradLine = QLinearGradient(ARC_HPOS+(ARC_WIDTH*.1+10), ARC_VPOS, rectLength+(ARC_WIDTH/2), ARC_VPOS)
        if self.rpmValue > 6500:
            gradLine.setColorAt(0, QColor(lineStartRed, lineStartGreen, lineStartBlue))
            gradLine.setColorAt(1, Qt.red)
        else:
            gradLine.setColorAt(0, QColor(lineStartRed, lineStartGreen, lineStartBlue))
            gradLine.setColorAt(1, QColor(redValue,greenValue,blueValue))
            
        linePen = QPen(QBrush(gradLine), BRUSH_WIDTH)# color and thickness, TODO: QBrush should be set to a graident 
        linePen.setCapStyle(Qt.FlatCap)
        qp.setPen(linePen)

        
        if rectLength > 0:
            qp.drawLine(ARC_HPOS+(ARC_WIDTH*.1+10), ARC_VPOS, rectLength+(ARC_WIDTH/2), ARC_VPOS)        
