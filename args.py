#############################################################################
## Description: Sets up a python library called argparse that handles command line arguments
## Written for: BOLT Senior Design Team
## Author: Matt Verghese
## Written: Fall 2017
## Last Upadated: Fall 2017
## Notes:
#############################################################################

import argparse

class Arg_Class(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='arg parse lets go')
        parser.add_argument('-demo', action='store_true', help='demo help')
        parser.add_argument('-debug', action='store_true', help='debug help')
        parser.add_argument('-canoff', action='store_false', help='canoff help')
        parser.add_argument('-gpsoff', action='store_false', help='gpsoff help')
        parser.add_argument('-dots', action='store_true', help='turn dots on')
        parser.add_argument('-fullscreen', action='store_true', help='full screen')
        # option to use fake data instead of reading from can bus
        parser.add_argument('-dev', action='store_false', help='dev help')
        parser.add_argument('-log', action='store_true', help='log help')
        parser.add_argument('-loc', help='location help')
        # option to go to the charging screen instead of the racing dash
        parser.add_argument('-charging', action='store_true', help='charging on')
        self.Args = parser.parse_args()
