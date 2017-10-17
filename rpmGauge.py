import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QRect

class Rpm(QWidget):
    def __init__(self, parent):
        super(Rpm, self).__init__(parent)
        
        self.rpmValue = 0
        
        self.rpmLCD = QLCDNumber(self)
        self.rpmLCD.display(str(self.rpmValue).zfill(4))
        self.rpmLCD.move(200,150)
        self.rpmLCD.resize(200,100)
        self.rpmLCD.setFrameStyle(QFrame.NoFrame)
        self.rpmLCD.setSegmentStyle(QLCDNumber.Flat)
        
        self.rpmLabel = QLabel(self)
        self.rpmLabel.setText("rpm: ")
        self.rpmLabel.move(200,130)
        
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        size = self.size()
        qp.drawRect(50,50,650,50)
        #qp.drawLine(50,50,650,50)#top
        #qp.drawLine(50,100,650,100)#bottom
        #qp.drawLine(650,50,650,100)#right side

        #qp.drawArc(75,100,175,200,16*100,16*150)
        if self.rpmValue < 80:
            qp.setBrush(Qt.green)
        elif self.rpmValue >=80:
            qp.setBrush(Qt.red)
        qp.drawRect(50,50, self.rpmValue*6 ,50) #repaints rect every time self.update() is called

    @pyqtSlot(int)
    def rpm_update(self, value):
        self.rpmLCD.display(str(value).zfill(4))
        self.rpmValue = value
        
        self.update()
        
