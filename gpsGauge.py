import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from args import Arg_Class

class Gps(QWidget):
    def __init__(self, parent):

        super(Gps, self).__init__(parent)

        self.arguments = Arg_Class()
        
        self.latValue = 5.0
        self.longValue = 3.0
        self.rollValue = 0.0
        self.pitchValue = 0.0
        self.gForceValue = 0.0

        self.latLCD = QLCDNumber(self)
        self.latLCD.display(self.latValue)
        self.latLCD.setFrameShape(QFrame.NoFrame)
        self.latLCD.setSegmentStyle(QLCDNumber.Flat)
        self.latLCD.move(0,30)
        self.latLCD.resize(70,50)
        self.latLCD.hide()
        
        self.latLabel = QLabel(self)
        self.latLabel.setText("lat: ")
        self.latLabel.move(0,20)
        self.latLabel.hide()

        self.longLCD = QLCDNumber(self)
        self.longLCD.display(self.longValue)
        self.longLCD.setFrameShape(QFrame.NoFrame)
        self.longLCD.setSegmentStyle(QLCDNumber.Flat)
        self.longLCD.move(100,30)
        self.longLCD.resize(70,50)
        self.longLCD.hide()
        
        self.longLabel = QLabel(self)
        self.longLabel.setText("long: ")
        self.longLabel.move(100,20)
        self.longLabel.hide()

        self.rollLCD = QLCDNumber(self)
        self.rollLCD.display(self.rollValue)
        self.rollLCD.setFrameShape(QFrame.NoFrame)
        self.rollLCD.setSegmentStyle(QLCDNumber.Flat)
        self.rollLCD.move(200,30)
        self.rollLCD.resize(70,50)
        self.rollLCD.hide()
        
        self.rollLabel = QLabel(self)
        self.rollLabel.setText("Roll: ")
        self.rollLabel.move(200,20)
        self.rollLabel.hide()

        self.pitchLCD = QLCDNumber(self)
        self.pitchLCD.display(self.pitchValue)
        self.pitchLCD.setFrameShape(QFrame.NoFrame)
        self.pitchLCD.setSegmentStyle(QLCDNumber.Flat)
        self.pitchLCD.move(300,30)
        self.pitchLCD.resize(70,50)
        self.pitchLCD.hide()
        
        self.pitchLabel = QLabel(self)
        self.pitchLabel.setText("Pitch: ")
        self.pitchLabel.move(300,20)
        self.pitchLabel.hide()

        self.gForceLCD = QLCDNumber(self)
        self.gForceLCD.display(self.gForceValue)
        self.gForceLCD.setFrameShape(QFrame.NoFrame)
        self.gForceLCD.setSegmentStyle(QLCDNumber.Flat)
        self.gForceLCD.move(0,100)
        self.gForceLCD.resize(70,50)
        self.gForceLCD.hide()
        
        self.gForceLabel = QLabel(self)
        self.gForceLabel.setText("gForce: ")
        self.gForceLabel.move(0,100)
        self.gForceLabel.hide()
        
        self.latLCD.show()
        self.latLabel.show()
        self.longLCD.show()
        self.longLabel.show()
        self.rollLCD.show()
        self.rollLabel.show()
        self.pitchLCD.show()
        self.pitchLabel.show()
        self.gForceLCD.show()
        self.gForceLabel.show()
    @pyqtSlot(float)
    def lat_update(self, value):
        self.latLCD.display(value)
        self.latValue = value
        self.update()

    @pyqtSlot(float)
    def long_update(self, value):
        self.longLCD.display(value)
        self.longValue = value
        self.update()

    @pyqtSlot(float)
    def roll_update(self, value):
        self.rollLCD.display(value)
        self.rollValue = value
        self.update()

    @pyqtSlot(float)
    def pitch_update(self, value):
        self.pitchLCD.display(value)
        self.pitchValue = value
        self.update()
        
    @pyqtSlot(float)
    def gForce_update(self, value):
        self.gForceLCD.display(value)
        self.gForceValue = value
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)

        #qp.drawRect(50, 50, 150, 150)
