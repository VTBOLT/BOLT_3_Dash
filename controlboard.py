############################################################################################################
## Description: Displays LED display of the control board
## Values displayed: IMB, PSI, ACC, BMS State
## Written for: BOLT Senior Design Team
## Author: Khang Lieu
## Written: Spring 2018
## Modified:
############################################################################################################

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber, QLabel, QAction, QFrame
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from args import Arg_Class

class Cb(QWidget):
    def __init__(self, parent):

        super(Cb, self).__init__(parent)

        self.arguments = Arg_Class()


        #Initializing states as false until true input
        self.imbState = False
        self.psiState = False
        self.accState = False
        self.bmsState = False

        self.imdLabel = QLabel(self)
        self.psiLabel = QLabel(self)
        self.accLabel = QLabel(self)
        self.bmsLabel = QLabel(self)
        self.imdLabel.setText("IMD ")
        self.psiLabel.setText("PSI ")
        self.accLabel.setText("ACC ")
        self.bmsLabel.setText("BMS ")
        self.imdLabel.move(10,0)
        self.psiLabel.move(10,30)
        self.accLabel.move(10,60)
        self.bmsLabel.move(10,90)


    @pyqtSlot(float)
    def cb_update(self, value):

         self.update()
    #
    #
    def paintEvent(self, event):
            qp = QPainter(self)
            qp.setPen(Qt.white)

            #LED outlines
            qp.drawRect(50,0, 10, 10)
            qp.drawRect(50,30, 10, 10)
            qp.drawRect(50,60, 10, 10)
            qp.drawRect(50,90, 10, 10)

            #Insert if statements here for input states
            qp.setBrush(Qt.green)
            qp.drawRect(50,0,10,10)
            qp.drawRect(50,30,10,10)
            qp.drawRect(50,60,10,10)
            qp.drawRect(50,90,10,10)
