############################################################################################################
## Description: displays debug gps values for testing in a seperate window
## Values displayed: defined in gpsGauge.py
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Modified: Fall 2017
## Notes: 
## TODO: combine with gpsGauge.py
############################################################################################################

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame, QApplication, QPushButton
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from gpsGauge import Gps

DEBUG_WIDTH = 600
DEBUG_HEIGHT = 380

CHANNEL_WIDTH = 100
CHANNEL_HEIGHT = 100

class DebugGPS(QWidget):
    def __init__(self, parent):
        super(DebugGPS, self).__init__(parent)

        self.setWindowTitle('DEBUG GPS WINDOW')
        self.setMinimumWidth(DEBUG_WIDTH)
        self.setMinimumHeight(DEBUG_HEIGHT)
        self.initDebug()

    def initDebug(self):
        self.setAutoFillBackground(True)
        self.closeButton = QPushButton("Close", self)
        self.closeButton.move(540,350)
        self.closeButton.resize(50,20)
        self.closeButton.clicked.connect(self.debug_close)

        self.gpsGauge = Gps(self)
        self.gpsGauge.move(0, 0)
        self.gpsGauge.resize(400,400)
        

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

