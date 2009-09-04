# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefsketcher.ui'
#
# Created: Tue May 22 11:24:42 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_sketcherForm(object):
    def setupUi(self, sketcherForm):
        sketcherForm.setObjectName("sketcherForm")
        sketcherForm.resize(QtCore.QSize(QtCore.QRect(0,0,439,417).size()).expandedTo(sketcherForm.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(sketcherForm)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_10 = QtGui.QLabel(sketcherForm)
        self.label_10.setMaximumSize(QtCore.QSize(16777215,30))

        font = QtGui.QFont(self.label_10.font())
        font.setPointSize(16)
        font.setWeight(50)
        font.setBold(False)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.vboxlayout.addWidget(self.label_10)

        self.colorsizeGroupBox = QtGui.QGroupBox(sketcherForm)
        self.colorsizeGroupBox.setObjectName("colorsizeGroupBox")

        self.gridlayout = QtGui.QGridLayout(self.colorsizeGroupBox)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont(self.label.font())
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.label_3 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont(self.label_3.font())
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,3,0,1,1)

        self.fPointClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.fPointClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.fPointClrButton.setFlat(False)
        self.fPointClrButton.setObjectName("fPointClrButton")
        self.gridlayout.addWidget(self.fPointClrButton,2,1,1,1)

        self.fPointSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.fPointSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.fPointSizeSpin.setMinimum(1)
        self.fPointSizeSpin.setObjectName("fPointSizeSpin")
        self.gridlayout.addWidget(self.fPointSizeSpin,2,2,1,1)

        self.dConstraintClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.dConstraintClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.dConstraintClrButton.setFlat(False)
        self.dConstraintClrButton.setObjectName("dConstraintClrButton")
        self.gridlayout.addWidget(self.dConstraintClrButton,3,1,1,1)

        self.angleClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.angleClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.angleClrButton.setFlat(False)
        self.angleClrButton.setObjectName("angleClrButton")
        self.gridlayout.addWidget(self.angleClrButton,4,1,1,1)

        self.label_7 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont(self.label_7.font())
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7,6,0,1,1)

        self.label_6 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont(self.label_6.font())
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,5,0,1,1)

        self.selectClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.selectClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.selectClrButton.setFlat(False)
        self.selectClrButton.setObjectName("selectClrButton")
        self.gridlayout.addWidget(self.selectClrButton,5,1,1,1)

        self.label_4 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont(self.label_4.font())
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,4,0,1,1)

        self.distanceSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.distanceSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.distanceSizeSpin.setMinimum(0)
        self.distanceSizeSpin.setObjectName("distanceSizeSpin")
        self.gridlayout.addWidget(self.distanceSizeSpin,3,2,1,1)

        self.distanceClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.distanceClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.distanceClrButton.setFlat(False)
        self.distanceClrButton.setObjectName("distanceClrButton")
        self.gridlayout.addWidget(self.distanceClrButton,1,1,1,1)

        self.label_5 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont(self.label_5.font())
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,2,0,1,1)

        self.label_2 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont(self.label_2.font())
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.bgClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.bgClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.bgClrButton.setFlat(False)
        self.bgClrButton.setObjectName("bgClrButton")
        self.gridlayout.addWidget(self.bgClrButton,6,1,1,1)

        self.pointClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.pointClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.pointClrButton.setFlat(False)
        self.pointClrButton.setObjectName("pointClrButton")
        self.gridlayout.addWidget(self.pointClrButton,0,1,1,1)

        self.pointSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.pointSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.pointSizeSpin.setMinimum(1)
        self.pointSizeSpin.setObjectName("pointSizeSpin")
        self.gridlayout.addWidget(self.pointSizeSpin,0,2,1,1)

        self.lineSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.lineSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.lineSizeSpin.setMinimum(0)
        self.lineSizeSpin.setObjectName("lineSizeSpin")
        self.gridlayout.addWidget(self.lineSizeSpin,1,2,1,1)
        self.vboxlayout.addWidget(self.colorsizeGroupBox)

        self.gridGroupBox = QtGui.QGroupBox(sketcherForm)
        self.gridGroupBox.setObjectName("gridGroupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.gridGroupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.gridHeightSpin = QtGui.QSpinBox(self.gridGroupBox)
        self.gridHeightSpin.setEnabled(False)
        self.gridHeightSpin.setMaximumSize(QtCore.QSize(60,16777215))
        self.gridHeightSpin.setMaximum(999)
        self.gridHeightSpin.setMinimum(1)
        self.gridHeightSpin.setObjectName("gridHeightSpin")
        self.gridlayout1.addWidget(self.gridHeightSpin,1,4,1,1)

        self.label_8 = QtGui.QLabel(self.gridGroupBox)

        font = QtGui.QFont(self.label_8.font())
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridlayout1.addWidget(self.label_8,0,0,1,1)

        self.label_11 = QtGui.QLabel(self.gridGroupBox)

        font = QtGui.QFont(self.label_11.font())
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridlayout1.addWidget(self.label_11,1,0,1,1)

        self.label_12 = QtGui.QLabel(self.gridGroupBox)
        self.label_12.setMinimumSize(QtCore.QSize(100,0))
        self.label_12.setMaximumSize(QtCore.QSize(16777215,16777215))

        font = QtGui.QFont(self.label_12.font())
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridlayout1.addWidget(self.label_12,1,3,1,1)

        self.showgridCheckBox = QtGui.QCheckBox(self.gridGroupBox)
        self.showgridCheckBox.setChecked(False)
        self.showgridCheckBox.setObjectName("showgridCheckBox")
        self.gridlayout1.addWidget(self.showgridCheckBox,0,1,1,1)

        self.gridWidthSpin = QtGui.QSpinBox(self.gridGroupBox)
        self.gridWidthSpin.setEnabled(False)
        self.gridWidthSpin.setMaximumSize(QtCore.QSize(60,16777215))
        self.gridWidthSpin.setMaximum(999)
        self.gridWidthSpin.setMinimum(1)
        self.gridWidthSpin.setObjectName("gridWidthSpin")
        self.gridlayout1.addWidget(self.gridWidthSpin,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,1,2,1,1)
        self.vboxlayout.addWidget(self.gridGroupBox)

        self.retranslateUi(sketcherForm)
        QtCore.QObject.connect(self.showgridCheckBox,QtCore.SIGNAL("toggled(bool)"),self.gridWidthSpin.setEnabled)
        QtCore.QObject.connect(self.showgridCheckBox,QtCore.SIGNAL("toggled(bool)"),self.gridHeightSpin.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(sketcherForm)

    def retranslateUi(self, sketcherForm):
        sketcherForm.setWindowTitle(QtGui.QApplication.translate("sketcherForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("sketcherForm", "Sketcher Options", None, QtGui.QApplication.UnicodeUTF8))
        self.colorsizeGroupBox.setTitle(QtGui.QApplication.translate("sketcherForm", "Color && Size", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("sketcherForm", "Point:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("sketcherForm", "Distance Constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.fPointClrButton.setToolTip(QtGui.QApplication.translate("sketcherForm", "Fixed point constraint color", None, QtGui.QApplication.UnicodeUTF8))
        self.fPointSizeSpin.setToolTip(QtGui.QApplication.translate("sketcherForm", "Radius of the fixed point constraint", None, QtGui.QApplication.UnicodeUTF8))
        self.dConstraintClrButton.setToolTip(QtGui.QApplication.translate("sketcherForm", "Distance constraint color", None, QtGui.QApplication.UnicodeUTF8))
        self.angleClrButton.setToolTip(QtGui.QApplication.translate("sketcherForm", "Angle constraint color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("sketcherForm", "Background:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("sketcherForm", "Selection:", None, QtGui.QApplication.UnicodeUTF8))
        self.selectClrButton.setToolTip(QtGui.QApplication.translate("sketcherForm", "Selection color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("sketcherForm", "Angle Constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.distanceSizeSpin.setToolTip(QtGui.QApplication.translate("sketcherForm", "Radius of distance constraint", None, QtGui.QApplication.UnicodeUTF8))
        self.distanceClrButton.setToolTip(QtGui.QApplication.translate("sketcherForm", "Line color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("sketcherForm", "Fixed Point Constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("sketcherForm", "Line:", None, QtGui.QApplication.UnicodeUTF8))
        self.bgClrButton.setToolTip(QtGui.QApplication.translate("sketcherForm", "Background color", None, QtGui.QApplication.UnicodeUTF8))
        self.pointClrButton.setToolTip(QtGui.QApplication.translate("sketcherForm", "Point color", None, QtGui.QApplication.UnicodeUTF8))
        self.pointSizeSpin.setToolTip(QtGui.QApplication.translate("sketcherForm", "Radius of the point", None, QtGui.QApplication.UnicodeUTF8))
        self.lineSizeSpin.setToolTip(QtGui.QApplication.translate("sketcherForm", "Radius of line", None, QtGui.QApplication.UnicodeUTF8))
        self.gridGroupBox.setTitle(QtGui.QApplication.translate("sketcherForm", "Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.gridHeightSpin.setToolTip(QtGui.QApplication.translate("sketcherForm", "Height of one cell", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("sketcherForm", "Show Grid:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("sketcherForm", "Width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("sketcherForm", "Height:", None, QtGui.QApplication.UnicodeUTF8))
        self.showgridCheckBox.setToolTip(QtGui.QApplication.translate("sketcherForm", "Grid visibility", None, QtGui.QApplication.UnicodeUTF8))
        self.gridWidthSpin.setToolTip(QtGui.QApplication.translate("sketcherForm", "Width of one cell", None, QtGui.QApplication.UnicodeUTF8))

