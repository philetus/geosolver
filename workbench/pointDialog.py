from includes import *
from ui_pointDialog import *

class PointDialog(QtGui.QWidget):
	def __init__(self, widget):
		QtGui.QWidget.__init__(self, widget)
		self.panel = widget
		self.ui = Ui_PointDialog()
		self.ui.setupUi(self)
		self.createTriggers()
		self.prototypeManager = PrototypeManager()
		self.pName = ""
		self.needUpdateObject = True
	
	def createTriggers(self):
		QtCore.QObject.connect(self.ui.pointName_2,QtCore.SIGNAL("textEdited(const QString &)"), self.nameEdited)
		QtCore.QObject.connect(self.ui.pointCoordX_2,QtCore.SIGNAL("valueChanged(double)"), self.newXPos)
		QtCore.QObject.connect(self.ui.pointCoordY_2,QtCore.SIGNAL("valueChanged(double)"), self.newYPos)
		QtCore.QObject.connect(self.ui.pointCoordZ_2,QtCore.SIGNAL("valueChanged(double)"), self.newZPos)
		QtCore.QObject.connect(self.ui.pointFixed_2,QtCore.SIGNAL("stateChanged(int)"), self.fixedChange)
		
	def update(self, objectInfo):
		self.ui.pointName_2.setText(objectInfo.name)
		self.setTextColor(self.ui.pointName_2, QtCore.Qt.black)
		self.pName = objectInfo.name
		self.ui.pointCoordX_2.setValue(objectInfo.position[0])
		self.ui.pointCoordY_2.setValue(objectInfo.position[1])
		self.ui.pointCoordZ_2.setValue(objectInfo.position[2])
		
		if objectInfo.objType == ObjectType.FIXED_POINT:
			self.ui.pointFixed_2.setCheckState(QtCore.Qt.Checked)
		else:
			self.ui.pointFixed_2.setCheckState(QtCore.Qt.Unchecked)
	
	def reset(self):
		pass
			
	def nameEdited(self, newName):
		#print " triggered nameEdited"
		if self.prototypeManager.isNameUnique(self.pName, str(newName)):
			self.setTextColor(self.ui.pointName_2, QtCore.Qt.black)
			
			if self.prototypeManager.setObjectName(self.pName, str(newName)):
				self.panel.renameItem(self.pName, str(newName))
				self.pName = str(newName)
		else:
			self.setTextColor(self.ui.pointName_2, QtCore.Qt.red)

	def setTextColor(self, textField, color):
		palette = QtGui.QPalette(textField.palette())
		palette.setColor(QtGui.QPalette.Text, color)
		textField.setPalette(palette)
	
	def newXPos(self, xPos):
		#print " triggered newXPos"
		if self.prototypeManager.objectSelected != None and self.needUpdateObject:
			obj = self.prototypeManager.objectSelected
			if obj.objType == ObjectType.POINT or obj.objType == ObjectType.FIXED_POINT:
				obj.position[0] = xPos
		if self.needUpdateObject:
			self.updateObjects()
		
	def newYPos(self, yPos):
		#print " triggered newYPos"
		if self.prototypeManager.objectSelected != None:
			obj = self.prototypeManager.objectSelected
			if obj.objType == ObjectType.POINT or obj.objType == ObjectType.FIXED_POINT:
				obj.position[1] = yPos
		if self.needUpdateObject:
			self.updateObjects()
		
	def newZPos(self, zPos):
		#print " triggered newZPos"
		if self.prototypeManager.objectSelected != None:
			obj = self.prototypeManager.objectSelected
			if obj.objType == ObjectType.POINT or obj.objType == ObjectType.FIXED_POINT:
				obj.position[2] = zPos
		if self.needUpdateObject:
			self.updateObjects()			

	def fixedChange(self, state):
		#print " triggered fixed"
		if self.prototypeManager.objectSelected != None:
			obj = self.prototypeManager.objectSelected
			if state == QtCore.Qt.Unchecked and obj.objType == ObjectType.FIXED_POINT:
				# remove constraint
				self.prototypeManager.removeConstraint(obj)
				self.panel.removeItem(obj.name)
				self.panel.addItemToSelectionList(obj.name, ObjectType.POINT)
			elif state == QtCore.Qt.Checked and obj.objType == ObjectType.POINT:
				# add constraint
				self.prototypeManager.addConstraint(obj)
				self.panel.removeItem(obj.name)
				self.panel.addItemToSelectionList(obj.name, ObjectType.FIXED_POINT)
			self.updateObjects()	
			
			
	def updateObjects(self):
		#print " triggered Update"
		self.prototypeManager.updateObjects()
		self.panel.updateMainWindow()
		

		