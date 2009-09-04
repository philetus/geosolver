import pdb
from includes import *
from constants import *
from viewport import *

class ViewportManager:
	def __init__(self, window):
		self.activeViewport = None

		self.mainWindow = window
		self.viewportList = []	
		self.viewport = None
		self.splitterVertical = QtGui.QSplitter()
		
		self.frmt = QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers)
		#self.frmt.setDoubleBuffer(True)
		#self.frmt.setOverlay(True)	
		self.displayViewport = DisplayViewport.ALL
		self.mouseActiveAction = None
		
	def getActiveViewportType(self):
		return self.activeViewport

	def getMainWindow(self):
		return self.mainWindow

	def showViewport(self, displViewport, vpType):
		self.cleanUp()
		self.displayViewport = displViewport
		
		if displViewport == DisplayViewport.ALL:
			self.showAll()
		elif displViewport == DisplayViewport.SINGLE:
			self.showSingle(vpType)
			
	def showAll(self):
		self.viewDownLeft = Viewport(self, ViewportType.FRONT)
		self.viewUpRight = Viewport(self, ViewportType.SIDE)
		self.viewUpLeft = Viewport(self, ViewportType.TOP)
		self.viewDownRight = Viewport(self, ViewportType.PERSPECTIVE)
		self.activeViewport = self.viewUpLeft

		self.viewportList = [self.viewUpLeft]
		self.viewportList += [self.viewDownLeft]
		self.viewportList += [self.viewUpRight]
		self.viewportList += [self.viewDownRight]
				
		# splits the upper and lower two windows
		self.splitterVertical = QtGui.QSplitter()
		self.splitterVertical.setHandleWidth(3)
		self.splitterVertical.setOrientation(QtCore.Qt.Vertical)
		
		# splits the top windows into left and right
		splitterHorUp = QtGui.QSplitter()
		splitterHorUp.setHandleWidth(3)
		splitterHorUp.addWidget(self.viewUpLeft)
		splitterHorUp.addWidget(self.viewUpRight)
		self.splitterVertical.addWidget(splitterHorUp)
		
		# splits the lower windows into left and right
		splitterHorDown = QtGui.QSplitter()
		splitterHorDown.setHandleWidth(3)
		splitterHorDown.addWidget(self.viewDownLeft)
		splitterHorDown.addWidget(self.viewDownRight)
		splitterHorDown.moveSplitter(50, 1)
		self.splitterVertical.addWidget(splitterHorDown)
		self.mainWindow.setCentralWidget(self.splitterVertical)
		

	def showSingle(self, vpType):	
		self.viewport = Viewport(self, vpType)
		self.mainWindow.setCentralWidget(self.viewport)
		self.viewport.showMaximized()

	def updateViewports(self):
		if self.displayViewport == DisplayViewport.ALL:
			for viewport in self.viewportList:
				viewport.glViewport.updateGL()
		elif self.displayViewport == DisplayViewport.SINGLE:
			self.viewport.glViewport.updateGL()
	
	def updateSolution(self):
		if self.displayViewport == DisplayViewport.ALL:
			for viewport in self.viewportList:
				if viewport.solutionView != None and viewport.glViewport.getViewportType() == ViewportType.SOLUTION:
					viewport.solutionView.createSolution()
		elif self.displayViewport == DisplayViewport.SINGLE:
			if self.viewport.solutionView != None and self.viewport.glViewport.getViewportType() == ViewportType.SOLUTION:
					self.viewport.solutionView.createSolution()
	
	def updateDecomposition(self):
		if self.displayViewport == DisplayViewport.ALL:
			for viewport in self.viewportList:
				if viewport.glViewport != None and viewport.glViewport.viewportType == ViewportType.DECOMPOSITION:
					viewport.glViewport.createDecomposition()
		elif self.displayViewport == DisplayViewport.SINGLE:
			if self.viewport.glViewport != None and self.viewport.glViewport.viewportType == ViewportType.DECOMPOSITION:
					viewport.glViewport.createDecomposition()
			
	def updateDecompositionFixed(self, id, fixed):
		if self.displayViewport == DisplayViewport.ALL:
			for viewport in self.viewportList:
				if viewport.glViewport != None and viewport.glViewport.viewportType == ViewportType.DECOMPOSITION:
					viewport.glViewport.updateState(id, fixed, viewport.glViewport.tree.root)
		if self.mainWindow.compositionView != None:
			self.mainWindow.compositionView.updateState(id, fixed, self.mainWindow.compositionView.tree.root)
						
	def resetScene(self):
		if self.displayViewport == DisplayViewport.ALL:
			for viewport in self.viewportList:
				viewport.resetViewport()
		elif self.displayViewport == DisplayViewport.SINGLE:
			self.viewport.resetViewport()	

	def cleanUp(self):
		if self.displayViewport == DisplayViewport.ALL:
			for i in range(len(self.viewportList)):
				self.viewportList[i].takeWidget()
				self.viewportList[i].close()
				self.viewportList[i] = None
			self.viewportList = []
			self.splitterVertical.close()
		elif self.displayViewport == DisplayViewport.SINGLE:
			if not self.viewport == None:
				self.viewport.takeWidget()
				self.viewport.close()
			self.viewport=None
					
		self.mainWindow.setCentralWidget(None)
	
	def minmaxView(self):
		if self.displayViewport == DisplayViewport.ALL:
			self.showViewport(DisplayViewport.SINGLE, self.activeViewport.glViewport.viewportType)
		elif self.displayViewport == DisplayViewport.SINGLE: 
			self.showViewport(DisplayViewport.ALL, None)


	



