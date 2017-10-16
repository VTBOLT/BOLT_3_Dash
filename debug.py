import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame, QApplication
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

DEBUG_WIDTH = 600
DEBUG_HEIGHT = 380

class Debug(QWidget):
    def __init__(self, parent):
        super(Debug, self).__init__(parent)

        self.setWindowTitle('DEBUG WINDOW')
        self.setMinimumWidth(DEBUG_WIDTH)
        self.setMinimumHeight(DEBUG_HEIGHT)
        #self.initDebug()

    def initDebug(self):

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        p.setColor(self.foregroundRole(), Qt.black)
        self.setPalette(p)

        self.show()
        
    @pyqtSlot()
    def debug_open(self):
        self.initDebug()

