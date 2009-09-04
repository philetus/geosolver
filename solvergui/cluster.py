""" Cluster objects partially based on the existing prototype objects for visualisation
in the sketcher. """

from includes import *
#import prototypeObjects

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    app = QtGui.QApplication( sys.argv )
    QtGui.QMessageBox.critical( None, "OpenGL grabber", "PyOpenGL must be installed to run this example.", 
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton )
    sys.exit( 1 )

