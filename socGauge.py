import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt
DEMO = False
if len(sys.argv) > 1:
    if any("-demo" in s for s in sys.argv):
        DEMO = True

class Soc(QWidget):
    def __init__(self, parent):

        super(Soc, self).__init__(parent)
                 
        self.socValue = 0.0
        
        self.socLCD = QLCDNumber(self)
        self.socLCD.display(str(int(self.socValue)).zfill(4)+'.'+str((self.socValue - int(self.socValue))*10).zfill(4))
        self.socLCD.setFrameShape(QFrame.NoFrame)
        self.socLCD.setSegmentStyle(QLCDNumber.Flat)
        self.socLCD.move(0,10)
        self.socLCD.resize(160,100)
        self.socLCD.hide()
        
        self.socLabel = QLabel(self)
        self.socLabel.setText("soc: ")
        self.socLabel.move(0,0)
        self.socLabel.hide()
        
        if DEMO:
            self.socLCD.show()
            self.socLabel.show()
        
    @pyqtSlot(float)
    def soc_update(self, value):
        self.socLCD.display(value)
        self.socValue = value
        self.update()
        #self.socGauge.display(str(int(self.socValue)).zfill(2)+'.'+ str((self.socValue - int(self.socValue))*10).zfill(2))

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        if DEMO:
            qp.drawRect(60,110, 60, 20)
            qp.drawRect(57,117, 2, 5)
        else:
            qp.drawRect(60,0, 150, 60)
            qp.drawRect(53,20, 7, 20)

        if self.socValue < 20:
            qp.setBrush(Qt.red)
        else:
            qp.setBrush(Qt.green)
        if DEMO:
            qp.drawRect(60+(60*(1-(self.socValue/100))), 110, ((60*self.socValue/100)),20)
        else:
            qp.drawRect(60+(150*(1-(self.socValue/100))), 0, ((150*self.socValue/100)),60)
            

