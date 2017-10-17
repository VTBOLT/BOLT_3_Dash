import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

class Soc(QWidget):
    def __init__(self, parent):

        super(Soc, self).__init__(parent)
                 
        self.socValue = 0.0

        self.socGauge = QLCDNumber(self)
        self.socGauge.display(str(int(self.socValue)).zfill(2)+'.'+str((self.socValue - int(self.socValue))*10).zfill(2))
        self.socGauge.move(0,10)
        self.socGauge.resize(160,100)
        self.socGauge.setFrameShape(QFrame.NoFrame)
        self.socGauge.setSegmentStyle(QLCDNumber.Flat)
        
        self.soclabel = QLabel(self)
        self.soclabel.setText("soc: ")
        self.soclabel.move(0,0)

    @pyqtSlot(float)
    def soc_update(self, value):
        self.socGauge.display(value)
        self.socValue = value
        self.update()
        #self.socGauge.display(str(int(self.socValue)).zfill(2)+'.'+ str((self.socValue - int(self.socValue))*10).zfill(2))

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        qp.drawRect(60,110, 60, 20)
        qp.drawRect(57,117, 2, 5)

        if self.socValue < 20:
            qp.setBrush(Qt.red)
        else:
            qp.setBrush(Qt.green)
            
        qp.drawRect(60+(60*(1-(self.socValue/100))), 110, ((60*self.socValue/100)),20)

