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
#
# class socGraph(QWidget):
#     def __init__(self, parent):
#         super(socGraph, self).__init__(parent)
#         self.left = 10
#         self.top = 10
#         self.title = "Charge test"
#         self.width = 640
#         self.height = 400
#         self.initUI()
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         m = PlotCanvas(self, width=5, height=4)
#         m.move(0,0)
#
#         button = QPushButton('PyQt5 button', self)
#         button.setToolTip('This s an example button')
#         button.move(500,0)
#         button.resize(140,100)
#
#         self.show()
# class PlotCanvas(FigureCanvas):
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#
#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)
#
#         FigureCanvas.setSizePolicy(self,
#                 QSizePolicy.Expanding,
#                 QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#         self.plot()
#
#
#     def plot(self):
#         data = [random.random() for i in range(25)]
#         ax = self.figure.add_subplot(111)
#         ax.plot(data, 'r-')
#         ax.set_title('PyQt Matplotlib Example')
#         self.draw()
#
class CustomFigCanvas1(FigureCanvas, TimedAnimation):

        def __init__(self):

            # The data
            self.n = np.linspace(0, 1000, 1001)
            self.y = 1.5 + np.sin(self.n/20)

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
# embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#               2015 Jens H Nielsen

# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.
#
# import sys
# import os
# import random
# import matplotlib
# # Make sure that we are using QT5
# matplotlib.use('Qt5Agg')
# from PyQt5 import QtCore, QtWidgets
#
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
#
# progname = os.path.basename(sys.argv[0])
# progversion = "0.1"
#
#
# class MyMplCanvas(FigureCanvas):
#     """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
#
# import sys
# import os
# import random
# import matplotlib
# # Make sure that we are using QT5
# matplotlib.use('Qt5Agg')
# from PyQt5 import QtCore, QtWidgets
#
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
#
# progname = os.path.basena
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#
#         self.compute_initial_figure()
#
#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)
#
#         FigureCanvas.setSizePolicy(self,
#                                    QtWidgets.QSizePolicy.Expanding,
#                                    QtWidgets.QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#
#     def compute_initial_figure(self):
#         pass
#
#
# class MyStaticMplCanvas(MyMplCanvas):
#     """Simple canvas with a sine plot."""
#
#     def compute_initial_figure(self):
#         t = arange(0.0, 3.0, 0.01)
#         s = sin(2*pi*t)
#         self.axes.plot(t, s)
#
#
# class MyDynamicMplCanvas(MyMplCanvas):
#     """A canvas that updates itself every second with a new plot."""
#
#     def __init__(self, *args, **kwargs):
#         MyMplCanvas.__init__(self, *args, **kwargs)
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(self.update_figure)
#         timer.start(1000)
#
#     def compute_initial_figure(self):
#         self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
#
#     def update_figure(self):
#         # Build a list of 4 random integers between 0 and 10 (both inclusive)
#         l = [random.randint(0, 10) for i in range(4)]
#         self.axes.cla()
#         self.axes.plot([0, 1, 2, 3], l, 'r')
#         self.draw()
#
#
# class ApplicationWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         QtWidgets.QMainWindow.__init__(self)
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         self.setWindowTitle("application main window")
#
#         self.file_menu = QtWidgets.QMenu('&File', self)
#         self.file_menu.addAction('&Quit', self.fileQuit,
#                                  QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
#         self.menuBar().addMenu(self.file_menu)
#
#         self.help_menu = QtWidgets.QMenu('&Help', self)
#         self.menuBar().addSeparator()
#         self.menuBar().addMenu(self.help_menu)
#
#         self.help_menu.addAction('&About', self.about)
#
#         self.main_widget = QtWidgets.QWidget(self)
#
#         l = QtWidgets.QVBoxLayout(self.main_widget)
#         sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
#         dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
#         l.addWidget(sc)
#         l.addWidget(dc)
#
#         self.main_widget.setFocus()
#         self.setCentralWidget(self.main_widget)
#
#         self.statusBar().showMessage("All hail matplotlib!", 2000)
#
#     def fileQuit(self):
#         self.close()
#
#     def closeEvent(self, ce):
#         self.fileQuit()
#
#     def about(self):
#         QtWidgets.QMessageBox.about(self, "About",
#                                     """embedding_in_qt5.py example
# Copyright 2005 Florent Rougon, 2006 Darren Dale, 2015 Jens H Nielsen
#
# This program is a simple example of a Qt5 application embedding matplotlib
# canvases.
#
# It may be used and modified with no restriction; raw copies as well as
# modified versions may be distributed without limitation.
#
# This is modified from the embedding in qt4 example to show the difference
# between qt4 and qt5"""
#                                 )
