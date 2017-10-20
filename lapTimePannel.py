import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

DEMO = False
if len(sys.argv) > 1:
    if any("-demo" in s for s in sys.argv):
        DEMO = True

class LastLapTime(QWidget):
    def __init__(self, parent):
        super(LastLapTime, self).__init__(parent)
        
        self.lastLapTimeMin = 0
        self.lastLapTimeSec = 0
        self.lastLapTimeMsec = 0
        
        self.lastLapTimeLCD = QLCDNumber(self)
        self.lastLapTimeLCD.setDigitCount(9)
        self.lastLapTimeLCD.display(str(self.lastLapTimeMin).zfill(2)+":"+str(self.lastLapTimeSec).zfill(2)+":"+str(self.lastLapTimeMsec).zfill(3))
        self.lastLapTimeLCD.move(0,20)
        self.lastLapTimeLCD.resize(170,40)
        self.lastLapTimeLCD.setFrameShape(QFrame.NoFrame)
        self.lastLapTimeLCD.setSegmentStyle(QLCDNumber.Flat)
        
        self.lastLapTimeLabel = QLabel(self)
        self.lastLapTimeLabel.setText("Last Lap Time:")
        self.lastLapTimeLabel.move(0,0)
        
    @pyqtSlot(int, int, int)
    def lastLapTime_update(self, min, sec, msec):
        self.lastLapTimeLCD.display(str(min).zfill(2) + ':' + str(sec).zfill(2) + ':' + str(msec).zfill(3))
        

class CurrentLapTime(QWidget):
    def __init__(self, parent):
        super(CurrentLapTime, self).__init__(parent)
        
        
        self.currentLapTimeValue = "00:00:000"
        
        self.currentLapTimeLCD = QLCDNumber(self)
        self.currentLapTimeLCD.setDigitCount(9)
        self.currentLapTimeLCD.display(self.currentLapTimeValue)
        self.currentLapTimeLCD.move(0, 20)
        if DEMO:
            self.currentLapTimeLCD.resize(170,40)
        else:
            self.currentLapTimeLCD.resize(270,140)
            self.currentLapTimeLCD.move(0,0)
        self.currentLapTimeLCD.setFrameShape(QFrame.NoFrame)
        self.currentLapTimeLCD.setSegmentStyle(QLCDNumber.Flat)
        
        self.currentLapTimeLabel = QLabel(self)
        self.currentLapTimeLabel.setText("Current Lap Time:")
        self.currentLapTimeLabel.move(0,0)
        self.currentLapTimeLabel.hide()
        if DEMO:
            self.currentLapTimeLabel.show()
        
    @pyqtSlot(int, int, int)
    def currentLapTime_update(self, min, sec, msec):
        self.currentLapTimeLCD.display(str(min).zfill(2) + ':' + str(sec).zfill(2) + ':' + str(msec).zfill(3))
        

    def paintEvent(self, event):
        qp = QPainter(self)
        if DEMO:
            qp.setPen(Qt.white)
            qp.drawRect(40,70, 90, 50)
            qp.drawRect(50, 80, 70, 30)
            qp.setBrush(Qt.green)
            qp.drawRect(60,70,5,10)
        
class BestLapTime(QWidget):
    def __init__(self, parent):
        super(BestLapTime, self).__init__(parent)

        self.bestLapTimeValue = "00:00:000"
                                                  
        self.bestLapTimeLCD = QLCDNumber(self)
        self.bestLapTimeLCD.setDigitCount(9)
        self.bestLapTimeLCD.display(self.bestLapTimeValue)
        self.bestLapTimeLCD.move(0,20)
        self.bestLapTimeLCD.resize(170,40)
        self.bestLapTimeLCD.setFrameShape(QFrame.NoFrame)
        self.bestLapTimeLCD.setSegmentStyle(QLCDNumber.Flat)
        
        self.bestLapTimeLabel = QLabel(self)
        self.bestLapTimeLabel.setText("Best Lap Time: ")
        self.bestLapTimeLabel.move(0, 0)

    @pyqtSlot(int, int, int)
    def bestLapTime_update(self, min, sec, msec):
        self.bestLapTimeLCD.display(str(min).zfill(2) + ':' + str(sec).zfill(2) + ':' + str(msec).zfill(3))
