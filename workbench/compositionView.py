from includes import *
from ui_compositionView import Ui_compositionView
from tree import Tree
from cvitems import CVCluster, CVPoint, CVInfoOverlay, CVConnection
from parameters import Settings

class CompositionView(QtGui.QDialog):
	""" A view where the decomposition of the system of constraints is visualised as a tree """
	def __init__(self, viewport, viewportMngr, vpType, prototypeMngr, parent=None):
		""" Initialization of the CompositionView class
			
		Parameters:
			viewportMngr - the manager of the viewports where the composition view can reside in
			prototypeMngr - the manager of the prototypes is used to obtain the results of the solver
		"""
		QtGui.QDialog.__init__(self, parent)
		self.prototypeManager = prototypeMngr
		self.viewport = viewport
		self.viewportManager = viewportMngr
		self.settings = Settings()
		self.setWindowFlags(QtCore.Qt.Window)
		self.timer = QtCore.QObject()
		#QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))
		
		self.tree = Tree(None)
		self.infoOverlay = CVInfoOverlay(self)
		self.connections = []
		self.ui = Ui_compositionView()
		self.ui.setupUi(self)
		self.ui.graphicsView.setupViewport(QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers|QtOpenGL.QGL.DoubleBuffer)))
		#self.ui.graphicsView.setViewport(QtGui.QWidget())
		self.ui.graphicsView.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
		
		self.collapsed = False
		self.currentTool = None
		self.viewportType = vpType
		self.first = False
		self.nodeId = 0

		self.overConstrainedColor = QtGui.QColor(0,0,255)
		self.underConstrainedColor = QtGui.QColor(255,0,0)
		self.wellConstrainedColor = QtGui.QColor(0,255,0)
		self.unsolvedColor = QtGui.QColor(125,124,255)
		
		self.setScene()
		self.createTriggers()
		
	def createTriggers(self):
		""" Create the triggers for the components in the graphical window """ 
		QtCore.QObject.connect(self.ui.zoomInButton,QtCore.SIGNAL("clicked()"),self.zoomIn)
		QtCore.QObject.connect(self.ui.zoomOutButton,QtCore.SIGNAL("clicked()"),self.zoomOut)
		QtCore.QObject.connect(self.ui.fitButton, QtCore.SIGNAL("clicked()"), self.fit)
		QtCore.QObject.connect(self.ui.collapseButton, QtCore.SIGNAL("clicked()"), self.collapse)
		QtCore.QObject.connect(self.ui.graphicsScene, QtCore.SIGNAL("changed(const QList<QRectF> & )"), self.updateSceneRect)
		QtCore.QObject.connect(self.ui.verticalSlider,QtCore.SIGNAL("valueChanged(int)"),self.setupMatrix)
		QtCore.QObject.connect(self.settings.dvData,QtCore.SIGNAL("treeOrientationChanged()"), self.updateTreeOrientation)
			
	def setScene(self):
		""" The scene where the tree is visualised in, will be created and set """
		self.initView()
	
	def getViewportType(self):
		return self.viewportType
		
	def updateGL(self):
		self.update()
	
	def createDecomposition(self):
		""" Create a new decomposition. If an older one exists it will be removed. """ 
		if self.ui.graphicsScene != None:
			for item in self.ui.graphicsView.items():
				item.hide()
				if item.parentItem() == None:
					self.ui.graphicsScene.removeItem(item)
			if self.tree.root != None:
				self.tree.clear(self.tree.root)
			del self.connections[:]
			del self.settings.dvData.fixedClusterIds[:]
			self.initView()
			
	def initView(self):
		""" Updating the view with new data and nodes for the visualisation of the tree """
		if self.prototypeManager.result != None:
			self.nodeId = 0
			self.tree.root = self.populateTree(self.prototypeManager.result.subs, None, self.prototypeManager.result)
			# return    # Rick 20090522 debug
			self.drawTree(self.ui.graphicsScene, self.tree.root, self.tree.root.children)
			self.drawConnections(self.ui.graphicsScene)
			self.determineCollapse(self.tree.root)
			self.showConnections()
			self.tree.root.showChildren()
			self.updateTree()
			self.addInfoOverlay()
			self.initFixStates()
				
	def updateViewports(self):
		self.viewportManager.updateViewports()
	
	def updateTree(self):
		""" Update the tree, where the node positions and connections between the nodes are updated """
		self.tree.clear(self.tree.root)
		self.tree.updateTree()
		self.updateNodePositions(self.tree.root)		
		self.showConnections()
		
	def populateTree(self, nodes, rootNode, currentNode, id=0):
		""" Recursive function to populate a tree, from the results of the solver to finally display it in the Decomposition View. 
		The population is depth first.
			
		Parameters:
			nodes 		- the childnodes
			rootNode 	- root node of the (partial) tree
			currentNode	- the current node of the result obtained from the constraints solver
		"""	
		if len(currentNode.variables) == 1:
			self.createLeafPoint(rootNode, currentNode.variables[0], self.nodeId)
			
		else:
			newNode = CVCluster(self, rootNode, self.nodeId)
			newNode.flag = currentNode.flag
			newNode.variables = currentNode.variables
			
			needCollapse = False		
			""" Add children to the rootNode to create the full tree """
			if rootNode != None:
				#self.setCollapse(newNode)
				
				rootNode.children += [newNode]
	
				""" Create a connection between the nodes if the current node has a rootnode"""
				newConnection = CVConnection(self, rootNode, newNode)
				self.connections += [newConnection]		
		
			""" get the leaf nodes """
			if len(nodes) == 0:
				for variable in newNode.variables:
					self.createLeafPoint(newNode, variable, self.nodeId)
		
		for node in nodes:
			self.nodeId += 1
			self.populateTree(node.subs, newNode, node, self.nodeId)
		
		""" To return the whole tree, a check will be performed for the rootnode """
		if rootNode == None:
			return newNode
	
	def initFixStates(self):
		""" Initialize the fix states from another view if available """
		for fixedId in self.settings.dvData.fixedClusterIds:
			self.updateState(fixedId, True, self.tree.root)
	
	def stateChange(self, id, fixed):
		""" Change the state of the cluster which might be fixed and report it 
			to the other decomposition views.
		
		Paramaters: 
			id - unique id of the cluster 
			fixed - should the clusters be fixed or not 
		"""
		self.viewportManager.updateDecompositionFixed(id, fixed)
		if fixed:
			self.settings.dvData.fixedClusterIds += [id]
		elif not fixed:
			self.settings.dvData.fixedClusterIds = filter(lambda x:x!=id, self.settings.dvData.fixedClusterIds)
			
	def updateState(self, id, fixed, rootNode):
		""" Update the fixed cluster, with the visuals. 
		Parameters:
			id - unique id of the cluster
			fixed - should the cluster be fixed or not
			rootNode - recursive funcion to walk the tree
		"""
		if rootNode.identifier == id:
			if fixed and rootNode.isVisible():
				rootNode.fixGraphic.show()
				rootNode.clusterActive = True
			elif fixed and not rootNode.isVisible():
				rootNode.fixGraphic.hide()
				rootNode.clusterActive = True
			else:
				rootNode.fixGraphic.hide()
				rootNode.clusterActive = False
				self.prototypeManager.removeClusterObjects([rootNode.permCluster], True, True)
				rootNode.permCluster = None
			return True
		
		for node in rootNode.children:
			found = self.updateState(id, fixed, node)
			if found:
				break
			
		return False
	
	def createLeafPoint(self, node, variable, id):
		cvPoint = CVPoint(self, node, id)
		cvPoint.setWidthAndHeight(20, 20)
		cvPoint.prtRef = self.prototypeManager.getObjectByKey(variable) 
		cvPoint.isCollapsed = False
		cvPoint.canCollapse = False
		#cvPoint.setInfoOverlay()
		node.children += [cvPoint]
		newConnection = CVConnection(self, node, cvPoint)
		self.connections += [newConnection]
	
	def setCollapse(self, node):
		node.isCollapsed = False
		if not isinstance(node, CVPoint):
			if not node.collapseFromResult():
				node.updateCluster()
	
	def determineCollapse(self, node):
		self.setCollapse(node)
		for child in node.children:
			self.determineCollapse(child)
		
	def addInfoOverlay(self):
		self.ui.graphicsScene.addItem(self.infoOverlay)
		self.infoOverlay.hide()
			
	def drawTree(self, scene, root, childNodes):
		""" The different nodes are added to the scene and will automatically be drawn 
			
		Parameters:
			scene		- the scene where the rootnode has to be drawn in
			root		- the rootnode of the (sub-) tree
			childNode	- the children of this root node
		"""
		root.setPos(root.position)
		scene.addItem(root)
		#print "#nodes: ", len(childNodes), " position: ",root.position.x(), " " , root.position.y()

		for node in childNodes:	
			self.drawTree(scene, node, node.children)
	
	def drawConnections(self, scene):
		""" The connections between the nodes are added to the scene and will automatically be drawn 
			
		Parameters:
			scene	- the scene where the connections has to be drawn in
		"""
		for connection in self.connections:
			#connection.setPos()
			scene.addItem(connection)
	
	def showConnections(self):
		""" Show/hide the connections between the nodes, this depends if the node is collapsed """
		for connection in self.connections:
			connection.setPos(connection.nodeTo.position)
			if connection.nodeFrom.isCollapsed or (connection.nodeTo.isVisible() == False):
				connection.hide()
			else:
				connection.show()
	
	def updateConnections(self):
		for connection in self.connections:
			connection.update()
	
	def nrVisibleConnections(self):
		number = 0
		#for connection in self.connections:
			#print "x, y: " , connection.x(), connection.y()
		#print "nr of visible connections: " , number 
	
	def updateNodePositions(self, node):
		""" Map the position of the nodes in the tree on the graphical view 
			
		Parameters:
			node	- a node in the tree for which the position is set
		"""
		node.setPos(node.position)

		for childNode in node.children:
			self.updateNodePositions(childNode)

	def updateSceneRect(self, rectList=None):
		self.ui.graphicsScene.setSceneRect(self.ui.graphicsScene.itemsBoundingRect())
	
	def updateTreeOrientation(self):
		self.tree.orientation = self.settings.dvData.treeAlignment
			
	def zoomIn(self):
		""" Zoom in the graphics view, by updating the vertical slider """
		self.ui.verticalSlider.setValue(self.ui.verticalSlider.value() + 1)
	
	def zoomOut(self):
		""" Zoom out the graphics view, by updating the vertical slider """
		self.ui.verticalSlider.setValue(self.ui.verticalSlider.value() - 1)
	
	def fit(self):
		""" Fits the tree exactly in the graphics view """
		self.ui.graphicsView.fitInView(0.0, 0.0, self.ui.graphicsScene.width(), self.ui.graphicsScene.height(), QtCore.Qt.KeepAspectRatio)
		""" Update the slider """
		value = (math.log(self.ui.graphicsView.matrix().m11(),2)*50) + 250.0
		self.ui.verticalSlider.setValue(value)
	
	def collapseAll(self, node):
		if node.canCollapse:
			node.collapse()
			for childNode in node.children:
				self.collapseAll(childNode)
		
	def expandAll(self, node):
		node.expand()
		for childNode in node.children:
			self.expandAll(childNode)
		
	def collapse(self):
		if self.collapsed:
			self.collapsed = False
			self.collapseAll(self.tree.root)
		else:
			self.collapsed = True
			self.expandAll(self.tree.root)
			
		self.updateTree()
		self.update()
			
	def setupMatrix(self, value):
		""" Zoom in/out the graphics view, depending on the value of the slider 
		
		Parameters
			value	-	value of the updated slider
		"""
		scale = math.pow(2.0, (self.ui.verticalSlider.value()-250.0)/50.0)
		matrix = QtGui.QMatrix()
		matrix.scale(scale,scale)

		self.ui.graphicsView.setMatrix(matrix)
