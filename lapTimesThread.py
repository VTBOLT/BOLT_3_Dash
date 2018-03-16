############################################################################################################
## Description: 
## Written for: BOLT Senior Design Team
## Author: 
## Written: 
## Modified: 
## Notes
############################################################################################################

import os, sys
import time
import subprocess
import can
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

from args import Arg_Class

class LapTimesThread(QThread):

    
    def __init__(self):
        QThread.__init__(self)
        self.time = 5.0
        self.latValue = 0.0
        self.longValue = 0.0
        self.lapTimeUpateValue = pyqtSignal(float)
    def run(self):

        self.arguments = Arg_Class()

        print("Lap times worker thread:", self.currentThread())
        
        while True:
            time.sleep(.1)
            
            #self.lapTimeUpdateValue.emit(self.time)
            
            #self.processEvents()
        self.exec()
    @pyqtSlot(float)
    def lat_update(self, value):
        self.latValue = value

    @pyqtSlot(float)
    def long_update(self, value):
        self.longValue = value

