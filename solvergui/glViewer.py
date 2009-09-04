from includes import *
from camera import *
from cameraHandler import *
from prototypeObjects import *
from sceneObjects import *
from parameters import Settings
from geosolver.matfunc import Vec
import viewport

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except ImportError:
	app = QtGui.QApplication(sys.argv)
	QtGui.QMessageBox.critical(None, "OpenGL grabber","PyOpenGL must be installed to run this example.",
					QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)
	sys.exit(1)

class GLViewport(QtOpenGL.QGLWidget):
	def __init__(self, viewport, vpType, shareWidget=None, format=None, parent=None):
		QtOpenGL.QGLWidget.__init__(self, format, parent)
		self.gridColor = QtGui.QColor(190,190,190)
		#self.gridVisible = True
		self.viewport = viewport
		self.sceneObjects = SceneObject(self)
		self.setMouseTracking(True)
		self.windowWidth = 0
		self.windowHeight = 0
		self.zoomfactor = 1.0
		self.scaleAxis = 1.0
		self.viewportType = vpType
		self.camera = None
		self.cameraHandler = CameraHandler(self)
		self.selectionHandler = SelectionHandler()
		self.settings = Settings()
		self.bindings = {}
		self.bufferSize = 4000
		self.selectRegionWidth = 3
		self.selectRegionHeight = 3
		self.selectionRect = QtCore.QRect()
		self.selectedName = -1
		self.texture = None
		self.mousePosition = Vec([0.0, 0.0, 0.0])
		self.prtManager = PrototypeManager()
		self.currentTool = None
		self.updateStatusBar = UpdateTaskbarCommand(self, self.getMainWindow())
	
		if self.viewportType == ViewportType.PERSPECTIVE or self.viewportType == ViewportType.SOLUTION:
			self.camera = Camera(self, CameraType.PERSPECTIVE)
		else:
			self.camera = Camera(self, CameraType.ORTHOGRAPHIC)

		self.createTriggers()
		self.setCameraView()
		self.setBindings()
		
		
	def initializeGL(self):
		mat_specular = [0.1, 0.1, 0.1, 0.5]
		mat_emission = [0.0, 0.0, 0.0, 1.0]
		mat_shininess = [10.0]		
		light_position = [1.0, 1.0, 0.0, 0.0]
		light_position2 = [-100.0, -100.0, -100.0, 0.0]
		light_ambient = [0.2, 0.2, 0.2, 1.0]
		light_diffuse = [1.0, 1.0, 1.0, 1.0]
		
		glLightfv(GL_LIGHT0, GL_POSITION, light_position)
		glLightfv( GL_LIGHT0, GL_AMBIENT, light_ambient )
		glLightfv( GL_LIGHT0, GL_DIFFUSE, light_diffuse )
		glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE)
		glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
		glMaterialfv(GL_FRONT, GL_EMISSION, mat_emission)
		glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
		glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glShadeModel( GL_SMOOTH )		
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		glEnable(GL_NORMALIZE)
		glEnable(GL_COLOR_MATERIAL)
		#glEnable(GL_CULL_FACE)
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
			
		self.setBackgroundColor()
		#self.zoom(1.0)
	
	def createTriggers(self):
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("showGridChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("gridWidthChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("gridHeightChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("backgroundColorChanged"), self.setBackgroundColor)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("backgroundColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("pointSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("fPointSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("lineSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("distanceSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("pointColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("fPointColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("lineColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("angleColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("selectionColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("distanceColorChanged"), self.update)
			
	def paintGL(self):
		self.preDraw()
		self.draw()
		self.postDraw()
	
		glFlush()

	def preDraw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.camera.loadProjection()
		self.camera.loadModelView()
		self.showGrid()

	def showGrid(self):		
		if self.settings.sketcherData.showGrid:
			self.qglColor(QtGui.QColor(0.0, 0.0, 0.0)) 
			self.drawGrid()
				
	def draw(self):
		self.prtManager.drawObjects()

	def postDraw(self):
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		self.camera.loadModelView()
		
		glPushAttrib(GL_ALL_ATTRIB_BITS)
		glDisable(GL_COLOR_MATERIAL)
				
		self.startOverlay()
 		
 		self.drawViewportAxis()
		self.drawRotationHelper()
		if self.viewport.isActive():
			self.drawSelection()
		#self.sceneObjects.testDraw2()
		self.endOverlay()

		#glDisable(GL_LIGHTING)
		#self.drawText(100.0, 100.0, "GALLOEWTERGERGEG")
		glPopAttrib()
		glPopMatrix()

	def transparentDraw(self):
		self.prtManager.drawTransparentObjects()

	def resizeGL(self, newWidth, newHeight):
		glViewport( 0, 0, newWidth, newHeight)
		self.windowWidth = newWidth
		self.windowHeight = newHeight
		self.camera.setScreenWidthAndHeight(newWidth, newHeight)
					
	def setCameraView(self):
		if self.viewportType == ViewportType.TOP:
			self.camera.setPosition([0.0, 300.0, 0.0])
		elif self.viewportType == ViewportType.SIDE:
			self.camera.setPosition([300.0, 0.0, 0.0])
		elif self.viewportType == ViewportType.FRONT:
			self.camera.setPosition([0.0, 0.0, 300.0])
		elif self.viewportType == ViewportType.PERSPECTIVE:
			self.camera.setPosition([-200.0, 200.0, 300.0])
		elif self.viewportType == ViewportType.SOLUTION:
			self.camera.setPosition([-200.0, 200.0, 300.0])
		
		self.camera.lookAt(self.camera.getSceneCenter())
			
	def getViewportType(self):
		return self.viewportType

	def getCamera(self):
		return self.camera

	def startOverlay(self, upward=False):
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		
		if (upward):
			glOrtho(0, self.camera.getWindowWidth(), 0, self.camera.getWindowHeight(), 0.1, 100.0)
		else:
			glOrtho(0, self.camera.getWindowWidth(),self.camera.getWindowHeight(), 0.0, 0.1, 100.0)

		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glEnable(GL_COLOR_MATERIAL)
	
	def endOverlay(self):
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()

		glMatrixMode(GL_MODELVIEW)
		glPopMatrix()

	def drawGrid(self):
		if self.viewportType == ViewportType.PERSPECTIVE or self.viewportType == ViewportType.SOLUTION:
			self.sceneObjects.drawBackgroundgrid3D(600, 600, self.settings.sketcherData.gridWidth, self.settings.sketcherData.gridHeight, self.gridColor, False)
		else:
			self.sceneObjects.drawBackgroundgrid2D(self.settings.sketcherData.gridWidth, self.settings.sketcherData.gridHeight, self.gridColor, False)

	def drawSelection(self):
		if self.currentTool != None and self.currentTool.multipleSelect and self.currentTool.selectionStarted:
			self.sceneObjects.drawSelection(self.currentTool.beginSelPoint.x(), self.currentTool.beginSelPoint.y(), self.currentTool.endSelPoint.x(), self.currentTool.endSelPoint.y())
			"""glPushMatrix()
			glDisable(GL_LIGHTING)
			glRectf(self.currentTool.beginSelPoint.x(), self.currentTool.beginSelPoint.y(), self.currentTool.endSelPoint.x(), self.currentTool.endSelPoint.y())
			glEnable(GL_LIGHTING)
			glPopMatrix() """
	
	def drawViewportAxis(self):	
		glPushMatrix()	
		#glScalef(self.scaleAxis,self.scaleAxis,1.0)
		glTranslatef(20.0, self.camera.getWindowHeight()-40.0, -50.0)
		rotAxis = Vec([0.0,0.0,0.0])
		rotAngle = self.camera.getOrientation().getAxisAngle(self.camera.getOrientation(), rotAxis)
		glRotatef(rotAngle, rotAxis[0], -rotAxis[1], rotAxis[2])
		self.sceneObjects.drawXAxis()
		self.sceneObjects.drawYAxis()
		self.sceneObjects.drawZAxis()
		
		glPopMatrix()

	def setMouseBinding(self, mouseAction, state):
		self.bindings[mouseAction] = state

	def mouseAction(self, state):
		for key in self.bindings:
			if self.bindings[key] == state:
				return key
		
		return None

	def getMouseState(self, key):
		return self.bindings[key]

	def getMainWindow(self):
		return self.viewport.getMainWindow()

	def setBindings(self):
		self.setMouseBinding(MouseAction.TRANSLATE, QtCore.Qt.LeftButton)
		self.setMouseBinding(MouseAction.ROTATE, QtCore.Qt.LeftButton)
		self.setMouseBinding(MouseAction.ZOOM, QtCore.Qt.LeftButton)
		self.setMouseBinding(MouseAction.FIT, QtCore.Qt.LeftButton)
	
	def mouseMoveEvent(self, mouseEvent):
		""" The user has moved the mouse, which needs to be handled depending on the selected tool """
		self.makeCurrent()
		if self.currentTool == None:	
			self.cameraHandler.mouseMoveEvent(mouseEvent, self.camera)
			self.updateGL()
		else:
			self.currentTool.needUpdate = False
			if self.currentTool.needPicking:
				selection = self.picking(mouseEvent.pos(), mouseEvent.buttons())
				self.currentTool.handleMouseMove(mouseEvent, self.camera, self.viewportType, selection)
			else:
				self.currentTool.handleMouseMove(mouseEvent, self.camera, self.viewportType)
			if self.currentTool.needUpdate:
				self.prtManager.updateObjects()
				self.viewport.updateViewports()

		self.updateStatusBar.execute(mouseEvent)
		
		#if self.prtManager.isObjectSelected():
		#	self.picking(mouseEvent.pos(), mouseEvent.buttons())

	def mousePressEvent(self, mouseEvent):
		""" The user has pressed a mousebutton, which needs to be handled depending on the selected tool """
		self.makeCurrent()    # Rick 20091519
		if self.currentTool != None:
			self.currentTool.needUpdate = False
			if self.currentTool.needPicking:
				selection = self.picking(mouseEvent.pos(), mouseEvent.buttons())
				self.currentTool.handleMousePress(mouseEvent, self.camera, self.viewportType, selection)
			else:
				self.currentTool.handleMousePress(mouseEvent, self.camera, self.viewportType)

			if self.currentTool.needUpdate:
				self.prtManager.updateObjects()
				self.viewport.updateViewports()
		
		if isinstance(self.viewport, viewport.Viewport):
			self.viewport.mousePressEvent(mouseEvent)
	
	def mouseReleaseEvent(self, mouseEvent):
		if self.currentTool != None:
			self.currentTool.needUpdate = False
			if self.currentTool.needPicking:
				selection = self.picking(mouseEvent.pos(), mouseEvent.buttons())
				self.currentTool.handleMouseRelease(mouseEvent, selection)
			if self.currentTool.needUpdate:
				self.viewport.updateViewports()
	
	def keyPressEvent(self, keyEvent):
		if self.currentTool != None:
			self.currentTool.handleKeyPress(keyEvent)
			self.viewport.updateViewports()
	
	def keyReleaseEvent(self, keyEvent):
		if self.currentTool != None:
			self.currentTool.handleKeyRelease(keyEvent)
			self.viewport.updateViewports()
			
	def setBackgroundColor(self):
		self.makeCurrent()		
		self.qglClearColor(self.settings.sketcherData.bgColor)

	def drawRotationHelper(self):
		pass


	def drawWithPicking(self):
		self.prtManager.drawWithPicking()
		self.prtManager.drawTransparentWithPicking()

	def picking(self, point, buttons):
		self.startPicking(point)
		self.drawWithPicking()
		selection = self.endPicking(point, buttons)
		return selection

	def startPicking(self, point):
		self.makeCurrent()
		glSelectBuffer(self.bufferSize)
		glRenderMode(GL_SELECT)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		if self.currentTool != None and self.currentTool.multipleSelect and self.currentTool.selectionStarted:
			width = height = centerX = centerY = 0
			self.selectionRect = QtCore.QRect(self.currentTool.beginSelPoint, self.currentTool.endSelPoint)
			if self.selectionRect.width() < 0:
				width = -self.selectionRect.width()
			else:
				width = self.selectionRect.width()
			if self.selectionRect.height() < 0:
				height = -self.selectionRect.height()
			else:
				height = self.selectionRect.height()
			
			if width == 0:
				width = self.selectRegionWidth
			if height == 0:
				height = self.selectRegionHeight
			
			centerX = self.selectionRect.center().x()
			centerY = self.selectionRect.center().y()
			gluPickMatrix(centerX, centerY, width, height, self.camera.getViewport())
		else:
			gluPickMatrix(point.x(), point.y(), self.selectRegionWidth, self.selectRegionHeight, self.camera.getViewport())
		self.camera.loadProjection(False)
		self.camera.loadModelView()
		glInitNames()

	def endPicking(self, point, buttons):
		glFlush()
		hits = list(glRenderMode(GL_RENDER))
		self.selectionHandler.processHits(hits)
		selection = -1
				
		if len(hits) > 0:
			selection = self.selectionHandler.getOrderedHits()
		
		#print selection
			#self.prtManager.setSelectedObject(selection)
		
		#if selection != -1:
		#	self.prtManager.objectsSelected(selection, buttons)
		#print selectedName
		return selection
"""		

	def wheelEvent(self, wheelEvent):
		self.makeCurrent()
		if wheelEvent.delta() < 0 and self.zoomfactor > 1.0:
			self.zoomfactor=1.0
		elif wheelEvent.delta() > 0 and self.zoomfactor < 1.0:
			self.zoomfactor = 1.0
	
		if self.zoomfactor < 0.0:
			self.zoomfactor = 0.0
		
		self.zoomfactor -= wheelEvent.delta()/4*0.001
		self.zoom(self.zoomfactor)
		
	
		"""

class SolutionGLViewport(GLViewport):
	def __init__(self, viewport, vpType,shareWidget=None, format=None, parent=None):
		GLViewport.__init__(self, viewport, vpType, shareWidget, format, parent)
		#self.timer = QtCore.QTimer(self)
		#self.timer.start(1000)
		self.createTriggers()
			
	def createTriggers(self):
	    #QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("showGridChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("gridWidthChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("gridHeightChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("backgroundColorChanged"), self.setBackgroundColor)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("backgroundColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("pointSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("fPointSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("lineSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("distanceSizeChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("pointColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("fPointColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("lineColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("angleColorChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("distanceColorChanged"), self.update)

		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("pointVisChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("fpointVisChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("lineVisChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("angleVisChanged"), self.update)
		QtCore.QObject.connect(self.settings.svData,QtCore.SIGNAL("distanceVisChanged"), self.update)
     	
	def draw(self):
		self.viewport.drawObjects()

	def setBackgroundColor(self):
		self.makeCurrent()		
		self.qglClearColor(self.settings.svData.bgColor)

	def showGrid(self):		
		if self.settings.svData.showGrid:
			self.qglColor(QtGui.QColor(0.0, 0.0, 0.0)) 
			self.drawGrid()
	
	def drawGrid(self):
		if self.viewportType == ViewportType.PERSPECTIVE or self.viewportType == ViewportType.SOLUTION:
			self.sceneObjects.drawBackgroundgrid3D(600, 600, self.settings.svData.gridWidth, self.settings.svData.gridHeight, self.gridColor, False)
		else:
			self.sceneObjects.drawBackgroundgrid2D(self.settings.svData.gridWidth, self.settings.svData.gridHeight, self.gridColor, False)	
					
class SelectionHandler:
	""" Selection of the objects by the user """ 
	def __init__(self):
		self.hits = []
		self.selection = []
	
	def getClosestHit(self):
		""" select the objects which is closest to the user """ 
		self.selection[0] = [self.hits[0][2][0]]
		zMin = self.hits[0][0]
		for hit in self.hits:
			if hit[0] < zMin:
				zMin = hit[0]
				self.selection[0] = [hit[2][0]]
				if len(hit[2]) > 1:
					self.selection[0] += [hit[2][1]]

		""" check whether a subobject is selected (like axis) """
		if len(self.hits[0][2]) > 1:
			self.selection[0] += [self.hits[0][2][1]]
		return self.selection
	
	def getOrderedHits(self):
		aHit = False
		self.selection = []
		zBuffer = []
		for hit in self.hits:
			inserted = False
			for index, zValue in enumerate(zBuffer):
				if hit[0] <= zValue:
					zBuffer.insert(index, [hit[0]])
					self.selection.insert(index, [hit[2][0]])
					inserted = True
					break

			if not inserted:
				self.selection += [[hit[2][0]]]
				zBuffer += [hit[0]]
				
			if len(hit[2]) > 1:
				self.selection[len(self.selection)-1] += [hit[2][1]]
			aHit = True
		
		if not aHit:
			self.selection = [[-1]]

		return self.selection
			
	def getHits(self):
		""" Return al the hits, not ordered """
		aHit = False
		self.selection = []
		for index, hit in enumerate(self.hits):
			self.selection += [[hit[2][0]]]
			if len(hit[2]) > 1:
				self.selection[index] += [hit[2][1]]
			aHit = True

		if not aHit:
			self.selection = [[-1]]
			
		return self.selection
		
	def processHits(self, hits):
		""" Process the selection of the objects """
		self.hits = hits
		self.selection = [[-1]]
		
	

