#ifndef CANREADER_H
#define CANREADER_H

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <net/if.h>
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
