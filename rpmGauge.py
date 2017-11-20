import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
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
        qp.setPen(Qt.white)
        size = self.size()

        if self.arguments.Args.dots:
            qp.drawRect(40,40,40,40)
            qp.drawRect(140,40,40,40)
            qp.drawRect(240,40,40,40)
            qp.drawRect(340,40,40,40)
            qp.drawRect(440,40,40,40)
            qp.drawRect(540,40,40,40)
            qp.drawRect(640,40,40,40)
            qp.drawRect(740,40,40,40)

            qp.setBrush(Qt.green)
            if self.rpmValue < 1000:
                qp.drawRect(40,40,40,40)
            elif self.rpmValue < 2000:
                qp.drawRect(40,40,40,40)
                qp.drawRect(140,40,40,40)
            elif self.rpmValue < 3000:
                qp.drawRect(40,40,40,40)
                qp.drawRect(140,40,40,40)
                qp.drawRect(240,40,40,40)
            elif self.rpmValue < 4000:
                qp.drawRect(40,40,40,40)
                qp.drawRect(140,40,40,40)
                qp.drawRect(240,40,40,40)
                qp.drawRect(340,40,40,40)
            elif self.rpmValue < 5000:
                qp.drawRect(40,40,40,40)
                qp.drawRect(140,40,40,40)
                qp.drawRect(240,40,40,40)
                qp.drawRect(340,40,40,40)
                qp.drawRect(440,40,40,40)
            elif self.rpmValue < 6000:
                qp.drawRect(40,40,40,40)
                qp.drawRect(140,40,40,40)
                qp.drawRect(240,40,40,40)
                qp.drawRect(340,40,40,40)
                qp.drawRect(440,40,40,40)
                qp.drawRect(540,40,40,40)
            elif self.rpmValue < 7000:
                qp.drawRect(40,40,40,40)
                qp.drawRect(140,40,40,40)
                qp.drawRect(240,40,40,40)
                qp.drawRect(340,40,40,40)
                qp.drawRect(440,40,40,40)
                qp.drawRect(540,40,40,40)
                qp.setBrush(Qt.red)
                qp.drawRect(640,40,40,40)
            elif self.rpmValue < 8000:
                qp.drawRect(40,40,40,40)
                qp.drawRect(140,40,40,40)
                qp.drawRect(240,40,40,40)
                qp.drawRect(340,40,40,40)
                qp.drawRect(440,40,40,40)
                qp.drawRect(540,40,40,40)
                qp.setBrush(Qt.red)
                qp.drawRect(640,40,40,40)
                qp.drawRect(740,40,40,40)
                        
        else:
            qp.drawRect(20,40,960,80)
            if self.rpmValue < 6000:
                qp.setBrush(Qt.green)
            elif self.rpmValue >= 6000:
                qp.setBrush(Qt.red)
            qp.drawRect(20,40, 960*(self.rpmValue/8000) ,80) #repaints rect every time self.update() is called

        
