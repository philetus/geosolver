from includes import *
from glViewer import *
from ui_solutionView import Ui_SolutionView
from parameters import Settings

class SolutionView(QtGui.QDialog):
	""" Visualises the solution from the constraint solver. """ 
	def __init__(self, mainWindow, viewportMngr, vpType, prototypeMngr, isViewport=False, parent=None):
		""" Initialization of the CompositionView class
			
		Parameters:
			mainWindow - main window of the application, necessary for updating
			viewportMngr - the manager of the viewports where the composition view can reside in
			vpType - type of this view
			prototypeMngr - the manager of the prototypes is used to obtain the results of the solver
			parent - parent of this dialog
		"""
		QtGui.QDialog.__init__(self, parent)
		self.mainWindow = mainWindow
		self.prototypeManager = prototypeMngr
		self.viewportManager = viewportMngr
		self.setWindowFlags(QtCore.Qt.Window)
		self.ui = Ui_SolutionView()
		self.ui.setupUi(self)
		self.settings = Settings()

		self.solutionWidget = SolutionGLViewport(self, ViewportType.SOLUTION, None, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), self)
		self.solutionWidget.gridVisible = False
		self.ui.vboxlayout.addWidget(self.solutionWidget, 200)
		
		self.updateAction = UpdateActionCommand(self.getMainWindow())
		self.isViewport = isViewport
		self.solutionObjects = []
		
		if not self.isViewport:
			self.moveActive = False
			self.zoomActive = False
			self.rotateActive = False
			self.createTriggers()
		else:
			self.removeInterfaceItems()
			
		self.createSolution()
	
	def createTriggers(self):
		""" Triggers for the buttons in the Solution View """
		QtCore.QObject.connect(self.ui.moveButton, QtCore.SIGNAL("clicked(bool)"), self.setMoveActive)
		QtCore.QObject.connect(self.ui.rotateButton, QtCore.SIGNAL("clicked(bool)"), self.setRotateActive)
		QtCore.QObject.connect(self.ui.zoomButton, QtCore.SIGNAL("clicked(bool)"), self.setZoomActive)
		QtCore.QObject.connect(self.ui.syncButton, QtCore.SIGNAL("clicked(bool)"), self.synchronise)
		
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("pointSizeChanged"), self.updateSize)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("fPointSizeChanged"), self.updateSize)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("lineSizeChanged"), self.updateSize)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("distanceSizeChanged"), self.updateSize)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("pointColorChanged"), self.updateColor)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("fPointColorChanged"), self.updateColor)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("lineColorChanged"), self.updateColor)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("angleColorChanged"), self.updateColor)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("selectionColorChanged"), self.updateColor)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("distanceColorChanged"), self.updateColor)

		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("pointVisChanged"), self.updateVisibility)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("fpointVisChanged"), self.updateVisibility)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("lineVisChanged"), self.updateVisibility)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("angleVisChanged"), self.updateVisibility)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("distanceVisChanged"), self.updateVisibility)		

	def removeInterfaceItems(self):
		""" Removes the standard interface buttons to control the camera etc. """
		self.ui.moveButton.hide()
		self.ui.rotateButton.hide()
		self.ui.zoomButton.hide()
		self.ui.vboxlayout.removeItem(self.ui.hboxlayout)
	
	def setMoveActive(self, active):
		""" Set the move button as active button and inform the camera the translation action is active
		
		Paramaters:
			active - set the state of the camera, in this case for translation
		"""
		self.moveActive = active
		self.updateAction.execute(self.solutionWidget)
		self.solutionWidget.cameraHandler.setActiveMouseaction(MouseAction.TRANSLATE)

	def setZoomActive(self, active):
		""" Set the zoom button as active button and inform the camera the zoom action is active
		
		Paramaters:
			active - set the state of the camera, in this case for zooming
		"""
		self.zoomActive = active
		self.updateAction.execute(self.solutionWidget)
		self.solutionWidget.cameraHandler.setActiveMouseaction(MouseAction.ZOOM)

	def setRotateActive(self, active):
		""" Set the rotation button as active button and inform the camera the rotation action is active
		
		Paramaters:
			active - set the state of the camera, in this case for rotation
		"""
		self.rotateActive = active
		self.updateAction.execute(self.solutionWidget)
		self.solutionWidget.cameraHandler.setActiveMouseaction(MouseAction.ROTATE)

	def updateSize(self):
		for solObject in self.solutionObjects:
			if solObject.objType == ObjectType.POINT:
				solObject.radius = self.settings.svData.pointRadius
			elif solObject.objType == ObjectType.FIXED_POINT:
				solObject.radius = self.settings.svData.fPointRadius
			elif solObject.objType == ObjectType.DISTANCE_HELPER:
				solObject.radius = self.settings.svData.lineRadius
			elif solObject.objType == ObjectType.DISTANCE_CONSTRAINT:
				solObject.radius = self.settings.svData.distanceRadius
				
	def updateColor(self):
		for solObject in self.solutionObjects:
			if solObject.objType == ObjectType.POINT:
				solObject.color = self.settings.svData.pointColor
			elif solObject.objType == ObjectType.FIXED_POINT:
				solObject.color = self.settings.svData.fPointColor
			elif solObject.objType == ObjectType.DISTANCE_HELPER:
				solObject.color = self.settings.svData.lineColor
			elif solObject.objType == ObjectType.DISTANCE_CONSTRAINT:
				solObject.color = self.settings.svData.distanceColor
			elif solObject.objType == ObjectType.ANGLE_CONSTRAINT:
				solObject.color = self.settings.svData.angleColor

	def updateVisibility(self):
		for solObject in self.solutionObjects:
			if solObject.objType == ObjectType.POINT:
				solObject.isVisible = self.settings.svData.pointVisible
			elif solObject.objType == ObjectType.FIXED_POINT:
				solObject.isVisible = self.settings.svData.fPointVisible
			elif solObject.objType == ObjectType.DISTANCE_HELPER:
				solObject.isVisible = self.settings.svData.lineVisible
			elif solObject.objType == ObjectType.DISTANCE_CONSTRAINT:
				solObject.isVisible = self.settings.svData.distanceVisible
			elif solObject.objType == ObjectType.ANGLE_CONSTRAINT:
				solObject.isVisible = self.settings.svData.angleVisible

	def updateViewports(self):
		""" Update the general viewports """
		self.viewportManager.updateViewports()
	
	def isActive(self):
		if self.viewportManager.getActiveViewportType() == self:
			return True
		else:
			return False
		
	def getMainWindow(self):
		""" Return the main window object """
		return self.mainWindow
	
	def createSolution(self):
		""" Create objects for visualisation in the solution view, this action will typically take place, when the system of GCS is solved """
		del self.solutionObjects[:]
		if self.prototypeManager.result != None:
			if len(self.prototypeManager.result.solutions) > 0:
				solution = self.prototypeManager.result.solutions[0]
				for variable in self.prototypeManager.result.variables:
					self.solutionObjects += [Point(variable, Vec(solution[variable]), 5.0)]
				
				self.createDistanceConstraints()
				self.createAngleConstraints()
				self.createDistances()
		self.solutionWidget.update()
	
	def createDistanceConstraints(self):
		""" Create the distance constraints as visualisation between the nodes """	
		distances = filter(lambda c: isinstance(c, geosolver.DistanceConstraint), self.prototypeManager.geoProblem.cg.constraints())		
		for distance in distances:
			beginPoint = self.getSolutionPointByKey(distance._variables[0])
			endPoint = self.getSolutionPointByKey(distance._variables[1])
			distanceConstr = DistanceConstraint("", beginPoint, endPoint)
			distanceConstr.height = distance._value
			distanceConstr.update()
			self.solutionObjects += [distanceConstr]	
	
	def createAngleConstraints(self):
		angles = filter(lambda c: isinstance(c, geosolver.AngleConstraint), self.prototypeManager.geoProblem.cg.constraints())		
		for angle in angles:
			beginPoint = self.getSolutionPointByKey(angle._variables[0])
			middlePoint = self.getSolutionPointByKey(angle._variables[1])
			endPoint = self.getSolutionPointByKey(angle._variables[2])
			angleConstr = AngleConstraint("", beginPoint, middlePoint, endPoint)
			angleConstr.realAngle = angle._value
			angleConstr.update()
			self.solutionObjects += [angleConstr]			
	
	def createDistances(self):
		distances = filter(lambda x:x.objType==ObjectType.DISTANCE_HELPER, self.prototypeManager.prtObjects)
		for distance in distances:
			solPointBegin = filter(lambda x:x.key == distance.pointBegin.key and x.objType==ObjectType.POINT, self.solutionObjects)
			solPointEnd = filter(lambda x:x.key == distance.pointEnd.key and x.objType==ObjectType.POINT, self.solutionObjects)
			solDistance = Distance("", solPointBegin[0], solPointEnd[0])
			solDistance.update()
			self.solutionObjects += [solDistance]
	
	def synchronise(self):
		if self.prototypeManager.result != None:
			prtPoints = filter(lambda x:x.objType == ObjectType.POINT, self.prototypeManager.prtObjects)
			solPoints = filter(lambda x:x.objType == ObjectType.POINT, self.solutionObjects)
			for prtPoint in prtPoints:
				for solPoint in solPoints:
					if prtPoint.key == solPoint.key:
						prtPoint.setPosition(solPoint.position)
			self.prototypeManager.updateObjects()
			self.updateViewports()
					
	def getSolutionPointByKey(self, variable):
		""" Get the first point from the solution by a variable 
		
		Parameters:
			variable - variable which identifies the point which needs to be obtained
		
		Return:
			point - point from the solution object list
		"""	
		point = filter(lambda p: p.key == variable, self.solutionObjects)
		if point != None:
			return point[0]
				
	def drawObjects(self):
		""" Draw the objects in the Solution View """
		for solObj in self.solutionObjects:
			if solObj.isVisible:
				solObj.draw()	
	
