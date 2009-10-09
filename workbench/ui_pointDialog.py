# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unknown'
#
# Created: Wed Nov  1 16:41:41 2006
#      by: PyQt4 UI code generator 4.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_PointDialog(object):
    def setupUi(self, PointDialog):
        PointDialog.setObjectName("PointDialog")
        PointDialog.resize(QtCore.QSize(QtCore.QRect(0,0,226,319).size()).expandedTo(PointDialog.minimumSizeHint()))

        self.label_19 = QtGui.QLabel(PointDialog)
        self.label_19.setGeometry(QtCore.QRect(10,10,54,24))

        font = QtGui.QFont(self.label_19.font())
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")

        self.groupBox_8 = QtGui.QGroupBox(PointDialog)
        self.groupBox_8.setGeometry(QtCore.QRect(20,80,181,141))
        self.groupBox_8.setObjectName("groupBox_8")

        self.gridLayout_4 = QtGui.QWidget(self.groupBox_8)
        self.gridLayout_4.setGeometry(QtCore.QRect(30,20,121,101))
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.gridlayout = QtGui.QGridLayout(self.gridLayout_4)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_21 = QtGui.QLabel(self.gridLayout_4)
        self.label_21.setObjectName("label_21")
        self.gridlayout.addWidget(self.label_21,0,0,1,1)

        self.label_22 = QtGui.QLabel(self.gridLayout_4)
        self.label_22.setObjectName("label_22")
        self.gridlayout.addWidget(self.label_22,1,0,1,1)

        self.label_23 = QtGui.QLabel(self.gridLayout_4)
        self.label_23.setObjectName("label_23")
        self.gridlayout.addWidget(self.label_23,2,0,1,1)

        self.pointCoordX_2 = QtGui.QDoubleSpinBox(self.gridLayout_4)
        self.pointCoordX_2.setDecimals(4)
        self.pointCoordX_2.setMaximum(9999.9999)
        self.pointCoordX_2.setMinimum(-10000.0)
        self.pointCoordX_2.setObjectName("pointCoordX_2")
        self.gridlayout.addWidget(self.pointCoordX_2,0,1,1,1)

        self.pointCoordY_2 = QtGui.QDoubleSpinBox(self.gridLayout_4)
        self.pointCoordY_2.setDecimals(4)
        self.pointCoordY_2.setMaximum(10000.0)
        self.pointCoordY_2.setMinimum(-10000.0)
        self.pointCoordY_2.setObjectName("pointCoordY_2")
        self.gridlayout.addWidget(self.pointCoordY_2,1,1,1,1)

        self.pointCoordZ_2 = QtGui.QDoubleSpinBox(self.gridLayout_4)
        self.pointCoordZ_2.setDecimals(4)
        self.pointCoordZ_2.setMaximum(10000.0)
        self.pointCoordZ_2.setMinimum(-10000.0)
        self.pointCoordZ_2.setObjectName("pointCoordZ_2")
        self.gridlayout.addWidget(self.pointCoordZ_2,2,1,1,1)

        self.groupBox_7 = QtGui.QGroupBox(PointDialog)
        self.groupBox_7.setGeometry(QtCore.QRect(20,230,181,61))
        self.groupBox_7.setObjectName("groupBox_7")

        self.pointFixed_2 = QtGui.QCheckBox(self.groupBox_7)
        self.pointFixed_2.setGeometry(QtCore.QRect(40,20,79,22))
        self.pointFixed_2.setObjectName("pointFixed_2")

        self.horizontalLayout_6 = QtGui.QWidget(PointDialog)
        self.horizontalLayout_6.setGeometry(QtCore.QRect(20,40,181,31))
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout_6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_20 = QtGui.QLabel(self.horizontalLayout_6)

        font = QtGui.QFont(self.label_20.font())
        font.setPointSize(10)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.hboxlayout.addWidget(self.label_20)

        spacerItem = QtGui.QSpacerItem(8,15,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pointName_2 = QtGui.QLineEdit(self.horizontalLayout_6)
        self.pointName_2.setObjectName("pointName_2")
        self.hboxlayout.addWidget(self.pointName_2)

        self.retranslateUi(PointDialog)
        QtCore.QMetaObject.connectSlotsByName(PointDialog)

    def tr(self, string):
        return QtGui.QApplication.translate("PointDialog", string, None, QtGui.QApplication.UnicodeUTF8)

    def retranslateUi(self, PointDialog):
        PointDialog.setWindowTitle(self.tr("Form"))
        self.label_19.setText(self.tr("Point"))
        self.groupBox_8.setTitle(self.tr("Coordinates"))
        self.label_21.setText(self.tr("X:"))
        self.label_22.setText(self.tr("Y:"))
        self.label_23.setText(self.tr("Z:"))
        self.groupBox_7.setTitle(self.tr("Options"))
        self.pointFixed_2.setText(self.tr("Fixed"))
        self.label_20.setText(self.tr("Name:"))
