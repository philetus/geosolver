# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferencesdialog.ui'
#
# Created: Tue May 22 16:27:12 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_preferencesDialog(object):
    def setupUi(self, preferencesDialog):
        preferencesDialog.setObjectName("preferencesDialog")
        preferencesDialog.resize(QtCore.QSize(QtCore.QRect(0,0,593,472).size()).expandedTo(preferencesDialog.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(preferencesDialog)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.contentsWidget = QtGui.QListWidget(preferencesDialog)
        self.contentsWidget.setMaximumSize(QtCore.QSize(128,16777215))
        self.contentsWidget.setObjectName("contentsWidget")
        self.hboxlayout.addWidget(self.contentsWidget)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.pagesWidget = QtGui.QStackedWidget(preferencesDialog)
        self.pagesWidget.setObjectName("pagesWidget")

        self.vboxlayout.addWidget(self.pagesWidget)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.closeButton = QtGui.QPushButton(preferencesDialog)
        self.closeButton.setObjectName("closeButton")
        self.hboxlayout1.addWidget(self.closeButton)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.retranslateUi(preferencesDialog)
        self.pagesWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),preferencesDialog.close)
        QtCore.QMetaObject.connectSlotsByName(preferencesDialog)

    def retranslateUi(self, preferencesDialog):
        preferencesDialog.setWindowTitle(QtGui.QApplication.translate("preferencesDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("preferencesDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

