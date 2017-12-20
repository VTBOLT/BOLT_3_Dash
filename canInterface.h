/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Reads from the CAN bus and writes values to standard out
// Written for: BOLT Senior Design Team
// Author: Joe Griffin
// Written: Summer 2017
// Modified: Henry Trease
// Modified: Fall 2017
// Compile command: g++ canInterface.cpp -o canInterface can/canrecieve.cpp
// Notes: executable must be called "canReader" so canReader.py can call it
//		   requires dependent files to be in a directory called "can" within the same directory as canInterface.h
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifndef CANREADER_H
#define CANREADER_H

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <cstdlib>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <linux/can/error.h>

//#include <list>

#include <iostream>


class CanReader
{
public:
    CanReader();
    ~CanReader();

    bool init();

    void run();

private:
    bool abort;

    int soc;
    int openPort(const char *port);
    int max(int, int, int, int);
};

#endif // CANREADER_H
