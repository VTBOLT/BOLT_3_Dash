// g++ canInterface.cpp -o canInterface can/canrecieve.cpp

#include "canInterface.h"

CanReader::CanReader()
{
  
  //system("sudo ifconfig can0 down");
  //system("sudo ip link set can0 up type can bitrate 500000");
  //system("sudo ifconfig can0 txqueuelen 100");//sets the buffer size to 100
  //try{
    openPort("can0");
    //}
    //catch(...){
    // std::cout << "ERROR: NO CAN BUS FOUND" << std::endl;
    //std::exit(0);
    //abort = true;
    //}
    abort = false;
}


CanReader::~CanReader()
{
    abort = true;

    sleep(1000);
    //system("sudo ip link set can0 down");
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
  //std::cout<< "run called" << std::endl;
  struct can_frame frame_rd;
  int recvbytes = 0;
  //std::list<int> mtrCntrlTemps;

  int RPM             = 0;
  int SOC             = 0;
  int mtrTemp         = 0;
  int moduleA         = 0;
  int moduleB         = 0;
  int moduleC         = 0;
  int gateDrvrBrd     = 0;
  int highCellTemp    = 0;

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
            case 0x181:
              //BMS Tempatures
              //possilby 1-3?? need to test
      	      highCellTemp = (int16_t)(( frame_rd.data[2] << 8 ) + ( frame_rd.data[1] )) * 0.1;
              lowCellTemp = (int16_5)(( frame_rd.data[5] << 8 ) + (frame_rd.data[4] )) * 0.1;                      
      	      std::cout << "highCellTemp:" << highCellTemp << std::endl;
              //std::cout << "lowCellTemp:" << lowCellTemp << std::endl;
      	      break;
    	      case 0x182:
              //BMS Isolations
            case 0x183:
              //BMS information
      	      SOC = (int16_t)(( frame_rd.data[5] << 8 ) + ( frame_rd.data[4] )) * 0.5;
      	      std::cout << "soc:" << SOC << std::endl;
      	      break;
    	      case 0x202:
              //BMS Current Limits
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
