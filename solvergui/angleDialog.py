from includes import *
from ui_angleDialog import *

class AngleDialog(QtGui.QWidget):
	def __init__(self, widget, mainWindow):
		QtGui.QWidget.__init__(self, widget)
		self.ui = Ui_AngleDialog()
		self.ui.setupUi(self)
		self.panel = widget
		self.createTriggers()
		self.prototypeManager = PrototypeManager()
		self.mainWindow = mainWindow
		self.aName = ""
		
	def createTriggers(self):
		QtCore.QObject.connect(self.ui.angleName,QtCore.SIGNAL("textEdited(const QString &)"), self.nameEdited)
		QtCore.QObject.connect(self.ui.optionAngle,QtCore.SIGNAL("valueChanged(double)"), self.newAngle)
		QtCore.QObject.connect(self.ui.angleFixed,QtCore.SIGNAL("stateChanged(int)"), self.fixedChange)
		QtCore.QObject.connect(self.ui.getRangesButton,QtCore.SIGNAL("clicked()"), self.setParameterRange)

	def update(self, objectInfo):
		self.ui.angleName.setText(objectInfo.name)
		self.setTextColor(self.ui.angleName, QtCore.Qt.black)
		self.aName = objectInfo.name
		
		if objectInfo.angle != None:
			self.ui.optionAngle.setValue(objectInfo.angle)
		self.ui.infoAPoint1Name.setText(objectInfo.pointBegin.name)
		self.ui.infoAPoint1Coords.setText("(" + str(round(objectInfo.pointBegin.position[0], 2)) + " ; " +
									  str(round(objectInfo.pointBegin.position[1], 2)) + " ; " +
									  str(round(objectInfo.pointBegin.position[2], 2)) + ")")
		
		self.ui.infoAPoint2Name.setText(objectInfo.pointMiddle.name)
		self.ui.infoAPoint2Coords.setText("(" + str(round(objectInfo.pointMiddle.position[0], 2)) + " ; " +
									  str(round(objectInfo.pointMiddle.position[1], 2)) + " ; " +
									  str(round(objectInfo.pointMiddle.position[2], 2)) + ")")
		
		self.ui.infoAPoint3Name.setText(objectInfo.pointEnd.name)
		self.ui.infoAPoint3Coords.setText("(" + str(round(objectInfo.pointEnd.position[0], 2)) + " ; " +
									  str(round(objectInfo.pointEnd.position[1], 2)) + " ; " +
									  str(round(objectInfo.pointEnd.position[2], 2)) + ")")

		if objectInfo.objType == ObjectType.ANGLE_CONSTRAINT and objectInfo.fixed:
			self.ui.angleFixed.setCheckState(QtCore.Qt.Checked)
			self.ui.optionAngle.setDisabled(True)
		else:
			self.ui.angleFixed.setCheckState(QtCore.Qt.Unchecked)
			self.ui.optionAngle.setDisabled(False)			
	
	def reset(self):
		self.ui.parRangeList.clear()
	
	def setParameterRange(self):
		angleObject = self.prototypeManager.objectSelected
		if angleObject != None:
			if angleObject.objType == ObjectType.ANGLE_CONSTRAINT:
				pRange = self.prototypeManager.getParameterRange(angleObject)
				if pRange != [] and len(pRange.intervals) > 0:
					for interval in pRange.intervals:
						self.ui.parRangeList.addItem(str(interval.left_value()) + " - " + str(interval.right_value()))
		
	def nameEdited(self, newName):
		if self.prototypeManager.isNameUnique(self.aName, str(newName)):
			self.setTextColor(self.ui.angleName, QtCore.Qt.black)
			
			if self.prototypeManager.setObjectName(self.aName, str(newName)):
				self.panel.renameItem(self.aName, str(newName))
				self.aName = str(newName)
		else:
			self.setTextColor(self.ui.angleName, QtCore.Qt.red)
	
	def fixedChange(self, state):
		if self.prototypeManager.objectSelected != None:
			if self.prototypeManager.objectSelected.objType == ObjectType.ANGLE_CONSTRAINT:
				if state == QtCore.Qt.Checked:
					self.prototypeManager.objectSelected.fixed = True
					self.ui.optionAngle.setDisabled(True)
				else:
					self.prototypeManager.objectSelected.fixed = False
					self.ui.optionAngle.setDisabled(False)

	def newAngle(self, newAngle):
		if self.prototypeManager.objectSelected != None:
			if self.prototypeManager.objectSelected.objType == ObjectType.ANGLE_CONSTRAINT:
				self.prototypeManager.updateConstraint(self.prototypeManager.objectSelected, newAngle)
				#self.mainWindow.updateWindow()
			else:
				self.prototypeManager.objectSelected.angle = newAngle
	
	def setTextColor(self, textField, color):
		palette = QtGui.QPalette(textField.palette())
		palette.setColor(QtGui.QPalette.Text, color)
		textField.setPalette(palette)		
