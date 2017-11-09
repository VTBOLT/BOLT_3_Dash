import sys

from PyQt5.QtWidgets import QApplication


from dash import Dash
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug
from args import Arg_Class

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    arguments = Arg_Class()
    dash = Dash()
    dash.show()

    if arguments.Args.canoff == True:
        canWorker =CanReader()
        canWorker.start()
        canWorker.rpmUpdateValue.connect(dash.rpmGauge.rpm_update)
        canWorker.socUpdateValue.connect(dash.socGauge.soc_update)
        canWorker.tempUpdateValue.connect(dash.tempGauge.temp_update)
        canWorker.errorSignal.connect(dash.error_update)

    if arguments.Args.canoff == True:
        gpsWorker = GpsReader()
        gpsWorker.start()
        gpsWorker.currentLapTimeValue.connect(dash.currentLapTimeGauge.currentLapTime_update)
        gpsWorker.latValue.connect(dash.debugGps.gpsGauge.lat_update)
        gpsWorker.longValue.connect(dash.debugGps.gpsGauge.long_update)
        gpsWorker.rollValue.connect(dash.debugGps.gpsGauge.roll_update)
        gpsWorker.pitchValue.connect(dash.debugGps.gpsGauge.pitch_update)
        gpsWorker.gForceValue.connect(dash.debug.c1.channel_update)
        #gpsWorker.accelValue.connect(
        #gpsWorker.gyroValue.connect(
        #gpsWorker.velValue.connect(
    
    print("dash thread:", app.instance().thread())
    app.processEvents()
    sys.exit(app.exec_())
                                                                
