//g++ spatialReader.c -o spatialReader -lboost_system spatial/an_packet_protocol.c spatial/spatial_packets.c

//executable must be called spatialReader so gpsReader.py can call it
#include <boost/asio/serial_port.hpp>
#include <boost/asio.hpp>
#include <iostream>
#include <stdint.h>
#include <iomanip>

#include "spatial/an_packet_protocol.h"
#include "spatial/spatial_packets.h"

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
	    double pitch = system_state_packet.orientation[1] * RADIANS_TO_DEGREES;
	    double gForce = sysetem_state_packet.g_force;
	    //velocity
	    double vX = system_state_packet_velocity[0];
	    double vY = system_state_packet_velocity[1];
	    double vZ = system_state_packet_velocity[2];
	    
	    cout << setprecision(8) << "lat:" << lat << endl;
	    cout << setprecision(8) << "long:"<< longitude << endl;
	    cout << setprecision(8) << "roll:" << roll << endl;
	    cout << setprecision(8) << "pitch:" << pitch << endl;
	    cout << setprecision(8) << "gForce:" << gForce << endl;
	    cout << setprecision(8) << "velocity:" << vX ":" << vY << ":" << vZ << endl;
	  }
	  else if(an_packet.id == packet_id_raw_sensors){
	    raw_sensors_packet_t raw_sensors_packet;
	     if(decode_raw_sensors_packet(&raw_sensors_packet, &an_packet) == 0){
	       //Accelerometer data
	       double aX = raw_sensors_packet.accelerometers[0] * RADIANS_TO_DEGREES;
	       double aY = raw_sensors_packet.accelerometers[1] * RADIANS_TO_DEGREES;
	       double aZ = raw_sensors_packet.accelerometers[2] * RADIANS_TO_DEGREES;
	       cout << setprecision(8) << "accel:" << aX << ":" << aY << ":" << aZ << endl;
	       //Gyroscopes

	       double gX = raw_sensors_packet.gyroscopes[0] * RADIANS_TO_DEGREES;
	       double gY = raw_sensors_packet.gyroscopes[1] * RADIANS_TO_DEGREES;
	       double gZ = raw_sensors_packet.gyroscopes[2] * RADIANS_TO_DEGREES;
	       cout << setprecision(8) << "gyro:"<< gX << ":" << gY << ":" << gZ << endl;
	     }
	  }
	}
      }
    }
  }
    return 0;
}
