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
        canWorker.rpmUpdateValue.connect(dash.fileWriter.rpm_write)
        canWorker.socUpdateValue.connect(dash.socGauge.soc_update)
        canWorker.socUpdateValue.connect(dash.fileWriter.soc_write)
        canWorker.tempUpdateValue.connect(dash.tempGauge.temp_update)
        canWorker.tempUpdateValue.connect(dash.fileWriter.temp_write)
        canWorker.errorSignal.connect(dash.error_update)

    if GPS == True:
        gpsWorker = GpsReader()
        gpsWorker.start()
        gpsWorker.currentLapTimeValue.connect(dash.currentLapTimeGauge.currentLapTime_update)
        gpsWorker.latValue.connect(dash.debugGps.gpsGauge.lat_update)
        gpsWorker.latValue.connect(dash.fileWriter.lat_write)
        gpsWorker.longValue.connect(dash.debugGps.gpsGauge.long_update)
        gpsWorker.longValue.connect(dash.fileWriter.long_write)
        gpsWorker.rollValue.connect(dash.debugGps.gpsGauge.roll_update)
        gpsWorker.rollValue.connect(dash.fileWriter.roll_write)
        gpsWorker.pitchValue.connect(dash.debugGps.gpsGauge.pitch_update)
        gpsWorker.pitchValue.connect(dash.fileWriter.pitch_write)
        gpsWorker.gForceValue.connect(dash.debug.c1.channel_update)
        gpsWorker.gForceValue.connect(dash.fileWriter.gForce_write)
        
        gpsWorker.accelValue.connect(dash.fileWriter.accel_write)
        gpsWorker.gyroValue.connect(dash.fileWriter.gyro_write)
        gpsWorker.velValue.connect(dash.fileWriter.vel_write)
    
    print("dash thread:", app.instance().thread())
    app.processEvents()
    sys.exit(app.exec_())
                                                                
