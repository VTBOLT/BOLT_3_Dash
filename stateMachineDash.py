import sys, time
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QAction, QPushButton
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QThread, pyqtSlot, QEvent
from PyQt5.QtGui import QKeyEvent
from stateMachineGUI import StateMachine

DASH_WIDTH = 1000
DASH_HEIGHT = 550
class Dash(QMainWindow):
    accessoryPress = pyqtSignal(int)
    ignitionPress = pyqtSignal(int)
    precharge = pyqtSignal(int)
    estop = pyqtSignal(int)
    def __init__(self, parent=None):
        super(Dash, self).__init__(parent)

        self.setWindowTitle('BOLT DASH')
        self.setMinimumWidth(DASH_WIDTH)
        self.setMinimumHeight(DASH_HEIGHT)
        self.initGUI()
    def initGUI(self):

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        p.setColor(self.foregroundRole(), Qt.white)

        self.setPalette(p)
        self.stateMachine = StateMachine(self)
        self.stateMachine.move(DASH_WIDTH/2-200,DASH_HEIGHT/2-100)
        self.stateMachine.resize(300,200)
        self.stateMachine.show()
        self.accessoryPress.connect(self.stateMachine.updateState)
        self.ignitionPress.connect(self.stateMachine.updateState)
        self.precharge.connect(self.stateMachine.updateState)
        self.estop.connect(self.stateMachine.updateState)
    def keyPressEvent(self, event):
        if (type(event) == QKeyEvent and event.key() == 0x41):
             self.accessoryPress.emit(1)
             print("Accessory Pressed")
             print(self.stateMachine.currState)
        elif (type(event) == QKeyEvent and event.key() == 0x49):
             self.ignitionPress.emit(2)
             print("Ignition Pressed")
             print(self.stateMachine.currState)
        elif (type(event) == QKeyEvent and event.key() == 0x45):
             self.estop.emit(0)
             print("Emergency Stop")
             print(self.stateMachine.currState)
