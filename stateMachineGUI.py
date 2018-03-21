import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame, QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

class StateMachine(QWidget):
    def __init__(self, parent):

        super(StateMachine, self).__init__(parent)

        self.currState = 0

        self.title = QLabel(self)
        self.idle = QLabel(self)
        self.accessory = QLabel(self)
        self.mc = QLabel(self)
        self.precharge = QLabel(self)

        self.title.setText("Current State")
        self.idle.setText("Idle")
        self.accessory.setText("Accessory On")
        self.mc.setText("Motor Controller On")
        self.precharge.setText("Precharging")

        self.title.move(50, 0)
        self.idle.move(50,50)
        self.accessory.move(50,70)
        self.mc.move(50,90)
        self.precharge.move(50,110)

	#arrow idle
        self.arrow = QPainterPath()
        self.arrow.moveTo(0,63)
        self.arrow.lineTo(40,63)
        self.arrow.moveTo(40,63)
        self.arrow.lineTo(30,53)
        self.arrow.moveTo(40,63)
        self.arrow.lineTo(30,73)

        #arrow accessory
        self.arrow1 = QPainterPath()
        self.arrow1.moveTo(0,83)
        self.arrow1.lineTo(40,83)
        self.arrow1.moveTo(40,83)
        self.arrow1.lineTo(30,73)
        self.arrow1.moveTo(40,83)
        self.arrow1.lineTo(30,93)

        #arrow MC
        self.arrow2 = QPainterPath()
        self.arrow2.moveTo(0,103)
        self.arrow2.lineTo(40,103)
        self.arrow2.moveTo(40,103)
        self.arrow2.lineTo(30,93)
        self.arrow2.moveTo(40,103)
        self.arrow2.lineTo(30,113)

        #arrow precharge
        self.arrow3 = QPainterPath()
        self.arrow3.moveTo(0,123)
        self.arrow3.lineTo(40,123)
        self.arrow3.moveTo(40,123)
        self.arrow3.lineTo(30,113)
        self.arrow3.moveTo(40,123)
        self.arrow3.lineTo(30,133)
    @pyqtSlot(int)
    def updateState(self, value):
        self.currState = value
        self.update()
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)
        if self.currState == 0:
             qp.drawPath(self.arrow)
        elif self.currState == 1:
             qp.drawPath(self.arrow1)
        elif self.currState == 2:
             qp.drawPath(self.arrow2)
        elif self.currState == 3:
             qp.drawPath(self.arrow3)
