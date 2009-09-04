import sys, math
from PyQt4 import QtCore, QtGui, QtXml, QtOpenGL
from constants import *
from commands import *

# check for the installation of PyOpenGL
try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except ImportError:
	app = QtGui.QApplication(sys.argv)
	QtGui.QMessageBox.critical(None, "OpenGL grabber","PyOpenGL must be installed to run this example.",
					QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)
	sys.exit(1)

