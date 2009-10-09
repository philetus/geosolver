# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefviews.ui'
#
# Created: Mon Oct 15 21:18:35 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_viewsForm(object):
    def setupUi(self, viewsForm):
        viewsForm.setObjectName("viewsForm")
        viewsForm.resize(QtCore.QSize(QtCore.QRect(0,0,439,453).size()).expandedTo(viewsForm.minimumSizeHint()))

        self.tabWidget = QtGui.QTabWidget(viewsForm)
        self.tabWidget.setGeometry(QtCore.QRect(9,9,421,431))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        self.compositionTab = QtGui.QWidget()
        self.compositionTab.setObjectName("compositionTab")

        self.treeGroupBox = QtGui.QGroupBox(self.compositionTab)
        self.treeGroupBox.setGeometry(QtCore.QRect(10,60,399,150))
        self.treeGroupBox.setMaximumSize(QtCore.QSize(16777215,150))
        self.treeGroupBox.setObjectName("treeGroupBox")

        self.label = QtGui.QLabel(self.treeGroupBox)
        self.label.setGeometry(QtCore.QRect(11,48,151,22))

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.alignTreeComboBox = QtGui.QComboBox(self.treeGroupBox)
        self.alignTreeComboBox.setGeometry(QtCore.QRect(120,50,93,22))
        self.alignTreeComboBox.setMaximumSize(QtCore.QSize(100,16777215))
        self.alignTreeComboBox.setObjectName("alignTreeComboBox")

        self.radioConnectionButton = QtGui.QRadioButton(self.treeGroupBox)
        self.radioConnectionButton.setGeometry(QtCore.QRect(120,90,56,23))
        self.radioConnectionButton.setMinimumSize(QtCore.QSize(0,0))
        self.radioConnectionButton.setObjectName("radioConnectionButton")

        self.label_2 = QtGui.QLabel(self.treeGroupBox)
        self.label_2.setGeometry(QtCore.QRect(10,80,85,41))

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.radioCurvedButton = QtGui.QRadioButton(self.treeGroupBox)
        self.radioCurvedButton.setGeometry(QtCore.QRect(190,90,67,23))
        self.radioCurvedButton.setMinimumSize(QtCore.QSize(0,0))
        self.radioCurvedButton.setObjectName("radioCurvedButton")

        self.label_10 = QtGui.QLabel(self.compositionTab)
        self.label_10.setGeometry(QtCore.QRect(10,10,399,30))
        self.label_10.setMaximumSize(QtCore.QSize(16777215,30))

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(50)
        font.setBold(False)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.tabWidget.addTab(self.compositionTab,"")

        self.solutionTab = QtGui.QWidget()
        self.solutionTab.setObjectName("solutionTab")

        self.label_11 = QtGui.QLabel(self.solutionTab)
        self.label_11.setGeometry(QtCore.QRect(20,20,371,30))
        self.label_11.setMaximumSize(QtCore.QSize(16777215,30))

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(50)
        font.setBold(False)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.gridGroupBox = QtGui.QGroupBox(self.solutionTab)
        self.gridGroupBox.setGeometry(QtCore.QRect(20,290,371,93))
        self.gridGroupBox.setObjectName("gridGroupBox")

        self.gridlayout = QtGui.QGridLayout(self.gridGroupBox)
        self.gridlayout.setMargin(9)
        self.gridlayout.setObjectName("gridlayout")

        self.svGridHeightSpin = QtGui.QSpinBox(self.gridGroupBox)
        self.svGridHeightSpin.setEnabled(False)
        self.svGridHeightSpin.setMaximumSize(QtCore.QSize(60,16777215))
        self.svGridHeightSpin.setMinimum(1)
        self.svGridHeightSpin.setMaximum(999)
        self.svGridHeightSpin.setObjectName("svGridHeightSpin")
        self.gridlayout.addWidget(self.svGridHeightSpin,1,4,1,1)

        self.label_8 = QtGui.QLabel(self.gridGroupBox)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridlayout.addWidget(self.label_8,0,0,1,1)

        self.label_12 = QtGui.QLabel(self.gridGroupBox)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridlayout.addWidget(self.label_12,1,0,1,1)

        self.label_13 = QtGui.QLabel(self.gridGroupBox)
        self.label_13.setMinimumSize(QtCore.QSize(100,0))
        self.label_13.setMaximumSize(QtCore.QSize(16777215,16777215))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridlayout.addWidget(self.label_13,1,3,1,1)

        self.svShowgrid = QtGui.QCheckBox(self.gridGroupBox)
        self.svShowgrid.setChecked(False)
        self.svShowgrid.setObjectName("svShowgrid")
        self.gridlayout.addWidget(self.svShowgrid,0,1,1,1)

        self.svGridWidthSpin = QtGui.QSpinBox(self.gridGroupBox)
        self.svGridWidthSpin.setEnabled(False)
        self.svGridWidthSpin.setMaximumSize(QtCore.QSize(60,16777215))
        self.svGridWidthSpin.setMinimum(1)
        self.svGridWidthSpin.setMaximum(999)
        self.svGridWidthSpin.setObjectName("svGridWidthSpin")
        self.gridlayout.addWidget(self.svGridWidthSpin,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,2,1,1)

        self.colorsizeGroupBox = QtGui.QGroupBox(self.solutionTab)
        self.colorsizeGroupBox.setGeometry(QtCore.QRect(20,50,371,231))
        self.colorsizeGroupBox.setObjectName("colorsizeGroupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.colorsizeGroupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_3 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,0,0,1,1)

        self.svPointClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.svPointClrButton.setMinimumSize(QtCore.QSize(80,0))
        self.svPointClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.svPointClrButton.setFlat(False)
        self.svPointClrButton.setObjectName("svPointClrButton")
        self.gridlayout1.addWidget(self.svPointClrButton,0,1,1,1)

        self.svPointSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.svPointSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.svPointSizeSpin.setMinimum(1)
        self.svPointSizeSpin.setObjectName("svPointSizeSpin")
        self.gridlayout1.addWidget(self.svPointSizeSpin,0,2,1,1)

        self.vPoint = QtGui.QCheckBox(self.colorsizeGroupBox)
        self.vPoint.setObjectName("vPoint")
        self.gridlayout1.addWidget(self.vPoint,0,3,1,1)

        self.label_14 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridlayout1.addWidget(self.label_14,1,0,1,1)

        self.svDistanceClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.svDistanceClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.svDistanceClrButton.setFlat(False)
        self.svDistanceClrButton.setObjectName("svDistanceClrButton")
        self.gridlayout1.addWidget(self.svDistanceClrButton,1,1,1,1)

        self.svLineSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.svLineSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.svLineSizeSpin.setMinimum(1)
        self.svLineSizeSpin.setObjectName("svLineSizeSpin")
        self.gridlayout1.addWidget(self.svLineSizeSpin,1,2,1,1)

        self.vLine = QtGui.QCheckBox(self.colorsizeGroupBox)
        self.vLine.setObjectName("vLine")
        self.gridlayout1.addWidget(self.vLine,1,3,1,1)

        self.label_9 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridlayout1.addWidget(self.label_9,2,0,1,1)

        self.svfPointClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.svfPointClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.svfPointClrButton.setFlat(False)
        self.svfPointClrButton.setObjectName("svfPointClrButton")
        self.gridlayout1.addWidget(self.svfPointClrButton,2,1,1,1)

        self.svfPointSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.svfPointSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.svfPointSizeSpin.setMinimum(1)
        self.svfPointSizeSpin.setObjectName("svfPointSizeSpin")
        self.gridlayout1.addWidget(self.svfPointSizeSpin,2,2,1,1)

        self.vfPoint = QtGui.QCheckBox(self.colorsizeGroupBox)
        self.vfPoint.setObjectName("vfPoint")
        self.gridlayout1.addWidget(self.vfPoint,2,3,1,1)

        self.label_4 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,3,0,1,1)

        self.svdConstraintClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.svdConstraintClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.svdConstraintClrButton.setFlat(False)
        self.svdConstraintClrButton.setObjectName("svdConstraintClrButton")
        self.gridlayout1.addWidget(self.svdConstraintClrButton,3,1,1,1)

        self.svDistanceSizeSpin = QtGui.QSpinBox(self.colorsizeGroupBox)
        self.svDistanceSizeSpin.setMaximumSize(QtCore.QSize(50,16777215))
        self.svDistanceSizeSpin.setMinimum(1)
        self.svDistanceSizeSpin.setObjectName("svDistanceSizeSpin")
        self.gridlayout1.addWidget(self.svDistanceSizeSpin,3,2,1,1)

        self.vDistance = QtGui.QCheckBox(self.colorsizeGroupBox)
        self.vDistance.setObjectName("vDistance")
        self.gridlayout1.addWidget(self.vDistance,3,3,1,1)

        self.label_5 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,4,0,1,1)

        self.svAngleClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.svAngleClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.svAngleClrButton.setFlat(False)
        self.svAngleClrButton.setObjectName("svAngleClrButton")
        self.gridlayout1.addWidget(self.svAngleClrButton,4,1,1,1)

        self.vAngle = QtGui.QCheckBox(self.colorsizeGroupBox)
        self.vAngle.setObjectName("vAngle")
        self.gridlayout1.addWidget(self.vAngle,4,3,1,1)

        self.label_7 = QtGui.QLabel(self.colorsizeGroupBox)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridlayout1.addWidget(self.label_7,5,0,1,1)

        self.svBgClrButton = QtGui.QPushButton(self.colorsizeGroupBox)
        self.svBgClrButton.setMaximumSize(QtCore.QSize(100,16777215))
        self.svBgClrButton.setFlat(False)
        self.svBgClrButton.setObjectName("svBgClrButton")
        self.gridlayout1.addWidget(self.svBgClrButton,5,1,1,1)
        self.tabWidget.addTab(self.solutionTab,"")

        self.retranslateUi(viewsForm)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.svShowgrid,QtCore.SIGNAL("toggled(bool)"),self.svGridHeightSpin.setEnabled)
        QtCore.QObject.connect(self.svShowgrid,QtCore.SIGNAL("toggled(bool)"),self.svGridWidthSpin.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(viewsForm)

    def retranslateUi(self, viewsForm):
        viewsForm.setWindowTitle(QtGui.QApplication.translate("viewsForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.treeGroupBox.setTitle(QtGui.QApplication.translate("viewsForm", "Tree Visualisation", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("viewsForm", "Alignment:", None, QtGui.QApplication.UnicodeUTF8))
        self.alignTreeComboBox.addItem(QtGui.QApplication.translate("viewsForm", "Top", None, QtGui.QApplication.UnicodeUTF8))
        self.alignTreeComboBox.addItem(QtGui.QApplication.translate("viewsForm", "Bottom", None, QtGui.QApplication.UnicodeUTF8))
        self.alignTreeComboBox.addItem(QtGui.QApplication.translate("viewsForm", "Right", None, QtGui.QApplication.UnicodeUTF8))
        self.alignTreeComboBox.addItem(QtGui.QApplication.translate("viewsForm", "Left", None, QtGui.QApplication.UnicodeUTF8))
        self.radioConnectionButton.setText(QtGui.QApplication.translate("viewsForm", "Lines", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("viewsForm", "Connection:", None, QtGui.QApplication.UnicodeUTF8))
        self.radioCurvedButton.setText(QtGui.QApplication.translate("viewsForm", "Curved", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("viewsForm", "Decomposition View Options", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.compositionTab), QtGui.QApplication.translate("viewsForm", "Decomposition", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("viewsForm", "Solution View Options", None, QtGui.QApplication.UnicodeUTF8))
        self.gridGroupBox.setTitle(QtGui.QApplication.translate("viewsForm", "Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.svGridHeightSpin.setToolTip(QtGui.QApplication.translate("viewsForm", "Height of one cell", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("viewsForm", "Show Grid:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("viewsForm", "Width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("viewsForm", "Height:", None, QtGui.QApplication.UnicodeUTF8))
        self.svShowgrid.setToolTip(QtGui.QApplication.translate("viewsForm", "Grid visibility", None, QtGui.QApplication.UnicodeUTF8))
        self.svGridWidthSpin.setToolTip(QtGui.QApplication.translate("viewsForm", "Width of one cell", None, QtGui.QApplication.UnicodeUTF8))
        self.colorsizeGroupBox.setTitle(QtGui.QApplication.translate("viewsForm", "Color && Size && Visibility", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("viewsForm", "Point:", None, QtGui.QApplication.UnicodeUTF8))
        self.svPointClrButton.setToolTip(QtGui.QApplication.translate("viewsForm", "Point color", None, QtGui.QApplication.UnicodeUTF8))
        self.svPointSizeSpin.setToolTip(QtGui.QApplication.translate("viewsForm", "Radius of the point", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("viewsForm", "Line:", None, QtGui.QApplication.UnicodeUTF8))
        self.svDistanceClrButton.setToolTip(QtGui.QApplication.translate("viewsForm", "Line color", None, QtGui.QApplication.UnicodeUTF8))
        self.svLineSizeSpin.setToolTip(QtGui.QApplication.translate("viewsForm", "Radius of line", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("viewsForm", "Fixed Point Constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.svfPointClrButton.setToolTip(QtGui.QApplication.translate("viewsForm", "Fixed point constraint color", None, QtGui.QApplication.UnicodeUTF8))
        self.svfPointSizeSpin.setToolTip(QtGui.QApplication.translate("viewsForm", "Radius of the fixed point constraint", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("viewsForm", "Distance Constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.svdConstraintClrButton.setToolTip(QtGui.QApplication.translate("viewsForm", "Distance constraint color", None, QtGui.QApplication.UnicodeUTF8))
        self.svDistanceSizeSpin.setToolTip(QtGui.QApplication.translate("viewsForm", "Radius of distance constraint", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("viewsForm", "Angle Constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.svAngleClrButton.setToolTip(QtGui.QApplication.translate("viewsForm", "Angle constraint color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("viewsForm", "Background:", None, QtGui.QApplication.UnicodeUTF8))
        self.svBgClrButton.setToolTip(QtGui.QApplication.translate("viewsForm", "Background color", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.solutionTab), QtGui.QApplication.translate("viewsForm", "Solution", None, QtGui.QApplication.UnicodeUTF8))

