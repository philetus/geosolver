# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compositionview.ui'
#
# Created: Wed Feb 14 13:07:17 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_compositionView(object):
    def setupUi(self, compositionView):
        compositionView.setObjectName("compositionView")
        compositionView.resize(QtCore.QSize(QtCore.QRect(0,0,540,387).size()).expandedTo(compositionView.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(compositionView)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.collapseButton = QtGui.QToolButton(compositionView)
        self.collapseButton.setObjectName("collapseButton")
        self.gridlayout.addWidget(self.collapseButton,4,1,1,1)

        self.fitButton = QtGui.QToolButton(compositionView)
        self.fitButton.setObjectName("fitButton")
        self.gridlayout.addWidget(self.fitButton,3,1,1,1)
		
        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsView = QtGui.QGraphicsView(self.graphicsScene, compositionView)
        self.graphicsView.setWindowModality(QtCore.Qt.NonModal)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.graphicsView.setObjectName("graphicsView")
        self.gridlayout.addWidget(self.graphicsView,0,0,5,1)

        self.zoomInButton = QtGui.QToolButton(compositionView)
        self.zoomInButton.setIcon(QtGui.QIcon("resources/zoomin.png"))
        self.zoomInButton.setAutoRepeat(True)
        self.zoomInButton.setAutoRepeatDelay(0)
        self.zoomInButton.setAutoRepeatInterval(33)
        self.zoomInButton.setObjectName("zoomInButton")
        self.gridlayout.addWidget(self.zoomInButton,0,1,1,1)

        self.verticalSlider = QtGui.QSlider(compositionView)
        self.verticalSlider.setMaximum(500)
        self.verticalSlider.setProperty("value",QtCore.QVariant(250))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.verticalSlider.setObjectName("verticalSlider")
        self.gridlayout.addWidget(self.verticalSlider,1,1,1,1)

        self.zoomOutButton = QtGui.QToolButton(compositionView)
        self.zoomOutButton.setIcon(QtGui.QIcon("resources/zoomout.png"))
        self.zoomOutButton.setAutoRepeat(True)
        self.zoomOutButton.setAutoRepeatDelay(0)
        self.zoomOutButton.setAutoRepeatInterval(33)
        self.zoomOutButton.setObjectName("zoomOutButton")
        self.gridlayout.addWidget(self.zoomOutButton,2,1,1,1)

        self.retranslateUi(compositionView)
        QtCore.QMetaObject.connectSlotsByName(compositionView)

    def retranslateUi(self, compositionView):
        compositionView.setWindowTitle(QtGui.QApplication.translate("compositionView", "Decomposition View", None, QtGui.QApplication.UnicodeUTF8))
        self.collapseButton.setText(QtGui.QApplication.translate("compositionView", "+/-", None, QtGui.QApplication.UnicodeUTF8))
        self.fitButton.setText(QtGui.QApplication.translate("compositionView", "Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomInButton.setText(QtGui.QApplication.translate("compositionView", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomOutButton.setText(QtGui.QApplication.translate("compositionView", "...", None, QtGui.QApplication.UnicodeUTF8))

