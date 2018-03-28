from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QLCDNumber,QLabel, QAction, QFrame, QGridLayout, QDesktopWidget
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D

class CustomFigCanvas2(FigureCanvas, TimedAnimation):

        def __init__(self):

            # The data
            self.n = np.linspace(0, 1000, 1001)
            self.y = 1.5 + np.cos(self.n/20)

            # The window
            self.fig = Figure(figsize=(5,5), dpi=100)
            ax1 = self.fig.add_subplot(111)

            # ax1 settings
            ax1.set_xlabel('time')
            ax1.set_ylabel('raw data')
            self.line1 = Line2D([], [], color='blue')
            ax1.add_line(self.line1)
            ax1.set_xlim(0, 1000)
            ax1.set_ylim(0, 4)

            FigureCanvas.__init__(self, self.fig)
            TimedAnimation.__init__(self, self.fig, interval = 20, blit = True)


        def _draw_frame(self, framedata):
            i = framedata
            print(i)


            self.line1.set_data(self.n[ 0 : i ], self.y[ 0 : i ])
            self._drawn_artists = [self.line1]

        def new_frame_seq(self):
            return iter(range(self.n.size))

        def _init_draw(self):
            lines = [self.line1]
            for l in lines:
                l.set_data([], [])
