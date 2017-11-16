#!/bin/bash
## compiles gps and can code

#g++ spatialReader.c -o spatialReader -lboost_system spatial/an_packet_protocol.c spatial/spatial_packets.c

#g++ canInterface.cpp -o canInterface can/canrecieve.cpp

## Runs dash
### Race mode with logging, can and gps enabled
#python3 main.py -dev -fullscreen -log

### Testing mode displaying fake data
sudo python3 /home/pi/BOLT_3_Dash/main.py -dev -canoff -log

