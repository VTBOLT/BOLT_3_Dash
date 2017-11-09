import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QRect

DEMO = False
DOTS = False
if len(sys.argv) > 1:
    if any("-demo" in s for s in sys.argv):
        DEMO = True
    if any("-dots" in s for s in sys.argv):
        DOTS = True
class Rpm(QWidget):
    def __init__(self, parent):
        super(Rpm, self).__init__(parent)
        
        self.rpmValue = 0
        
        self.rpmLCD = QLCDNumber(self)
        self.rpmLCD.display(str(self.rpmValue).zfill(4))
        self.rpmLCD.move(200,150)
        self.rpmLCD.resize(300,200)
        self.rpmLCD.setFrameStyle(QFrame.NoFrame)
        self.rpmLCD.setSegmentStyle(QLCDNumber.Flat)
        
        self.rpmLabel = QLabel(self)
        self.rpmLabel.setText("rpm (x1000): ")
        self.rpmLabel.move(200,130)
        self.rpmLabel.hide()
        
        if DEMO:
            self.rpmLabel.show()

    @pyqtSlot(int)
    def rpm_update(self, value):
        self.rpmLCD.display(str(value/1000).zfill(4))
        self.rpmValue = value
        
        self.update()

            
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        size = self.size()

        if DOTS:
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
            qp.drawRect(20,40,760,80)
            if self.rpmValue < 6000:
                qp.setBrush(Qt.green)
            elif self.rpmValue >= 6000:
                qp.setBrush(Qt.red)
            qp.drawRect(20,40, 760*(self.rpmValue/8000) ,80) #repaints rect every time self.update() is called

        
