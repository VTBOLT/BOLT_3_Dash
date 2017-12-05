import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame, QApplication, QPushButton
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from gpsGauge import Gps

DEBUG_WIDTH = 600
DEBUG_HEIGHT = 380

CHANNEL_WIDTH = 100
CHANNEL_HEIGHT = 100

class Debug(QWidget):
    def __init__(self, parent):
        super(Debug, self).__init__(parent)

        self.setWindowTitle('DEBUG WINDOW')
        self.setMinimumWidth(DEBUG_WIDTH)
        self.setMinimumHeight(DEBUG_HEIGHT)
        self.initDebug()

    def initDebug(self):
        self.setAutoFillBackground(True)
        self.closeButton = QPushButton("Close", self)
        self.closeButton.move(540,350)
        self.closeButton.resize(50,20)
        self.closeButton.clicked.connect(self.debug_close)

        self.c1 = Channel(self, "Example:",0, 0, 5)
        self.c2 = Channel(self, "Example 2:", 100, 0, 6)
        
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        p.setColor(self.foregroundRole(), Qt.blue)
        self.setPalette(p)

        self.hide()

    @pyqtSlot()
    def debug_open(self):
        self.show()

    @pyqtSlot()
    def debug_close(self):
        self.close()

class Channel(QWidget):
    def __init__(self, parent, name, x, y, value):
        super(Channel, self).__init__(parent)
        
        self.label = QLabel(name, self)
        self.label.resize(CHANNEL_WIDTH,20)
        self.label.move(x,y)
        
        self.gauge = QLCDNumber(self)
        self.gauge.display(value)
        self.gauge.move(x,y+20)
        self.gauge.resize(CHANNEL_WIDTH, CHANNEL_HEIGHT)
        self.gauge.setFrameShape(QFrame.NoFrame)
        self.gauge.setSegmentStyle(QLCDNumber.Flat)

    @pyqtSlot(float)
    def channel_update(self, value):
        self.gauge.display(value)
        self.value = value
        self.update()


#channel to display x,y,z data points
class Channel3(QWidget):
    def __init__(self, parent, name, x, y, value):
        super(Channel3, self).__init__(parent)
        
        self.label = QLabel(name, self)
        self.label.resize(CHANNEL_WIDTH,20)
        self.label.move(x,y)
        
        self.gauge = QLCDNumber(self)
        self.gauge.display(value)
        self.gauge.move(x,y+20)
        self.gauge.resize(CHANNEL_WIDTH, CHANNEL_HEIGHT)
        self.gauge.setFrameShape(QFrame.NoFrame)
        self.gauge.setSegmentStyle(QLCDNumber.Flat)

    @pyqtSlot(float)
    def channel_update(self, value):
        self.gauge.display(value)
        self.value = value
        self.update()        

