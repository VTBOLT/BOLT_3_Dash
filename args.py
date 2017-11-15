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
        self.Args = parser.parse_args()
