from includes import *
from ui_distanceDialog import *

class DistanceDialog(QtGui.QWidget):
	def __init__(self, widget):
		QtGui.QWidget.__init__(self, widget)
		self.ui = Ui_DistanceDialog()
		self.ui.setupUi(self)
		self.panel = widget
		self.createTriggers()
		self.prototypeManager = PrototypeManager()
		self.dName = ""
		
	def createTriggers(self):
		QtCore.QObject.connect(self.ui.distanceName,QtCore.SIGNAL("textEdited(const QString &)"), self.nameEdited)
		QtCore.QObject.connect(self.ui.optionDistance,QtCore.SIGNAL("valueChanged(double)"), self.newDistance)
		QtCore.QObject.connect(self.ui.DistanceFixed,QtCore.SIGNAL("stateChanged(int)"), self.fixedChange)
		QtCore.QObject.connect(self.ui.getRanges,QtCore.SIGNAL("clicked()"), self.setParameterRange)
		
	def update(self, objectInfo):
		self.ui.distanceName.setText(objectInfo.name)
		self.setTextColor(self.ui.distanceName, QtCore.Qt.black)
		self.dName = objectInfo.name
		
		self.ui.optionDistance.setValue(objectInfo.distance)
		self.ui.infoDPoint1Name.setText(objectInfo.pointBegin.name)
		self.ui.infoDPoint1Coords.setText("(" + str(round(objectInfo.pointBegin.position[0], 2)) + " ; " +
									  str(round(objectInfo.pointBegin.position[1], 2)) + " ; " +
									  str(round(objectInfo.pointBegin.position[2], 2)) + ")")
		
		self.ui.infoDPoint2Name.setText(objectInfo.pointEnd.name)
		self.ui.infoDPoint2Coords.setText("(" + str(round(objectInfo.pointEnd.position[0], 2)) + " ; " +
									  str(round(objectInfo.pointEnd.position[1], 2)) + " ; " +
									  str(round(objectInfo.pointEnd.position[2], 2)) + ")")			
		
		if objectInfo.objType == ObjectType.DISTANCE_CONSTRAINT and objectInfo.fixed:
			self.ui.DistanceFixed.setCheckState(QtCore.Qt.Checked)
			self.ui.optionDistance.setDisabled(True)
		else:
			self.ui.DistanceFixed.setCheckState(QtCore.Qt.Unchecked)
			self.ui.optionDistance.setDisabled(False)
	
	def reset(self):
		self.ui.parRangeList.clear()
	
	def setParameterRange(self):
		distanceObject = self.prototypeManager.objectSelected
		if distanceObject != None:
			if distanceObject.objType == ObjectType.DISTANCE_CONSTRAINT:
				pRange = self.prototypeManager.getParameterRange(distanceObject)
				if pRange != [] and len(pRange.intervals) > 0:
					for interval in pRange.intervals:
						self.ui.parRangeList.addItem(str(interval.left_value()) + " - " + str(interval.right_value()))
			
	def nameEdited(self, newName):
		if self.prototypeManager.isNameUnique(self.dName, str(newName)):
			self.setTextColor(self.ui.distanceName, QtCore.Qt.black)
			
			if self.prototypeManager.setObjectName(self.dName, str(newName)):
				self.panel.renameItem(self.dName, str(newName))
				self.dName = str(newName)
		else:
			self.setTextColor(self.ui.distanceName, QtCore.Qt.red)
	
	def fixedChange(self, state):
		if self.prototypeManager.objectSelected != None:
			if self.prototypeManager.objectSelected.objType == ObjectType.DISTANCE_CONSTRAINT:
				if state == QtCore.Qt.Checked:
					self.prototypeManager.objectSelected.fixed = True
					self.ui.optionDistance.setDisabled(True)
				else:
					self.prototypeManager.objectSelected.fixed = False
					self.ui.optionDistance.setDisabled(False)
				
	def newDistance(self, newDistance):
		if self.prototypeManager.objectSelected != None:
			if not self.prototypeManager.objectSelected.fixed:
				if self.prototypeManager.objectSelected.objType == ObjectType.DISTANCE_CONSTRAINT:
					self.prototypeManager.updateConstraint(self.prototypeManager.objectSelected, newDistance)
				else:
					self.prototypeManager.objectSelected.distance = newDistance
	
	def setTextColor(self, textField, color):
		palette = QtGui.QPalette(textField.palette())
		palette.setColor(QtGui.QPalette.Text, color)
		textField.setPalette(palette)	