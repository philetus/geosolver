# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'constraintdialog.ui'
#
# Created: Wed Oct 17 15:06:50 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConstraintDialog(object):
    def setupUi(self, ConstraintDialog):
        ConstraintDialog.setObjectName("ConstraintDialog")
        ConstraintDialog.resize(QtCore.QSize(QtCore.QRect(0,0,238,479).size()).expandedTo(ConstraintDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ConstraintDialog)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(ConstraintDialog)
        self.tabWidget.setObjectName("tabWidget")

        self.selectionTab = QtGui.QWidget()
        self.selectionTab.setObjectName("selectionTab")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.selectionTab)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.treeWidget = QtGui.QTreeWidget(self.selectionTab)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setObjectName("treeWidget")
        self.vboxlayout1.addWidget(self.treeWidget)
        self.tabWidget.addTab(self.selectionTab,"")

        self.editTab = QtGui.QWidget()
        self.editTab.setObjectName("editTab")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.editTab)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.stackedWidget = QtGui.QStackedWidget(self.editTab)
        self.stackedWidget.setObjectName("stackedWidget")

        self.pointEdit = QtGui.QWidget()
        self.pointEdit.setObjectName("pointEdit")
        self.stackedWidget.addWidget(self.pointEdit)
        self.vboxlayout2.addWidget(self.stackedWidget)
        self.tabWidget.addTab(self.editTab,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(ConstraintDialog)
        self.tabWidget.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ConstraintDialog)

    def retranslateUi(self, ConstraintDialog):
        ConstraintDialog.setWindowTitle(QtGui.QApplication.translate("ConstraintDialog", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setWhatsThis(QtGui.QApplication.translate("ConstraintDialog", "Edit of the different constraints and other objects", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0,QtGui.QApplication.translate("ConstraintDialog", "column 1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.clear()

        item = QtGui.QTreeWidgetItem(self.treeWidget)
        item.setText(0,QtGui.QApplication.translate("ConstraintDialog", "Points", None, QtGui.QApplication.UnicodeUTF8))

        item1 = QtGui.QTreeWidgetItem(self.treeWidget)
        item1.setText(0,QtGui.QApplication.translate("ConstraintDialog", "Distances", None, QtGui.QApplication.UnicodeUTF8))

        item2 = QtGui.QTreeWidgetItem(self.treeWidget)
        item2.setText(0,QtGui.QApplication.translate("ConstraintDialog", "Angles", None, QtGui.QApplication.UnicodeUTF8))

        item3 = QtGui.QTreeWidgetItem(self.treeWidget)
        item3.setText(0,QtGui.QApplication.translate("ConstraintDialog", "Fixed Points", None, QtGui.QApplication.UnicodeUTF8))

        item4 = QtGui.QTreeWidgetItem(self.treeWidget)
        item4.setText(0,QtGui.QApplication.translate("ConstraintDialog", "Lines", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.selectionTab), QtGui.QApplication.translate("ConstraintDialog", "Se&lection", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editTab), QtGui.QApplication.translate("ConstraintDialog", "E&dit", None, QtGui.QApplication.UnicodeUTF8))

