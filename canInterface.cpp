// g++ canInterface.cpp -o canInterface can/canrecieve.cpp

#include "canInterface.h"

CanReader::CanReader()
{
    openPort("can0");
    abort = false;
}


CanReader::~CanReader()
{
    abort = true;

    sleep(1000);
}

bool CanReader::init()
{
  //    if (!isRunning()) {
  //      start(HighestPriority);
  //  }

    return true;
}

void CanReader::run()
{
  struct can_frame frame_rd;
  int recvbytes = 0;

  int RPM             = 0;
  int SOC             = 0;
  int mtrTemp         = 0;
  int moduleA         = 0;
  int moduleB         = 0;
  int moduleC         = 0;
  int gateDrvrBrd     = 0;
  int highCellTemp    = 0;
  int post_lo_fault = 0;
  int post_hi_fault = 0;
  int run_lo_fault = 0;
  int run_hi_fault = 0;

  int VSM_state       = 0; 
  int inverter_state  = 0;
  int relay_state     = 0;
  int inverter_run_state = 0;
  int inverter_cmd_state = 0;  
  int inverter_enable_state = 0;
  int direction_state = 0;
  
  while(1)
  {
    if ( this->abort )
  	return;
      
    struct timeval timeout = {1, 0};
    fd_set readSet;
    FD_ZERO(&readSet);
    FD_SET(this->soc, &readSet);
    if (select((this->soc + 1), &readSet, NULL, NULL, &timeout) >= 0) {
  	  if (FD_ISSET(this->soc, &readSet)) {
	      recvbytes = read(this->soc, &frame_rd, sizeof(struct can_frame));
        if(recvbytes) {
    		  //std::cout << "can_id: " << frame_rd.can_id << std::endl;
    		  switch(frame_rd.can_id) {
            case 0xA0:
              //MC Tempatures
      	      moduleA         = (int16_t)(( frame_rd.data[1] << 8 ) + ( frame_rd.data[0] )) * 0.1;
      	      moduleB         = (int16_t)(( frame_rd.data[3] << 8 ) + ( frame_rd.data[2] )) * 0.1;
      	      moduleC         = (int16_t)(( frame_rd.data[5] << 8 ) + ( frame_rd.data[4] )) * 0.1;
      	      gateDrvrBrd     = (int16_t)(( frame_rd.data[7] << 8 ) + ( frame_rd.data[6] )) * 0.1;		      
      	      std::cout << "mcTemp:" << max(moduleA, moduleB, moduleC, gateDrvrBrd) << std::endl;		    
              break;
            case 0xA2:
              //MC Tempatures
      	      mtrTemp = (int16_t)(( frame_rd.data[5] << 8 ) + ( frame_rd.data[4] )) * 0.1;
      	      std::cout << "motorTemp:" << mtrTemp << std::endl;	      
      	      break;
    	      
            case 0xA5:
              //Motor Position
              RPM = (int16_t)(( frame_rd.data[3] << 8 ) + ( frame_rd.data[2] ));
              std::cout << "rpm:" << RPM << std::endl;		      
              break;
    	      case 0x180:
              //BMS VOLTAGES
              //high low cell delta
		break;
            case 0x181:
              //BMS Tempatures
      	      highCellTemp = (int16_t)(( frame_rd.data[2] << 8 ) + ( frame_rd.data[1] )) * 0.1;
              //lowCellTemp = (int16_5)(( frame_rd.data[5] << 8 ) + (frame_rd.data[4] )) * 0.1;
      	      std::cout << "highCellTemp:" << highCellTemp << std::endl;
              //std::cout << "lowCellTemp:" << lowCellTemp << std::endl;
      	      break;
    	    case 0x182:
              //BMS Isolations
	      break;
            case 0x183:
              //BMS information
      	      SOC = (int16_t)(( frame_rd.data[5] << 8 ) + ( frame_rd.data[4] )) * 0.5;
      	      std::cout << "soc:" << SOC << std::endl;
	      break;
	    case 0xAA:
	      //Internal State of MC
	      VSM_state = (int16_t)(( frame_rd.data[1] << 8 ) + ( frame_rd.data[0] ));
	      inverter_state = (int16_t)(( frame_rd.data[2] ));
	      relay_state = (int16_t)(( frame_rd.data[3] ));
	      inverter_run_state = (int16_t)(( frame_rd.data[4] ));
	      inverter_cmd_state = (int16_t)(( frame_rd.data[5] ));
	      inverter_enable_state = (int16_t)(( frame_rd.data[6] ));
	      direction_state = (int16_t)(( frame_rd.data[7] ));

	      std::cout << "states:" << VSM_state << "_" << inverter_state << "_" << relay_state << "_" << inverter_run_state << "_" << inverter_cmd_state << "_" << inverter_enable_state << "_" << direction_state << std::endl;
	      
	    case 0xAB:
	      //MC Errors
	      post_lo_fault = (int16_t)(( frame_rd.data[1] << 8 ) + ( frame_rd.data[0] ));
	      post_hi_fault = (int16_t)(( frame_rd.data[3] << 8 ) + ( frame_rd.data[2] ));
	      run_lo_fault = (int16_t)(( frame_rd.data[5] << 8 ) + ( frame_rd.data[4] ));
	      run_hi_fault = (int16_t)(( frame_rd.data[7] << 8 ) + ( frame_rd.data[6] ));
	      std::cout << "ERROR:" << post_lo_fault << "_" << post_hi_fault << "_" << run_lo_fault << "_" << run_hi_fault << std::endl;
	      break;
            default:		
      	      //std::cout << "defualt condition, can_id:" << frame_rd.can_id << std::endl;
      	      break;
          }
        }
      }
    }
  }
}

int CanReader::openPort(const char *port)
{
  struct ifreq ifr;
  struct sockaddr_can addr;
  /* open socket */
  this->soc = socket(PF_CAN, SOCK_RAW, CAN_RAW);
  if(this->soc < 0)
    {
      return (-1);
    }
  addr.can_family = AF_CAN;
  strcpy(ifr.ifr_name, port);
  if (ioctl(this->soc, SIOCGIFINDEX, &ifr) < 0)
    {
      return (-1);
    }
  addr.can_ifindex = ifr.ifr_ifindex;
  fcntl(this->soc, F_SETFL, O_NONBLOCK);
  if (bind(this->soc, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
      return (-1);
    }
  return 0;
}

int CanReader::max(int one, int two, int three, int four){
  int max = 0;
  if (one >= max)
    max = one;
  else if (two >= max)
    max = two;
  else if (three >= max)
    max = three;
  else if (four >= max)
    max = four;
  return max;
}


int main(){
  CanReader obj;
  obj.run();
  
  return 0;
}
