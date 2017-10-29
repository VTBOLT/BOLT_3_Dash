//g++ spatialReader.cpp -o spatialReader -lboost_system an_packet_protocol.c spatial_packets.c

//executable must be called spatialReader so gpsReader.py can call it
#include <boost/asio/serial_port.hpp>
#include <boost/asio.hpp>
#include <iostream>
#include <stdint.h>
#include <iomanip>

#include "an_packet_protocol.h"
#include "spatial_packets.h"

using namespace boost;
using namespace std;

#define RADIANS_TO_DEGREES (180.0/3.14)
#define MESSAGE_BUFFER_SIZE (10)

int main(){
  
  an_decoder_t an_decoder;
  an_packet_t an_packet;
  
  system_state_packet_t system_state_packet;
  raw_sensors_packet_t raw_sensors_packet;
  
  an_decoder_initialise(&an_decoder);

  int bytes_received;
  
  asio::io_service io;
  asio::serial_port port(io);

  port.open("/dev/ttyUSB0");
  port.set_option(asio::serial_port_base::baud_rate(115200));

  while(1){
    if((bytes_received = asio::read(port, asio::buffer(an_decoder_pointer(&an_decoder), an_decoder_size(&an_decoder)))) > 0){
      an_decoder_increment(&an_decoder, bytes_received);

      while((an_packet_decode(&an_decoder, &an_packet))){
	if (an_packet.id == packet_id_system_state){
	  if(decode_system_state_packet(&system_state_packet, &an_packet) == 0){
	    double lat = system_state_packet.latitude * RADIANS_TO_DEGREES;
	    double longitude = system_state_packet.longitude* RADIANS_TO_DEGREES;
	    double roll = system_state_packet.orientation[0] * RADIANS_TO_DEGREES;
	    cout << setprecision(8) << "lat:" << lat << endl;
	    cout << setprecision(8) << "long:"<< longitude << endl;
	    cout << setprecision(8) << "roll:" << roll << endl;
	  }
	}
      }
    }
  }
    return 0;
}
