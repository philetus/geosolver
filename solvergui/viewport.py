from includes import *
from compositionView import CompositionView
from solutionView import SolutionView
from prototypeObjects import PrototypeManager
from glViewer import *

class Viewport(QtGui.QScrollArea):
	def __init__(self, viewportMngr, vpType=None, shareWidget=None, parent=None):
		QtGui.QScrollArea.__init__(self, parent)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
		
		self.moveActive = False
		self.zoomActive = False
		self.rotateActive = False
		self.name = ""		
		self.viewportManager = viewportMngr
		self.glViewport = None
		self.solutionView = None
		
		self.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken)
	
		#self.setFrameShape(QtGui.QFrame.StyledPanel)
		#self.setFrameShadow(QtGui.QFrame.Plain)
		self.setWidgetResizable(True)
		
		self.setViewport(vpType, shareWidget)
		self.createActions()
		self.createToolbar()
		self.createVerticalSplit()
		self.createTriggers()

	def setViewport(self,vpType, shareWidget=None):
		self.setName(vpType)
		self.glViewport = GLViewport(self, vpType, shareWidget, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))
		
	def setMoveActive(self, active):
		self.moveActive = active
		self.updateAction.execute(self.glViewport)
		self.glViewport.cameraHandler.setActiveMouseaction(MouseAction.TRANSLATE)

	def setZoomActive(self, active):
		self.zoomActive = active
		self.updateAction.execute(self.glViewport)
		self.glViewport.cameraHandler.setActiveMouseaction(MouseAction.ZOOM)

	def setRotateActive(self, active):
		self.rotateActive = active
		self.updateAction.execute(self.glViewport)
		self.glViewport.cameraHandler.setActiveMouseaction(MouseAction.ROTATE)
	

	def setGridVisibility(self, visibility=True):
		self.gridVisible = visibility

	def isMoveActive(self):
		return self.moveActive

	def isZoomActive(self):
		return self.zoomActive
	
	def isRotateActive(self):
		return self.rotateActive

	def isGridVisible(self):
		return self.gridVisible
	
	def isActive(self):
		if self.viewportManager.getActiveViewportType() == self:
			return True
		else:
			return False
	
	def doSync(self, active):
		if self.solutionView != None:
			self.solutionView.synchronise()
	
	def createActions(self):
		self.editGroup = QtGui.QActionGroup(self)
		self.editGroup.setExclusive(True)
		self.actionMove = QtGui.QAction(self.tr("Move"), self)
		self.actionMove.setCheckable(True)		
		self.actionZoom = QtGui.QAction(self.tr("Zoom"), self)
		self.actionZoom.setCheckable(True)
		self.actionRotate = QtGui.QAction(self.tr("Rotate"), self)
		self.actionRotate.setCheckable(True)
		self.actionSync = QtGui.QAction(self.tr("Sync"), self)
		self.editGroup.addAction(self.actionMove)
		self.editGroup.addAction(self.actionZoom)
		self.editGroup.addAction(self.actionRotate)
		self.editGroup.addAction(self.actionSync)
		if self.glViewport.getViewportType() != ViewportType.PERSPECTIVE:
			self.actionRotate.setVisible(False)
		if self.glViewport.getViewportType() != ViewportType.SOLUTION:
			self.actionSync.setVisible(False)

	def createToolbar(self):
		self.toolbar = QtGui.QToolBar(self)
		self.toolbar.setMaximumHeight(30)
		self.toolbar.addAction(self.actionMove)
		self.toolbar.addAction(self.actionZoom)
		self.toolbar.addAction(self.actionRotate)
		self.toolbar.addAction(self.actionSync)
		
		self.viewportList = QtGui.QComboBox()
		self.viewportList.addItem("Top")
		self.viewportList.addItem("Front")
		self.viewportList.addItem("Side")
		self.viewportList.addItem("Perspective")
		self.viewportList.addItem("Decomposition")
		self.viewportList.addItem("Solution")
		self.viewportList.setCurrentIndex(self.viewportList.findText(self.name))
		self.viewportList.setMinimumWidth(100)
		self.toolbar.addWidget(self.viewportList)
		self.updateAction = UpdateActionCommand(self.getMainWindow())
		
		
	def createVerticalSplit(self):
		self.splitterVertical = QtGui.QSplitter()
		self.splitterVertical.setHandleWidth(1)
		self.splitterVertical.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
		self.splitterVertical.setOrientation(QtCore.Qt.Vertical)
		self.splitterVertical.addWidget(self.toolbar)
		self.splitterVertical.addWidget(self.glViewport)
		self.setWidget(self.splitterVertical)
		self.toolbar.resize(200,1)
	
	def createTriggers(self):
		QtCore.QObject.connect(self.viewportList,QtCore.SIGNAL("currentIndexChanged(const QString &)"), self.changeViewport)
		QtCore.QObject.connect(self.actionMove, QtCore.SIGNAL("triggered(bool)"), self.setMoveActive)
		QtCore.QObject.connect(self.actionRotate, QtCore.SIGNAL("triggered(bool)"), self.setRotateActive)
		QtCore.QObject.connect(self.actionZoom, QtCore.SIGNAL("triggered(bool)"), self.setZoomActive)
		QtCore.QObject.connect(self.actionSync, QtCore.SIGNAL("triggered(bool)"), self.doSync)
	
	def keyPressEvent(self, keyEvent):
		self.glViewport.keyPressEvent(keyEvent)
	
	def keyReleaseEvent(self, keyEvent):
		self.glViewport.keyReleaseEvent(keyEvent)
	
	def changeViewport(self, viewportName):
		if self.name == viewportName:
			return
		else:
			tool = self.glViewport.currentTool
			self.glViewport.close()
					
			if viewportName == "Top":
				self.glViewport = GLViewport(self, ViewportType.TOP, None, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))
			elif viewportName == "Side":
				self.glViewport = GLViewport(self, ViewportType.SIDE, None, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))
			elif viewportName == "Front":
				self.glViewport = GLViewport(self, ViewportType.FRONT, None, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))
			elif viewportName == "Perspective":
				self.glViewport = GLViewport(self, ViewportType.PERSPECTIVE, None, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))
			elif viewportName == "Decomposition":
				self.glViewport = CompositionView(self,  self.viewportManager, ViewportType.DECOMPOSITION, PrototypeManager()) #self.getMainWindow().compositionView #
			elif viewportName == "Solution":
				self.solutionView = SolutionView(self.getMainWindow(), self.viewportManager,  ViewportType.SOLUTION, PrototypeManager(), True)
				self.glViewport = self.solutionView.solutionWidget
				
			
			self.setActions()				
			for action in self.editGroup.actions():
				action.setChecked(False)
			self.splitterVertical.addWidget(self.glViewport)
			self.setName(self.glViewport.viewportType)
			self.glViewport.currentTool = tool
		if self.glViewport.viewportType != ViewportType.DECOMPOSITION:
			self.glViewport.makeCurrent()

	def setActions(self):
		if self.glViewport.getViewportType() == ViewportType.PERSPECTIVE:
			self.actionMove.setVisible(True)
			self.actionZoom.setVisible(True)
			self.actionRotate.setVisible(True)
			self.actionSync.setVisible(False)
		elif self.glViewport.getViewportType() == ViewportType.SOLUTION:
			self.actionMove.setVisible(True)
			self.actionZoom.setVisible(True)
			self.actionRotate.setVisible(True)
			self.actionSync.setVisible(True)
		elif self.glViewport.getViewportType() == ViewportType.DECOMPOSITION:
			self.actionMove.setVisible(False)
			self.actionZoom.setVisible(False)
			self.actionRotate.setVisible(False)
			self.actionSync.setVisible(False)
		else:
			self.actionMove.setVisible(True)
			self.actionZoom.setVisible(True)
			self.actionRotate.setVisible(False)
			self.actionSync.setVisible(False)
			

	def setName(self, vpType):
		if vpType == ViewportType.TOP:
			self.name = "Top"
		elif vpType == ViewportType.SIDE:
			self.name = "Side"
		elif vpType == ViewportType.FRONT:
			self.name = "Front"
		elif vpType == ViewportType.PERSPECTIVE:
			self.name = "Perspective"
		elif vpType == ViewportType.DECOMPOSITION:
			self.name = "Decomposition"
		elif vpType == ViewportType.SOLUTION:
			self.name = "Solution"

	def getMainWindow(self):
		return self.viewportManager.getMainWindow()
	
	def updateViewports(self):
		self.viewportManager.updateViewports()
	
	def resetViewport(self):
		self.glViewport.setCameraView()
		
	def mousePressEvent(self, mouseEvent):
		self.viewportManager.activeViewport = self
