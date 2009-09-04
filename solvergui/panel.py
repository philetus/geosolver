from includes import *
from pointDialog import *
from distanceDialog import *
from angleDialog import *
from ui_constraint import *

from prototypeObjects import *

class Panel(QtGui.QWidget):
	def __init__(self, mainWindow, widget):
		QtGui.QWidget.__init__(self, widget)
		self.ui = Ui_ConstraintDialog()
		self.ui.setupUi(self)
		self.mainWindow = mainWindow
		self.prototypeManager = PrototypeManager()
		self.prototypeManager.setPanel(self)
		self.ui.treeWidget.setItemHidden(self.ui.treeWidget.headerItem(), True)
		self.addConstraintPages()
		self.createTriggers()
		self.handleTrigger = True
		self.updateSelection = True
	
	def addConstraintPages(self):
		self.ui.stackedWidget.addWidget(PointDialog(self))
		self.ui.stackedWidget.addWidget(DistanceDialog(self))
		self.ui.stackedWidget.addWidget(AngleDialog(self, self.mainWindow))

	def createTriggers(self):
		QtCore.QObject.connect(self.ui.treeWidget,QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem *, QTreeWidgetItem *)"), self.selectionChanged)
		#QtCore.QObject.connect(self.ui.tabWidget,QtCore.SIGNAL("currentChanged(int)"), self.tabChanged)
	
	def reset(self):
		index = self.ui.stackedWidget.currentIndex()
		for i in range(self.ui.stackedWidget.count()):
			self.ui.stackedWidget.setCurrentIndex(i+1)
			self.ui.stackedWidget.currentWidget().reset()
	
	def addItemToSelectionList(self, objectName, objectType):
		newWidget = QtGui.QTreeWidgetItem()
		newWidget.setText(0, objectName)
		
		if objectType == ObjectType.POINT:
			itemList = self.ui.treeWidget.topLevelItem(0)
		elif objectType == ObjectType.DISTANCE_CONSTRAINT:
			itemList = self.ui.treeWidget.topLevelItem(1)
		elif objectType == ObjectType.ANGLE_CONSTRAINT:
			itemList = self.ui.treeWidget.topLevelItem(2)
		elif objectType == ObjectType.FIXED_POINT:
			itemList = self.ui.treeWidget.topLevelItem(3)
		elif objectType == ObjectType.DISTANCE_HELPER:
			itemList = self.ui.treeWidget.topLevelItem(4)
		else:
			return
		
		itemList.addChild(newWidget)
	
	def selectionChanged(self, currTreeItem,  prevTreeItem):
		if self.handleTrigger:
			self.prototypeManager.selectObjectByName(currTreeItem.text(0))
			self.updateEdit()
			#self.mainWindow.updateWindow()
	
	def selectItemByName(self, name):
		self.updateSelectionList(name)
		self.updateEdit()
	
	def renameItem(self, oldName, newName):
		itemList = self.ui.treeWidget.findItems(oldName, QtCore.Qt.MatchCaseSensitive | QtCore.Qt.MatchRecursive,0)
		if len(itemList) > 0:
			itemList[0].setText(0,newName)

	def removeItem(self, name):
		itemList = self.ui.treeWidget.findItems(name, QtCore.Qt.MatchCaseSensitive | QtCore.Qt.MatchRecursive,0)
		if len(itemList) > 0:
			parentItem = itemList[0].parent()
			parentItem.takeChild(parentItem.indexOfChild(itemList[0]))
			
	def removeItems(self, itemNames):
		self.handleTrigger = False
		for name in itemNames:
			self.removeItem(name)
		self.handleTrigger = True
		
	def keyPressEvent(self, keyEvent):
		if keyEvent.key() == QtCore.Qt.Key_Delete:
			self.prototypeManager.deleteObject(self.prototypeManager.objectSelected)
			self.mainWindow.updateWindow()
    			
	def updateSelectionList(self, name):
		itemList = self.ui.treeWidget.findItems(name, QtCore.Qt.MatchCaseSensitive | QtCore.Qt.MatchRecursive,0)
		if len(itemList) > 0:
			treeItem = itemList[0]
			self.ui.treeWidget.setCurrentItem(treeItem)
		
	def updateEdit(self):
		if self.prototypeManager.objectSelected != None:
			obj = self.prototypeManager.objectSelected
			if obj.objType == ObjectType.POINT:
				self.ui.stackedWidget.setCurrentIndex(1)
				if not self.updateSelection:
					self.ui.stackedWidget.currentWidget().needUpdateObject = False
					self.ui.stackedWidget.currentWidget().update(obj)
					self.ui.stackedWidget.currentWidget().needUpdateObject = True
				else:
					self.ui.stackedWidget.currentWidget().update(obj)
			elif obj.objType == ObjectType.DISTANCE_CONSTRAINT:
				self.ui.stackedWidget.setCurrentIndex(2)
				self.ui.stackedWidget.currentWidget().update(obj)
			elif obj.objType == ObjectType.ANGLE_CONSTRAINT:
				self.ui.stackedWidget.setCurrentIndex(3)
				self.ui.stackedWidget.currentWidget().update(obj)
			elif obj.objType == ObjectType.FIXED_POINT:
				self.ui.stackedWidget.setCurrentIndex(1)
				if not self.updateSelection:
					self.ui.stackedWidget.currentWidget().needUpdateObject = False
					self.ui.stackedWidget.currentWidget().update(obj)
					self.ui.stackedWidget.currentWidget().needUpdateObject = True
				else:
					self.ui.stackedWidget.currentWidget().update(obj)
			elif obj.objType == ObjectType.DISTANCE_HELPER:
				self.ui.stackedWidget.setCurrentIndex(2)
				self.ui.stackedWidget.currentWidget().update(obj)
		else:
			self.ui.stackedWidget.setCurrentIndex(0)

	def updateMainWindow(self):	
		self.mainWindow.updateWindow()
		
	
