# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'solutionview.ui'
#
# Created: Wed Feb 28 10:52:09 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_SolutionView(object):
    def setupUi(self, SolutionView):
        SolutionView.setObjectName("SolutionView")
        SolutionView.resize(QtCore.QSize(QtCore.QRect(0,0,614,527).size()).expandedTo(SolutionView.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(SolutionView)
        self.vboxlayout.setMargin(4)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.moveButton = QtGui.QToolButton(SolutionView)
        self.moveButton.setCheckable(True)
        self.moveButton.setAutoExclusive(True)
        self.moveButton.setObjectName("moveButton")
        self.hboxlayout.addWidget(self.moveButton)

        self.zoomButton = QtGui.QToolButton(SolutionView)
        self.zoomButton.setCheckable(True)
        self.zoomButton.setAutoExclusive(True)
        self.zoomButton.setObjectName("zoomButton")
        self.hboxlayout.addWidget(self.zoomButton)

        self.rotateButton = QtGui.QToolButton(SolutionView)
        self.rotateButton.setCheckable(True)
        self.rotateButton.setAutoExclusive(True)
        self.rotateButton.setObjectName("rotateButton")
        self.hboxlayout.addWidget(self.rotateButton)
        
        self.syncButton = QtGui.QToolButton(SolutionView)
        self.syncButton.setObjectName("syncButton")
        self.hboxlayout.addWidget(self.syncButton)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.actionZoom = QtGui.QAction(SolutionView)
        self.actionZoom.setObjectName("actionZoom")

        self.actionMove = QtGui.QAction(SolutionView)
        self.actionMove.setObjectName("actionMove")

        self.actionRotate = QtGui.QAction(SolutionView)
        self.actionRotate.setObjectName("actionRotate")
        
        self.actionSync = QtGui.QAction(SolutionView)
        self.actionSync.setObjectName("actionSync")

        self.retranslateUi(SolutionView)
        QtCore.QMetaObject.connectSlotsByName(SolutionView)

    def retranslateUi(self, SolutionView):
        SolutionView.setWindowTitle(QtGui.QApplication.translate("SolutionView", "Solution View", None, QtGui.QApplication.UnicodeUTF8))
        self.moveButton.setText(QtGui.QApplication.translate("SolutionView", "Move", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomButton.setText(QtGui.QApplication.translate("SolutionView", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.rotateButton.setText(QtGui.QApplication.translate("SolutionView", "Rotate", None, QtGui.QApplication.UnicodeUTF8))
        self.syncButton.setText(QtGui.QApplication.translate("SolutionView", "Sync", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom.setText(QtGui.QApplication.translate("SolutionView", "zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMove.setText(QtGui.QApplication.translate("SolutionView", "move", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRotate.setText(QtGui.QApplication.translate("SolutionView", "rotate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSync.setText(QtGui.QApplication.translate("SolutionView", "sync",None, QtGui.QApplication.UnicodeUTF8))

