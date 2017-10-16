import sys
import argparse

from PyQt5.QtWidgets import QApplication


from dash import Dash
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug
#import parseArguments

CAN = True
GPS = True
if len(sys.argv) > 1:
    if any("-canoff" in s for s in sys.argv):
        CAN = False
    if any("-gpsoff" in s for s in sys.argv):
        GPS = False

if __name__ == '__main__':
    #args = parseArguments.ParseArguments()
    
    app = QApplication(sys.argv)
    dash = Dash()
    dash.show()

    if CAN == True:
        canWorker =CanReader()
        canWorker.start()
        canWorker.rpmUpdateValue.connect(dash.rpmGauge.rpm_update)
        canWorker.socUpdateValue.connect(dash.socGauge.soc_update)
        canWorker.tempUpdateValue.connect(dash.tempGauge.temp_update)
        canWorker.errorSignal.connect(dash.error_update)

    if GPS == True:
        gpsWorker = GpsReader()
        gpsWorker.start()
        gpsWorker.currentLapTime.connect(dash.lapTimeCurrentGauge.currentLapTime_update)
    
    print("dash thread:", app.instance().thread())
    app.processEvents()
    sys.exit(app.exec_())
                                                                