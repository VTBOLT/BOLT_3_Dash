import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

DEMO = False

if len(sys.argv) > 1:
    if any("-demo" in s for s in sys.argv):
        DEMO = True

class Gps(QWidget):
    def __init__(self, parent):

        super(Gps, self).__init__(parent)

        self.latValue = 5.0
        self.longValue = 3.0

        self.gpsLatLCD = QLCDNumber(self)
        self.gpsLatLCD.display(self.latValue)
        self.gpsLatLCD.setFrameShape(QFrame.NoFrame)
        self.gpsLatLCD.setSegmentStyle(QLCDNumber.Flat)
        self.gpsLatLCD.move(0,0)
        self.gpsLatLCD.resize(100,50)
        self.gpsLatLCD.hide()
        
        self.gpsLatLabel = QLabel(self)
        self.gpsLatLabel.setText("lat: ")
        self.gpsLatLabel.move(0,0)
        self.gpsLatLabel.hide()

        self.gpsLongLCD = QLCDNumber(self)
        self.gpsLongLCD.display(self.longValue)
        self.gpsLongLCD.setFrameShape(QFrame.NoFrame)
        self.gpsLongLCD.setSegmentStyle(QLCDNumber.Flat)
        self.gpsLongLCD.move(200,10)
        self.gpsLongLCD.resize(100,50)
        self.gpsLongLCD.hide()
        
        self.gpsLongLabel = QLabel(self)
        self.gpsLongLabel.setText("long: ")
        self.gpsLongLabel.move(200,0)
        self.gpsLongLabel.hide()
        
        if DEMO:
            self.gpsLatLCD.show()
            self.gpsLatLabel.show()
            self.gpsLongLCD.show()
            self.gpsLongLabel.show()


    @pyqtSlot(float)
    def lat_update(self, value):
        self.gpsLatLCD.display(value)
        self.latValue = value
        self.update()

    @pyqtSlot(float)
    def long_update(self, value):
        self.gpsLongLCD.display(value)
        self.longValue = value
        self.update()

