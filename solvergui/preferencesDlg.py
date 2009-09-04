from includes import *
from parameters import Settings
from ui_preferencesDlg import Ui_preferencesDialog
from ui_prefSketcher import Ui_sketcherForm
from ui_prefViews import Ui_viewsForm

class Preferences:
	def __init__(self, preferenceHandler):
		self.preferenceHandler = preferenceHandler
		self.widget = QtGui.QWidget()
		self.name = ""
		self.settings = Settings()
	
	def updateIconColor(self, icon, iconButton, color):
		if not color == None:
			icon.fill(color)	
		else:
			icon.fill(QtGui.QColor(0,0,0))
	
		iconButton.setIcon(QtGui.QIcon(icon))

class SketcherPreferences(Preferences):
	def __init__(self, preferenceHandler):	
		Preferences.__init__(self, preferenceHandler)
		self.ui = Ui_sketcherForm()
		self.ui.setupUi(self.widget)
		self.name = "Sketcher" 
		self.preferenceHandler.addPreferencePage(self.name, self.widget)
		self.fPointIcon = QtGui.QPixmap(40,20)
		self.dConstraintIcon = QtGui.QPixmap(40,20)
		self.angleIcon = QtGui.QPixmap(40,20)
		self.selectionIcon = QtGui.QPixmap(40,20)
		self.distanceIcon = QtGui.QPixmap(40,20)
		self.backgroundIcon = QtGui.QPixmap(40,20)
		self.pointIcon = QtGui.QPixmap(40,20)
		self.setIcons()
		self.setValues()
		self.createTriggers()
	
	def setIcons(self):
		self.fPointIcon.fill(self.settings.sketcherData.fPointColor)
		self.ui.fPointClrButton.setIcon(QtGui.QIcon(self.fPointIcon))
		self.dConstraintIcon.fill(self.settings.sketcherData.distanceColor)
		self.ui.dConstraintClrButton.setIcon(QtGui.QIcon(self.dConstraintIcon))
		self.angleIcon.fill(self.settings.sketcherData.angleColor)
		self.ui.angleClrButton.setIcon(QtGui.QIcon(self.angleIcon))
		self.selectionIcon.fill(self.settings.sketcherData.selectColor)
		self.ui.selectClrButton.setIcon(QtGui.QIcon(self.selectionIcon))
		self.distanceIcon.fill(self.settings.sketcherData.lineColor)
		self.ui.distanceClrButton.setIcon(QtGui.QIcon(self.distanceIcon))
		self.backgroundIcon.fill(self.settings.sketcherData.bgColor)
		self.ui.bgClrButton.setIcon(QtGui.QIcon(self.backgroundIcon))
		self.pointIcon.fill(self.settings.sketcherData.pointColor)
		self.ui.pointClrButton.setIcon(QtGui.QIcon(self.pointIcon))
	
	def setValues(self):
		self.ui.pointSizeSpin.setValue(self.settings.sketcherData.pointRadius)
		self.ui.fPointSizeSpin.setValue(self.settings.sketcherData.fPointRadius)
		self.ui.lineSizeSpin.setValue(self.settings.sketcherData.lineRadius)
		self.ui.distanceSizeSpin.setValue(self.settings.sketcherData.distanceRadius)
		self.ui.showgridCheckBox.setChecked(self.settings.sketcherData.showGrid)
		self.ui.gridWidthSpin.setValue(self.settings.sketcherData.gridWidth)
		self.ui.gridHeightSpin.setValue(self.settings.sketcherData.gridHeight)
		
	def createTriggers(self):
		QtCore.QObject.connect(self.ui.showgridCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.showGrid)
		QtCore.QObject.connect(self.ui.pointSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updatePointSize)
		QtCore.QObject.connect(self.ui.fPointSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateFPointSize)
		QtCore.QObject.connect(self.ui.lineSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateLineSize)
		QtCore.QObject.connect(self.ui.distanceSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateDistanceSize)
		QtCore.QObject.connect(self.ui.gridWidthSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateGridWidth)
		QtCore.QObject.connect(self.ui.gridHeightSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateGridHeight)
		
		QtCore.QObject.connect(self.ui.fPointClrButton,QtCore.SIGNAL("clicked()"), self.setFPointColor)
		QtCore.QObject.connect(self.ui.dConstraintClrButton,QtCore.SIGNAL("clicked()"), self.setDistanceColor)
		QtCore.QObject.connect(self.ui.angleClrButton,QtCore.SIGNAL("clicked()"), self.setAngleColor)
		QtCore.QObject.connect(self.ui.selectClrButton,QtCore.SIGNAL("clicked()"), self.setSelectionColor)
		QtCore.QObject.connect(self.ui.distanceClrButton,QtCore.SIGNAL("clicked()"), self.setLineColor)
		QtCore.QObject.connect(self.ui.bgClrButton,QtCore.SIGNAL("clicked()"), self.setBackgroundColor)
		QtCore.QObject.connect(self.ui.pointClrButton,QtCore.SIGNAL("clicked()"), self.setPointColor)
		
	def showGrid(self, state):			
		if state == QtCore.Qt.Unchecked:
			self.settings.sketcherData.showGrid = False
		else:
			self.settings.sketcherData.showGrid = True
		self.settings.sketcherData.emit(QtCore.SIGNAL("showGridChanged"), self.settings.sketcherData.showGrid)
	
	def updatePointSize(self, size):
		self.settings.sketcherData.pointRadius = size
		self.settings.sketcherData.emit(QtCore.SIGNAL("pointSizeChanged"), size)
		
	def updateFPointSize(self, size):
		self.settings.sketcherData.fPointRadius = size
		self.settings.sketcherData.emit(QtCore.SIGNAL("fPointSizeChanged"), size)
		
	def updateLineSize(self, size):
		self.settings.sketcherData.lineRadius = size
		self.settings.sketcherData.emit(QtCore.SIGNAL("lineSizeChanged"), size)
		
	def updateDistanceSize(self, size):
		self.settings.sketcherData.distanceRadius = size
		self.settings.sketcherData.emit(QtCore.SIGNAL("distanceSizeChanged"), size)
		
	def updateGridWidth(self, width):
		self.settings.sketcherData.gridWidth= width
		self.settings.sketcherData.emit(QtCore.SIGNAL("gridWidthChanged"), width)
		
	def updateGridHeight(self, height):
		self.settings.sketcherData.gridHeight = height
		self.settings.sketcherData.emit(QtCore.SIGNAL("gridHeightChanged"), height)
		
	def setPointColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.pointColor)
		if color.isValid():
			self.settings.sketcherData.pointColor = color
			self.updateIconColor(self.pointIcon, self.ui.pointClrButton, color)
			self.settings.sketcherData.emit(QtCore.SIGNAL("pointColorChanged"), color)
			
	def setFPointColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.fPointColor)
		if color.isValid():
			self.settings.sketcherData.fPointColor = color
			self.updateIconColor(self.fPointIcon, self.ui.fPointClrButton, color)
			self.settings.sketcherData.emit(QtCore.SIGNAL("fPointColorChanged"), color)
			
	def setLineColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.lineColor)
		if color.isValid():
			self.settings.sketcherData.lineColor = color
			self.updateIconColor(self.distanceIcon, self.ui.distanceClrButton, color)
			self.settings.sketcherData.emit(QtCore.SIGNAL("lineColorChanged"), color)
			
	def setAngleColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.angleColor)
		if color.isValid():
			self.settings.sketcherData.angleColor = color
			self.updateIconColor(self.angleIcon, self.ui.angleClrButton, color)
			self.settings.sketcherData.emit(QtCore.SIGNAL("angleColorChanged"), color)
			
	def setSelectionColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.selectColor)
		if color.isValid():
			self.settings.sketcherData.selectColor = color
			self.updateIconColor(self.selectionIcon, self.ui.selectClrButton, color)
			self.settings.sketcherData.emit(QtCore.SIGNAL("selectionColorChanged"), color)
			
	def setDistanceColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.distanceColor)
		if color.isValid():
			self.settings.sketcherData.distanceColor = color
			self.updateIconColor(self.dConstraintIcon, self.ui.dConstraintClrButton, color)
			self.settings.sketcherData.emit(QtCore.SIGNAL("distanceColorChanged"), color)
			
	def setBackgroundColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.bgColor)
		if color.isValid():
			self.settings.sketcherData.bgColor = color
			self.updateIconColor(self.backgroundIcon, self.ui.bgClrButton, color)
			self.settings.sketcherData.emit(QtCore.SIGNAL("backgroundColorChanged"), color)
			
class ViewsPreferences(Preferences):
	def __init__(self, preferenceHandler):	
		Preferences.__init__(self, preferenceHandler)
		self.ui = Ui_viewsForm()
		self.ui.setupUi(self.widget)
		self.name = "Views" 
		self.preferenceHandler.addPreferencePage(self.name, self.widget)
		self.decViewPref = DecompositionViewPreferences(self.ui, self.settings)
		self.solViewPref = SolutionViewPreferences(self, self.ui, self.settings)

class DecompositionViewPreferences:
	def __init__(self, ui, settings):
		self.ui = ui
		self.settings = settings
		
	 	self.initSettings()
		self.createTriggers()
		
	def initSettings(self):
		if self.settings.dvData.treeConnection ==  ConnectionType.BEZIER:
			self.ui.radioCurvedButton.setChecked(True)
		elif self.settings.dvData.treeConnection ==  ConnectionType.LINES:
			self.ui.radioConnectionButton.setChecked(True)
		
		if self.settings.dvData.treeAlignment == TreeOrientation.TOP:
			self.ui.alignTreeComboBox.setCurrentIndex(self.ui.alignTreeComboBox.findText("Top"))
		elif self.settings.dvData.treeAlignment == TreeOrientation.BOTTOM:
			self.ui.alignTreeComboBox.setCurrentIndex(self.ui.alignTreeComboBox.findText("Bottom"))
		elif self.settings.dvData.treeAlignment == TreeOrientation.RIGHT:
			self.ui.alignTreeComboBox.setCurrentIndex(self.ui.alignTreeComboBox.findText("Right"))
		elif self.settings.dvData.treeAlignment == TreeOrientation.LEFT:
			self.ui.alignTreeComboBox.setCurrentIndex(self.ui.alignTreeComboBox.findText("Left"))
	
	def createTriggers(self):
		QtCore.QObject.connect(self.ui.radioCurvedButton,QtCore.SIGNAL("toggled(bool)"), self.curvedConnectionChanged)
		QtCore.QObject.connect(self.ui.radioConnectionButton,QtCore.SIGNAL("toggled(bool)"), self.lineConnectionChanged)
		QtCore.QObject.connect(self.ui.alignTreeComboBox,QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.treeAlignmentChanged)
	
	def lineConnectionChanged(self, state):
		if state:
			self.settings.dvData.treeConnection = ConnectionType.LINES

	def curvedConnectionChanged(self, state):
		if state:
			self.settings.dvData.treeConnection = ConnectionType.BEZIER
	
	def treeAlignmentChanged(self, alignment):
		if alignment == "Top": 
			self.settings.dvData.treeAlignment = TreeOrientation.TOP
		elif alignment == "Bottom":
			self.settings.dvData.treeAlignment = TreeOrientation.BOTTOM
		elif alignment == "Right":
			self.settings.dvData.treeAlignment = TreeOrientation.RIGHT
		elif alignment == "Left":
			self.settings.dvData.treeAlignment = TreeOrientation.LEFT
		self.settings.dvData.emit(QtCore.SIGNAL("treeOrientationChanged()"))	

class SolutionViewPreferences:
	def __init__(self, preferences, ui, settings):
		self.ui = ui
		self.settings = settings		
		self.preferences = preferences
		self.initSettings()
		self.createTriggers()
	
	def initSettings(self):
		self.fPointIcon = QtGui.QPixmap(40,20)
		self.dConstraintIcon = QtGui.QPixmap(40,20)
		self.angleIcon = QtGui.QPixmap(40,20)
		self.distanceIcon = QtGui.QPixmap(40,20)
		self.backgroundIcon = QtGui.QPixmap(40,20)
		self.pointIcon = QtGui.QPixmap(40,20)
		self.setIcons()
		self.setValues()
	
	def setIcons(self):
		self.fPointIcon.fill(self.settings.svData.fPointColor)
		self.ui.svfPointClrButton.setIcon(QtGui.QIcon(self.fPointIcon))
		self.dConstraintIcon.fill(self.settings.svData.distanceColor)
		self.ui.svdConstraintClrButton.setIcon(QtGui.QIcon(self.dConstraintIcon))
		self.angleIcon.fill(self.settings.svData.angleColor)
		self.ui.svAngleClrButton.setIcon(QtGui.QIcon(self.angleIcon))
		self.distanceIcon.fill(self.settings.svData.lineColor)
		self.ui.svDistanceClrButton.setIcon(QtGui.QIcon(self.distanceIcon))
		self.backgroundIcon.fill(self.settings.svData.bgColor)
		self.ui.svBgClrButton.setIcon(QtGui.QIcon(self.backgroundIcon))
		self.pointIcon.fill(self.settings.svData.pointColor)
		self.ui.svPointClrButton.setIcon(QtGui.QIcon(self.pointIcon))

	def setValues(self):
		self.ui.svPointSizeSpin.setValue(self.settings.svData.pointRadius)
		self.ui.svfPointSizeSpin.setValue(self.settings.svData.fPointRadius)
		self.ui.svLineSizeSpin.setValue(self.settings.svData.lineRadius)
		self.ui.svDistanceSizeSpin.setValue(self.settings.svData.distanceRadius)
		self.ui.svShowgrid.setChecked(self.settings.svData.showGrid)
		self.ui.svGridWidthSpin.setValue(self.settings.svData.gridWidth)
		self.ui.svGridHeightSpin.setValue(self.settings.svData.gridHeight)
		
		self.ui.vPoint.setChecked(self.settings.svData.pointVisible)		
		self.ui.vAngle.setChecked(self.settings.svData.angleVisible)
		self.ui.vfPoint.setChecked(self.settings.svData.fPointVisible)
		self.ui.vLine.setChecked(self.settings.svData.lineVisible)
		self.ui.vDistance.setChecked(self.settings.svData.distanceVisible)
	
	def createTriggers(self):
		QtCore.QObject.connect(self.ui.svShowgrid, QtCore.SIGNAL("stateChanged(int)"), self.showGrid)
		QtCore.QObject.connect(self.ui.svPointSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updatePointSize)
		QtCore.QObject.connect(self.ui.svfPointSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateFPointSize)
		QtCore.QObject.connect(self.ui.svLineSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateLineSize)
		QtCore.QObject.connect(self.ui.svDistanceSizeSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateDistanceSize)
		QtCore.QObject.connect(self.ui.svGridWidthSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateGridWidth)
		QtCore.QObject.connect(self.ui.svGridHeightSpin, QtCore.SIGNAL("valueChanged(int)"), self.updateGridHeight)
		
		QtCore.QObject.connect(self.ui.svfPointClrButton,QtCore.SIGNAL("clicked()"), self.setFPointColor)
		QtCore.QObject.connect(self.ui.svdConstraintClrButton,QtCore.SIGNAL("clicked()"), self.setDistanceColor)
		QtCore.QObject.connect(self.ui.svAngleClrButton,QtCore.SIGNAL("clicked()"), self.setAngleColor)
		QtCore.QObject.connect(self.ui.svDistanceClrButton,QtCore.SIGNAL("clicked()"), self.setLineColor)
		QtCore.QObject.connect(self.ui.svBgClrButton,QtCore.SIGNAL("clicked()"), self.setBackgroundColor)
		QtCore.QObject.connect(self.ui.svPointClrButton,QtCore.SIGNAL("clicked()"), self.setPointColor)

		QtCore.QObject.connect(self.ui.vPoint,QtCore.SIGNAL("stateChanged(int)"), self.setPointVisibility)
		QtCore.QObject.connect(self.ui.vAngle,QtCore.SIGNAL("stateChanged(int)"), self.setAngleVisibility)
		QtCore.QObject.connect(self.ui.vfPoint,QtCore.SIGNAL("stateChanged(int)"), self.setFixedPointVisibility)
		QtCore.QObject.connect(self.ui.vDistance,QtCore.SIGNAL("stateChanged(int)"), self.setDistanceVisibility)
		QtCore.QObject.connect(self.ui.vLine,QtCore.SIGNAL("stateChanged(int)"), self.setLineVisibility)
	
	def showGrid(self, state):
		if state == QtCore.Qt.Unchecked:
			self.settings.svData.showGrid = False
		else:
			self.settings.svData.showGrid = True
		self.settings.svData.emit(QtCore.SIGNAL("showGridChanged"), self.settings.svData.showGrid)
	
	def updatePointSize(self, size):
		self.settings.svData.pointRadius = size
		self.settings.svData.emit(QtCore.SIGNAL("pointSizeChanged"), size)
		
	def updateFPointSize(self, size):
		self.settings.svData.fPointRadius = size
		self.settings.svData.emit(QtCore.SIGNAL("fPointSizeChanged"), size)
		
	def updateLineSize(self, size):
		self.settings.svData.lineRadius = size
		self.settings.svData.emit(QtCore.SIGNAL("lineSizeChanged"), size)
		
	def updateDistanceSize(self, size):
		self.settings.svData.distanceRadius = size
		self.settings.svData.emit(QtCore.SIGNAL("distanceSizeChanged"), size)
		
	def updateGridWidth(self, width):
		self.settings.svData.gridWidth= width
		self.settings.svData.emit(QtCore.SIGNAL("gridWidthChanged"), width)
		
	def updateGridHeight(self, height):
		self.settings.svData.gridHeight = height
		self.settings.svData.emit(QtCore.SIGNAL("gridHeightChanged"), height)
		
	def setPointColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.svData.pointColor)
		if color.isValid():
			self.settings.svData.pointColor = color
			self.preferences.updateIconColor(self.pointIcon, self.ui.svPointClrButton, color)
			self.settings.svData.emit(QtCore.SIGNAL("pointColorChanged"), color)
			
	def setFPointColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.svData.fPointColor)
		if color.isValid():
			self.settings.svData.fPointColor = color
			self.preferences.updateIconColor(self.fPointIcon, self.ui.svfPointClrButton, color)
			self.settings.svData.emit(QtCore.SIGNAL("fPointColorChanged"), color)
			
	def setLineColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.svData.lineColor)
		if color.isValid():
			self.settings.svData.lineColor = color
			self.preferences.updateIconColor(self.distanceIcon, self.ui.svDistanceClrButton, color)
			self.settings.svData.emit(QtCore.SIGNAL("lineColorChanged"), color)
			
	def setAngleColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.sketcherData.angleColor)
		if color.isValid():
			self.settings.svData.angleColor = color
			self.preferences.updateIconColor(self.angleIcon, self.ui.svAngleClrButton, color)
			self.settings.svData.emit(QtCore.SIGNAL("angleColorChanged"), color)
					
	def setDistanceColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.svData.distanceColor)
		if color.isValid():
			self.settings.svData.distanceColor = color
			self.preferences.updateIconColor(self.dConstraintIcon, self.ui.svdConstraintClrButton, color)
			self.settings.svData.emit(QtCore.SIGNAL("distanceColorChanged"), color)
			
	def setBackgroundColor(self):
		color = QtGui.QColorDialog.getColor(self.settings.svData.bgColor)
		if color.isValid():
			self.settings.svData.bgColor = color
			self.preferences.updateIconColor(self.backgroundIcon, self.ui.svBgClrButton, color)
			self.settings.svData.emit(QtCore.SIGNAL("backgroundColorChanged"), color)

	def setPointVisibility(self, state):			
		if state == QtCore.Qt.Unchecked:
			self.settings.svData.pointVisible = False
		else:
			self.settings.svData.pointVisible = True
		self.settings.svData.emit(QtCore.SIGNAL("pointVisChanged"), self.settings.svData.pointVisible)
	
	def setAngleVisibility(self, state):			
		if state == QtCore.Qt.Unchecked:
			self.settings.svData.angleVisible = False
		else:
			self.settings.svData.angleVisible = True
		self.settings.svData.emit(QtCore.SIGNAL("angleVisChanged"), self.settings.svData.angleVisible)
	
	def setFixedPointVisibility(self, state):			
		if state == QtCore.Qt.Unchecked:
			self.settings.svData.fPointVisible = False
		else:
			self.settings.svData.fPointVisible = True
		self.settings.svData.emit(QtCore.SIGNAL("fpointVisChanged"), self.settings.svData.fPointVisible)

	def setDistanceVisibility(self, state):			
		if state == QtCore.Qt.Unchecked:
			self.settings.svData.distanceVisible = False
		else:
			self.settings.svData.distanceVisible = True
		self.settings.svData.emit(QtCore.SIGNAL("distanceVisChanged"), self.settings.svData.distanceVisible)

	def setLineVisibility(self, state):			
		if state == QtCore.Qt.Unchecked:
			self.settings.svData.lineVisible = False
		else:
			self.settings.svData.lineVisible = True
		self.settings.svData.emit(QtCore.SIGNAL("lineVisChanged"), self.settings.svData.lineVisible)
	
class PreferencesDlg(QtGui.QDialog):
	def __init__(self, viewportMngr, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.viewportManager = viewportMngr
		self.settings = Settings()
		self.ui = Ui_preferencesDialog()
		self.ui.setupUi(self)
		self.ui.contentsWidget.clear()
		self.preferencePages = []
		self.initPreferences()
		
		QtCore.QObject.connect(self.ui.contentsWidget,QtCore.SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"),self.changePage)
		QtCore.QObject.connect(self.ui.closeButton, QtCore.SIGNAL("clicked()"), self.closeClicked)
		QtCore.QObject.connect(self, QtCore.SIGNAL("finished(int)"), self.closeClicked)
	
	def initPreferences(self):
		self.preferencePages += [SketcherPreferences(self)]
		self.preferencePages += [ViewsPreferences(self)]
				
	def changePage(self, current, previous):
		if not current:
			current = previous
		
		self.ui.pagesWidget.setCurrentIndex(self.ui.contentsWidget.row(current))
			
	def addPreferencePage(self, name, widget):
		self.ui.pagesWidget.addWidget(widget)
		item = QtGui.QListWidgetItem(self.ui.contentsWidget)
		item.setText(QtGui.QApplication.translate("preferencesDialog", name, None, QtGui.QApplication.UnicodeUTF8))
		
	def closeClicked(self):
		self.settings.save()
		

		
	
