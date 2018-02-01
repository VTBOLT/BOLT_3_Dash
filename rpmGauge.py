############################################################################################################
## Description: displays rpm values
## Values displayed: RPM, tachometer
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Winter 2017
## TODO: add white box around tachometer, add flag for antialiasing, add lowpass filter on rpm
############################################################################################################

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QGradient, QBrush, QLinearGradient, QConicalGradient, QPainterPath, QPalette, QFont
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

        self.rpmLabelFont = QFont("Helvetica", 20)

        self.rpmLabel = QLabel(self)
        self.rpmLabel.setText("x1000 r/min")
        self.rpmLabel.setFont(self.rpmLabelFont)
        self.rpmLabel.move(4.0, 4.0)
        self.rpmLabel.show()

        self.labelFont = QFont("Helvetica", 28, QFont.Bold, QFont.StyleItalic)

        x = 4.0
        y = 250.0

        #bar1
        xb = 4.0
        yb = 360.0
        self.leftx1 = xb
        self.lefty1 = yb
        self.bar1 = QPainterPath()
        self.bar1.moveTo(xb, yb)
        self.bar1.lineTo(xb, y + 8.0)
        xb += 44.0
        yb -= 50.0
        self.rightx1 = xb
        self.righty1 = yb
        self.bar1.lineTo(xb, y - 50.0 + 8.0)
        self.bar1.lineTo(xb, yb)
        self.bar1.lineTo(xb - 44.0, yb + 50.0)
        self.bar1.closeSubpath()

        #1st seg
        x = 4.0
        y = 250.0
        self.guage1 = QPainterPath()
        self.guage1.moveTo(x, y)
        self.guage1.moveTo(x, y - 8.0)
        x += 44.0
        y -= 50.0
        self.guage1.lineTo(x , y - 8.0)
        self.guage1.lineTo(x, y)
        self.guage1.lineTo(x - 44.0, y + 50.0)
        self.guage1.closeSubpath()
        self.label1 = QLabel(self)
        self.label1.setText("1")
        self.label1.setFont(self.labelFont)
        self.label1.move(x - 10.0, y - 48.0)
        self.label1.show()

        #bar2
        x += 4.0
        y -= 3.0
        xb += 4.0
        yb -= 3.0
        self.leftx2 = xb
        self.lefty2 = yb
        self.bar2 = QPainterPath()
        self.bar2.moveTo(xb, yb)
        self.bar2.lineTo(xb, y + 8.0)
        xb += 56.0
        yb -= 50.0
        self.rightx2 = xb
        self.righty2 = yb
        self.bar2.lineTo(xb, y - 50.0 + 8.0)
        self.bar2.lineTo(xb, yb)
        self.bar2.lineTo(xb - 56.0, yb + 50.0)
        self.bar2.closeSubpath()

        #2nd seg
        self.guage2 = QPainterPath()
        self.guage2.moveTo(x, y)
        self.guage2.moveTo(x, y - 8.0)
        x += 56.0
        y -= 50.0
        self.guage2.lineTo(x , y - 8.0)
        self.guage2.lineTo(x, y)
        self.guage2.lineTo(x - 56.0, y + 50.0)
        self.guage2.closeSubpath()
        self.label2 = QLabel(self)
        self.label2.setText("2")
        self.label2.setFont(self.labelFont)
        self.label2.move(x - 10.0, y - 50.0)
        self.label2.show()

        #bar3
        x += 4.0
        y -= 3.0
        xb += 4.0
        yb -= 3.0
        self.leftx3 = xb
        self.lefty3 = yb
        self.bar3 = QPainterPath()
        self.bar3.moveTo(xb, yb)
        self.bar3.lineTo(xb, y + 8.0)
        xb += 78.0
        yb -= 44.0
        self.rightx3 = xb
        self.righty3 = yb
        self.bar3.lineTo(xb, y - 44.0 + 8.0)
        self.bar3.lineTo(xb, yb)
        self.bar3.lineTo(xb - 78.0, yb + 44.0)
        self.bar3.closeSubpath()

        #3rd seg
        self.guage3 = QPainterPath()
        self.guage3.moveTo(x, y)
        self.guage3.moveTo(x, y - 8.0)
        x += 78.0
        y -= 44.0
        self.guage3.lineTo(x , y - 8.0)
        self.guage3.lineTo(x, y)
        self.guage3.lineTo(x - 78.0, y + 44.0)
        self.guage3.closeSubpath()
        self.label3 = QLabel(self)
        self.label3.setText("3")
        self.label3.setFont(self.labelFont)
        self.label3.move(x - 10.0, y - 48.0)
        self.label3.show()

        #bar4
        x += 4.0
        y -= 1.0
        xb += 4.0
        yb -= 1.0
        self.leftx4 = xb
        self.lefty4 = yb
        self.bar4 = QPainterPath()
        self.bar4.moveTo(xb, yb)
        self.bar4.lineTo(xb, y + 8.0)
        xb += 108.0
        yb -= 36.0
        self.rightx4 = xb
        self.righty4 = yb
        self.bar4.lineTo(xb, y - 36.0 + 8.0)
        self.bar4.lineTo(xb, yb)
        self.bar4.lineTo(xb - 108.0, yb + 36.0)
        self.bar4.closeSubpath()

        #4th seg
        self.guage4 = QPainterPath()
        self.guage4.moveTo(x, y)
        self.guage4.moveTo(x, y - 8.0)
        x += 108.0
        y -= 36.0
        self.guage4.lineTo(x , y - 8.0)
        self.guage4.lineTo(x, y)
        self.guage4.lineTo(x - 108.0, y + 36.0)
        self.guage4.closeSubpath()
        self.label4 = QLabel(self)
        self.label4.setText("4")
        self.label4.setFont(self.labelFont)
        self.label4.move(x - 10.0, y - 48.0)
        self.label4.show()

        #bar5
        x += 4.0
        y -= 1.0
        xb += 4.0
        yb -= 1.0
        self.leftx5 = xb
        self.lefty5 = yb
        self.bar5 = QPainterPath()
        self.bar5.moveTo(xb, yb)
        self.bar5.lineTo(xb, y + 8.0)
        xb += 136.0
        yb -= 16.0
        self.rightx5 = xb
        self.righty5 = yb
        self.bar5.lineTo(xb, y - 16.0 + 8.0)
        self.bar5.lineTo(xb, yb)
        self.bar5.lineTo(xb - 136.0, yb + 16.0)
        self.bar5.closeSubpath()

        #5th seg
        self.guage5 = QPainterPath()
        self.guage5.moveTo(x, y)
        self.guage5.moveTo(x, y - 8.0)
        x += 136.0
        y -= 16.0
        self.guage5.lineTo(x , y - 8.0)
        self.guage5.lineTo(x, y)
        self.guage5.lineTo(x - 136.0, y + 16.0)
        self.guage5.closeSubpath()
        self.label5 = QLabel(self)
        self.label5.setText("5")
        self.label5.setFont(self.labelFont)
        self.label5.move(x - 8.0, y - 48.0)
        self.label5.show()

        #bar6
        x += 4.0
        y -= 0.0
        xb += 4.0
        yb -= 0.0
        self.leftx6 = xb
        self.lefty6 = yb
        self.bar6 = QPainterPath()
        self.bar6.moveTo(xb, yb)
        self.bar6.lineTo(xb, y + 8.0)
        xb += 164.0
        yb -= 0.0
        self.rightx6 = xb
        self.righty6 = yb
        self.bar6.lineTo(xb, y - 0.0 + 8.0)
        self.bar6.lineTo(xb, yb)
        self.bar6.lineTo(xb - 164.0, yb + 0.0)
        self.bar6.closeSubpath()

        #6th seg
        self.guage6 = QPainterPath()
        self.guage6.moveTo(x, y)
        self.guage6.moveTo(x, y - 8.0)
        x += 164.0
        y -= 0.0
        self.guage6.lineTo(x , y - 8.0)
        self.guage6.lineTo(x, y)
        self.guage6.lineTo(x - 164.0, y + 0.0)
        self.guage6.closeSubpath()
        self.label6 = QLabel(self)
        self.label6.setText("6")
        self.label6.setFont(self.labelFont)
        self.label6.move(x - 6.0, y - 46.0)
        self.label6.show()

        #bar7
        x += 4.0
        y -= 0.0
        xb += 4.0
        yb -= 0.0
        self.leftx7 = xb
        self.lefty7 = yb
        self.bar7 = QPainterPath()
        self.bar7.moveTo(xb, yb)
        self.bar7.lineTo(xb, y + 8.0)
        xb += 148.0
        yb -= 0.0
        self.rightx7 = xb
        self.righty7 = yb
        self.bar7.lineTo(xb, y - 0.0 + 8.0)
        self.bar7.lineTo(xb, yb)
        self.bar7.lineTo(xb - 148.0, yb + 0.0)
        self.bar7.closeSubpath()

        #7th seg
        self.guage7 = QPainterPath()
        self.guage7.moveTo(x, y)
        self.guage7.moveTo(x, y - 8.0)
        x += 148.0
        y -= 0.0
        self.guage7.lineTo(x , y - 8.0)
        self.guage7.lineTo(x, y)
        self.guage7.lineTo(x - 148.0, y + 0.0)
        self.guage7.closeSubpath()
        self.label7 = QLabel(self)
        self.label7.setText("7")
        self.label7.setFont(self.labelFont)
        self.label7.move(x - 6.0, y - 46.0)
        self.label7.show()

        #bar8
        x += 4.0
        y -= 0.0
        xb += 4.0
        yb -= 0.0
        self.leftx8 = xb
        self.lefty8 = yb
        self.bar8 = QPainterPath()
        self.bar8.moveTo(xb, yb)
        self.bar8.lineTo(xb, y + 8.0)
        xb += 112.0
        yb -= 0.0
        self.rightx8 = xb
        self.righty8 = yb
        self.bar8.lineTo(xb, y - 0.0 + 8.0)
        self.bar8.lineTo(xb, yb)
        self.bar8.lineTo(xb - 112.0, yb + 0.0)
        self.bar8.closeSubpath()

        #8th seg
        self.guage8 = QPainterPath()
        self.guage8.moveTo(x, y)
        self.guage8.moveTo(x, y - 8.0)
        x += 112.0
        y -= 0.0
        self.guage8.lineTo(x , y - 8.0)
        self.guage8.lineTo(x, y)
        self.guage8.lineTo(x - 112.0, y + 0.0)
        self.guage8.closeSubpath()
        self.label8 = QLabel(self)
        self.label8.setText("8")
        self.label8.setFont(self.labelFont)
        self.label8.move(x - 6.0, y - 46.0)
        self.label8.show()

        #bar9
        x += 4.0
        y -= 0.0
        xb += 4.0
        yb -= 0.0
        self.leftx9 = xb
        self.lefty9 = yb
        self.bar9 = QPainterPath()
        self.bar9.moveTo(xb, yb)
        self.bar9.lineTo(xb, y + 8.0)
        xb += 112.0
        yb -= 0.0
        self.rightx9 = xb
        self.righty9 = yb
        self.bar9.lineTo(xb, y - 0.0 + 8.0)
        self.bar9.lineTo(xb, yb)
        self.bar9.lineTo(xb - 112.0, yb + 0.0)
        self.bar9.closeSubpath()

        #9th seg
        self.guage9 = QPainterPath()
        self.guage9.moveTo(x, y)
        self.guage9.moveTo(x, y - 8.0)
        x += 112.0
        y -= 0.0
        self.guage9.lineTo(x , y - 8.0)
        self.guage9.lineTo(x, y)
        self.guage9.lineTo(x - 112.0, y + 0.0)
        self.guage9.closeSubpath()


    @pyqtSlot(int)
    def rpm_update(self, value):
        #self.rpmValue = value
        self.rpmValue = (800 * self.rpmValue + (1024 - 800) * value) >> 10
        if self.rpmValue < 0:
            self.rpmValue = 0
        self.rpmLCD.display(str(10*int(self.rpmValue/10)).zfill(4))#displays rpm, reduces precision to imporve readablity
        self.update()


    def paintEvent(self, event):
        qp = QPainter(self)
        #Antialiasing smooths the edges of the graphics, TODO: add a flag so its not set everytime, should help preformence
        qp.setRenderHints(QPainter.Antialiasing)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)

        qp.drawPath(self.guage1)
        qp.drawPath(self.guage2)
        qp.drawPath(self.guage3)
        qp.drawPath(self.guage4)
        qp.drawPath(self.guage5)
        qp.drawPath(self.guage6)
        qp.drawPath(self.guage7)
        qp.drawPath(self.guage8)
        qp.drawPath(self.guage9)

        if self.rpmValue > 0.0 and self.rpmValue <= 999:
            rightx = self.leftx1 + (self.rpmValue / 1000.0 * (self.rightx1 - self.leftx1))
            righty = self.lefty1 - (self.rpmValue / 1000.0 * (self.lefty1 - self.righty1))
            bar = QPainterPath()
            bar.moveTo(self.leftx1, self.lefty1)
            bar.lineTo(self.leftx1, self.lefty1 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx1, self.lefty1)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 1000 and self.rpmValue <= 1999:
            qp.drawPath(self.bar1)
            rightx = self.leftx2 + ((self.rpmValue - 1000.0) / 1000.0 * (self.rightx2 - self.leftx2))
            righty = self.lefty2 - ((self.rpmValue - 1000.0) / 1000.0 * (self.lefty2 - self.righty2))
            bar = QPainterPath()
            bar.moveTo(self.leftx2, self.lefty2)
            bar.lineTo(self.leftx2, self.lefty2 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx2, self.lefty2)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 2000 and self.rpmValue <= 2999:
            qp.drawPath(self.bar1)
            qp.drawPath(self.bar2)
            rightx = self.leftx3 + ((self.rpmValue - 2000.0) / 1000.0 * (self.rightx3 - self.leftx3))
            righty = self.lefty3 - ((self.rpmValue - 2000.0) / 1000.0 * (self.lefty3 - self.righty3))
            bar = QPainterPath()
            bar.moveTo(self.leftx3, self.lefty3)
            bar.lineTo(self.leftx3, self.lefty3 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx3, self.lefty3)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 3000 and self.rpmValue <= 3999:
            qp.drawPath(self.bar1)
            qp.drawPath(self.bar2)
            qp.drawPath(self.bar3)
            rightx = self.leftx4 + ((self.rpmValue - 3000.0) / 1000.0 * (self.rightx4 - self.leftx4))
            righty = self.lefty4 - ((self.rpmValue - 3000.0) / 1000.0 * (self.lefty4 - self.righty4))
            bar = QPainterPath()
            bar.moveTo(self.leftx4, self.lefty4)
            bar.lineTo(self.leftx4, self.lefty4 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx4, self.lefty4)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 4000 and self.rpmValue <= 4999:
            qp.drawPath(self.bar1)
            qp.drawPath(self.bar2)
            qp.drawPath(self.bar3)
            qp.drawPath(self.bar4)
            rightx = self.leftx5 + ((self.rpmValue - 4000.0) / 1000.0 * (self.rightx5 - self.leftx5))
            righty = self.lefty5 - ((self.rpmValue - 4000.0) / 1000.0 * (self.lefty5 - self.righty5))
            bar = QPainterPath()
            bar.moveTo(self.leftx5, self.lefty5)
            bar.lineTo(self.leftx5, self.lefty5 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx5, self.lefty5)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 5000 and self.rpmValue <= 5999:
            qp.drawPath(self.bar1)
            qp.drawPath(self.bar2)
            qp.drawPath(self.bar3)
            qp.drawPath(self.bar4)
            qp.drawPath(self.bar5)
            rightx = self.leftx6 + ((self.rpmValue - 5000.0) / 1000.0 * (self.rightx6 - self.leftx6))
            righty = self.righty6
            bar = QPainterPath()
            bar.moveTo(self.leftx6, self.lefty6)
            bar.lineTo(self.leftx6, self.lefty6 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx6, self.lefty6)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 6000 and self.rpmValue <= 6999:
            qp.drawPath(self.bar1)
            qp.drawPath(self.bar2)
            qp.drawPath(self.bar3)
            qp.drawPath(self.bar4)
            qp.drawPath(self.bar5)
            qp.drawPath(self.bar6)
            rightx = self.leftx7 + ((self.rpmValue - 6000.0) / 1000.0 * (self.rightx7 - self.leftx7))
            righty = self.righty7
            bar = QPainterPath()
            bar.moveTo(self.leftx7, self.lefty7)
            bar.lineTo(self.leftx7, self.lefty7 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx7, self.lefty7)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 7000 and self.rpmValue <= 7999:
            qp.drawPath(self.bar1)
            qp.drawPath(self.bar2)
            qp.drawPath(self.bar3)
            qp.drawPath(self.bar4)
            qp.drawPath(self.bar5)
            qp.drawPath(self.bar6)
            qp.drawPath(self.bar7)
            rightx = self.leftx8 + ((self.rpmValue - 7000.0) / 1000.0 * (self.rightx8 - self.leftx8))
            righty = self.righty8
            bar = QPainterPath()
            bar.moveTo(self.leftx8, self.lefty8)
            bar.lineTo(self.leftx8, self.lefty8 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx8, self.lefty8)
            bar.closeSubpath()
            qp.drawPath(bar)
        elif self.rpmValue >= 8000:
            qp.drawPath(self.bar1)
            qp.drawPath(self.bar2)
            qp.drawPath(self.bar3)
            qp.drawPath(self.bar4)
            qp.drawPath(self.bar5)
            qp.drawPath(self.bar6)
            qp.drawPath(self.bar7)
            qp.drawPath(self.bar8)
            rightx = self.leftx9 + ((self.rpmValue - 8000.0) / 1000.0 * (self.rightx9 - self.leftx9))
            righty = self.righty9
            bar = QPainterPath()
            bar.moveTo(self.leftx9, self.lefty9)
            bar.lineTo(self.leftx9, self.lefty9 - 102.0)
            bar.lineTo(rightx, righty - 102.0)
            bar.lineTo(rightx, righty)
            bar.lineTo(self.leftx9, self.lefty9)
            bar.closeSubpath()
            qp.drawPath(bar)
