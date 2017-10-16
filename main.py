import sys
from PyQt5.QtWidgets import QApplication
from dash import Dash
from canReader import CanReader
from gpsReader import GpsReader
from debug import Debug

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dash = Dash()
    dash.show()

    canWorker = CanReader()
    canWorker.start()
    canWorker.rpmUpdateValue.connect(dash.rpmGauge.rpm_update)
    canWorker.socUpdateValue.connect(dash.socGauge.soc_update)
    canWorker.tempUpdateValue.connect(dash.tempGauge.temp_update)
    canWorker.errorSignal.connect(dash.error_update)
    
    gpsWorker = GpsReader()
    #gpsWorker.start()
    #gpsWorker.currentLapTime.connect(dash.lapTimeCurrentGauge.currentLapTime_update)
    
    print("dash thread:", app.instance().thread())
    app.processEvents()
    sys.exit(app.exec_())
                                                                
