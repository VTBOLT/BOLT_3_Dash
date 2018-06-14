#!/bin/sh

#################################################################################
## Description: shell script to run the dashboard and log startup/ runtime errors
## Written for: BOLT Senior Design Team
## Author: Henry Trease
## Written: Fall 2017
## Notes:
#################################################################################

##compiles GPS and CAN code
#g++ spatialReader.c -o spatialReader -lboost_system spatial/an_packet_protocol.c spatial/spatial_packets.c
#g++ canInterface.cpp -o canInterface can/canrecieve.cpp

sleep 4 ## sleep is necessary to run on startup

## creates a log file with a unique filename everytime it is run
sudo python3 /home/pi/BOLT_3_Dash/main.py -fullscreen -gpsoff -log > /home/pi/logs/dash_start_log_$(date "+%H_%M_%S").txt 2>&1
