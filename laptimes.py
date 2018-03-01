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

class LapTimes(QThread):
#    rpmUpdateValue = pyqtSignal(float)

    
    def __init__(self):
        QThread.__init__(self)
        self.lat = 0.0
        self.longi = 0.0
        print("lapTime worker thread:", self.currentThread())
    def run(self):
        self.arguments = Arg_Class()
        while(1):
            print("thread working", self.lat, self.longi)

        self.exec()
        
    @pyqtSlot(float)
    def lat_update(self, value):
        self.lat = value
        
    @pyqtSlot(float)
    def long_update(self, value):
        self.longi = value


        
        
                                                                                    
