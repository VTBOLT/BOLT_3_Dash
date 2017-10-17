import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt
class Temp(QWidget):
    def __init__(self, parent):

        super(Temp, self).__init__(parent)
                 
        self.tempValue = 0

        self.tempGauge = QLCDNumber(self)
        self.tempGauge.display(str(self.tempValue).zfill(1))
        self.tempGauge.move(0,10)
        self.tempGauge.resize(160,100)
        self.tempGauge.setFrameShape(QFrame.NoFrame)
        self.tempGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.templabel = QLabel(self)
        self.templabel.setText("temp: ")
        self.templabel.move(0,0)
        
    @pyqtSlot(float)
    def temp_update(self, value):
        self.tempGauge.display(value)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        qp.drawRect(20,110,100,20)
        qp.drawLine(70, 104, 70, 136)
        qp.drawLine(90, 104, 90, 136)

        qp.setBrush(Qt.green)
        qp.drawRect(80,110,5,20)
        
