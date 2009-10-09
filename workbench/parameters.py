from includes import *
from constants import *
from singleton import *

class Settings (Singleton):
	def __init__(self):
		Singleton.__init__( self )
		if self._isNew:
			self.sketcherData = SketcherData()
			self.dvData = DecompositionViewData()
			self.svData = SolutionViewData()
			self.load()
			
	def load(self):
		self.settings = QtCore.QSettings("TUDelft", "Geometric Constraint Solver")
		if len(self.settings.allKeys()) > 0:
			self.sketcherData.load(self.settings)
			self.dvData.load(self.settings)
		
	def save(self):
		self.settings = QtCore.QSettings("TUDelft", "Geometric Constraint Solver")
		self.sketcherData.save(self.settings)
		self.dvData.save(self.settings)
			
class SketcherData(QtCore.QObject):
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.selectColor = QtGui.QColor(255.0, 255.0, 0.0)
		self.pointColor =  QtGui.QColor(33, 163, 125) #[0.13, 0.64, 0.49]
		self.lineColor = QtGui.QColor(0.0, 0.0, 255.0)
		self.fPointColor = QtGui.QColor(0.0, 255.0, 0.0)
		self.distanceColor = QtGui.QColor(0.0, 255.0, 255.0)
		self.angleColor = QtGui.QColor(255.0, 0.0, 0.0, 123)
		self.bgColor = QtGui.QColor(210,210,210)
		
		self.pointRadius = 5
		self.lineRadius = 2
		self.fPointRadius = 5
		self.distanceRadius = 2
		
		self.showGrid = True
		self.gridWidth = 50
		self.gridHeight = 50
	
	def save(self, settings):
		settings.beginGroup("sketcher")
		settings.setValue("selectColor", QtCore.QVariant(self.selectColor))
		settings.setValue("pointColor", QtCore.QVariant(self.pointColor))
		settings.setValue("lineColor", QtCore.QVariant(self.lineColor))
		settings.setValue("fixedPointColor", QtCore.QVariant(self.fPointColor))
		settings.setValue("distanceColor", QtCore.QVariant(self.distanceColor))
		settings.setValue("angleColor", QtCore.QVariant(self.angleColor))
		settings.setValue("backgroundColor", QtCore.QVariant(self.bgColor))
		
		settings.setValue("pointRadius", QtCore.QVariant(self.pointRadius))
		settings.setValue("lineRadius", QtCore.QVariant(self.lineRadius))
		settings.setValue("fixedPointRadius", QtCore.QVariant(self.fPointRadius))
		settings.setValue("distanceRadius", QtCore.QVariant(self.distanceRadius))
		settings.setValue("showGrid", QtCore.QVariant(self.showGrid))
		settings.setValue("gridWidth", QtCore.QVariant(self.gridWidth))
		settings.setValue("gridHeight", QtCore.QVariant(self.gridHeight))
		settings.endGroup()
	
	def load(self, settings):
		settings.beginGroup("sketcher")
		
		self.selectColor = QtGui.QColor(settings.value("selectColor"))
		self.pointColor = QtGui.QColor(settings.value("pointColor"))
		self.lineColor = QtGui.QColor(settings.value("lineColor"))
		self.fPointColor = QtGui.QColor(settings.value("fixedPointColor"))
		self.distanceColor = QtGui.QColor(settings.value("distanceColor"))
		self.angleColor = QtGui.QColor(settings.value("angleColor"))
		self.bgColor = QtGui.QColor(settings.value("backgroundColor"))
		
		self.pointRadius = settings.value("pointRadius").toInt()[0]
		self.lineRadius = settings.value("lineRadius").toInt()[0]
		self.fPointRadius = settings.value("fixedPointRadius").toInt()[0]
		self.distanceRadius = settings.value("distanceRadius").toInt()[0]
		self.showGrid = settings.value("showGrid").toBool();
		self.gridWidth = settings.value("gridWidth").toInt()[0]
		self.gridHeight = settings.value("gridHeight").toInt()[0]
		settings.endGroup()
		
class DecompositionViewData(QtCore.QObject):
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.treeAlignment = TreeOrientation.TOP
		self.treeConnection = ConnectionType.BEZIER
		self.fixedClusterIds = []
	
	def save(self, settings):
		settings.beginGroup("decompositionview")
		settings.setValue("treeAlignment", QtCore.QVariant(self.treeAlignment))
		settings.setValue("treeConnection", QtCore.QVariant(self.treeConnection))
		settings.endGroup()
	
	def load(self, settings):
		settings.beginGroup("decompositionview")
		self.treeAlignment = settings.value("treeAlignment").toInt()[0]
		self.treeConnection = settings.value("treeConnection").toInt()[0]
		settings.endGroup()

class SolutionViewData(QtCore.QObject):
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.pointColor =  QtGui.QColor(33, 163, 125) #[0.13, 0.64, 0.49]
		self.lineColor = QtGui.QColor(0.0, 0.0, 255.0)
		self.fPointColor = QtGui.QColor(0.0, 255.0, 0.0)
		self.distanceColor = QtGui.QColor(0.0, 255.0, 255.0)
		self.angleColor = QtGui.QColor(255.0, 0.0, 0.0, 123)
		self.bgColor = QtGui.QColor(210,210,210)
		
		self.pointRadius = 5
		self.lineRadius = 2
		self.fPointRadius = 5
		self.distanceRadius = 2

		self.pointVisible = True
		self.lineVisible = True
		self.fPointVisible = True
		self.distanceVisible = True
		self.angleVisible = True
		
		self.showGrid = True
		self.gridWidth = 50
		self.gridHeight = 50
	
	def save(self, settings):
		settings.beginGroup("sketcher")
		settings.setValue("pointColor", QtCore.QVariant(self.pointColor))
		settings.setValue("lineColor", QtCore.QVariant(self.lineColor))
		settings.setValue("fixedPointColor", QtCore.QVariant(self.fPointColor))
		settings.setValue("distanceColor", QtCore.QVariant(self.distanceColor))
		settings.setValue("angleColor", QtCore.QVariant(self.angleColor))
		settings.setValue("backgroundColor", QtCore.QVariant(self.bgColor))
		
		settings.setValue("pointRadius", QtCore.QVariant(self.pointRadius))
		settings.setValue("lineRadius", QtCore.QVariant(self.lineRadius))
		settings.setValue("fixedPointRadius", QtCore.QVariant(self.fPointRadius))
		settings.setValue("distanceRadius", QtCore.QVariant(self.distanceRadius))
		settings.setValue("showGrid", QtCore.QVariant(self.showGrid))
		settings.setValue("gridWidth", QtCore.QVariant(self.gridWidth))
		settings.setValue("gridHeight", QtCore.QVariant(self.gridHeight))

		settings.setValue("pointVisible", QtCore.QVariant(self.pointVisible))
		settings.setValue("lineVisible", QtCore.QVariant(self.lineVisible))
		settings.setValue("fPointVisible", QtCore.QVariant(self.fPointVisible))
		settings.setValue("distanceVisible", QtCore.QVariant(self.distanceVisible))
		settings.setValue("angleVisible", QtCore.QVariant(self.angleVisible))
		settings.endGroup()
	
	def load(self, settings):
		settings.beginGroup("sketcher")
		
		self.selectColor = QtGui.QColor(settings.value("selectColor"))
		self.pointColor = QtGui.QColor(settings.value("pointColor"))
		self.lineColor = QtGui.QColor(settings.value("lineColor"))
		self.fPointColor = QtGui.QColor(settings.value("fixedPointColor"))
		self.distanceColor = QtGui.QColor(settings.value("distanceColor"))
		self.angleColor = QtGui.QColor(settings.value("angleColor"))
		self.bgColor = QtGui.QColor(settings.value("backgroundColor"))
		
		self.pointRadius = settings.value("pointRadius").toInt()[0]
		self.lineRadius = settings.value("lineRadius").toInt()[0]
		self.fPointRadius = settings.value("fixedPointRadius").toInt()[0]
		self.distanceRadius = settings.value("distanceRadius").toInt()[0]
		self.showGrid = settings.value("showGrid").toBool();
		self.gridWidth = settings.value("gridWidth").toInt()[0]
		self.gridHeight = settings.value("gridHeight").toInt()[0]

		self.pointVisible = settings.value("pointVisible").toBool();
		self.lineVisible = settings.value("lineVisible").toBool();
		self.fPointVisible = settings.value("fPointVisible").toBool();
		self.distanceVisible = settings.value("distanceVisible").toBool();
		self.angleVisible = settings.value("angleVisible").toBool();
		settings.endGroup()
	
