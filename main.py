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
        canWorker.rpmUpdateValue.connect(dash.fileWriter.rpm_write)
        canWorker.socUpdateValue.connect(dash.fileWriter.soc_write)
        canWorker.tempUpdateValue.connect(dash.fileWriter.temp_write)
                
        gpsWorker = GpsReader()
        gpsWorker.start()
        gpsWorker.currentLapTimeValue.connect(dash.currentLapTimeGauge.currentLapTime_update)
        gpsWorker.latValue.connect(dash.debugGps.gpsGauge.lat_update)

        gpsWorker.longValue.connect(dash.debugGps.gpsGauge.long_update)

        gpsWorker.rollValue.connect(dash.debugGps.gpsGauge.roll_update)

        gpsWorker.pitchValue.connect(dash.debugGps.gpsGauge.pitch_update)
        
        gpsWorker.gForceValue.connect(dash.debug.c1.channel_update)
        
        if arguments.Args.log == True:
            gpsWorker.accelValue.connect(dash.fileWriter.accel_write)
            gpsWorker.gyroValue.connect(dash.fileWriter.gyro_write)
            gpsWorker.velValue.connect(dash.fileWriter.vel_write)
            
            gpsWorker.latValue.connect(dash.fileWriter.lat_write)
            gpsWorker.longValue.connect(dash.fileWriter.long_write)
            gpsWorker.rollValue.connect(dash.fileWriter.roll_write)
            gpsWorker.pitchValue.connect(dash.fileWriter.pitch_write)
            gpsWorker.gForceValue.connect(dash.fileWriter.gForce_write)
        
    print("dash thread:", app.instance().thread())
    app.processEvents()
    sys.exit(app.exec_())
                                                                
