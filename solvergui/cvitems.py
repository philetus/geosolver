from includes import *
from tree import Node
from geosolver import GeometricCluster
from parameters import Settings

class CVCluster(QtGui.QGraphicsItem, Node): 
	""" Visualisation of the clusters (nodes) in the decompositionView """
	def __init__(self, compView, parentNode, id, parent=None):
		QtGui.QGraphicsItem.__init__(self, parent)
		Node.__init__(self, parentNode)
		
		self.compositionView = compView
		self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setAcceptsHoverEvents(True)
		self.startAngle = 0
		self.spanAngle = 0
		self.paintRect = QtCore.QRectF(0, 0, self.width, self.height)
		self.boundary = QtCore.QRectF(0.0, 0.0, 0.0, 0.0)	
		self.fixGraphic = QtGui.QGraphicsSimpleTextItem("F", self)
		
		self.identifier = id
		
		self.bezierCurve = None
		self.initAngles()
		self.bound = QtCore.QRectF()
		self.updateBound()
		self.flag = None
		self.clusterHighlight = None
		self.permCluster = None
		self.clusterActive = False
		self.fixGraphic.hide()
			
	def initAngles(self):
		""" Initialize the angles for the visual representation of the nodes, these are dependent on the orientation of the tree """
		self.startAngle = 60 * 16
		self.spanAngle = 60 * 16
		
		if self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
			self.startAngle = -self.startAngle
			self.spanAngle = -self.spanAngle
		elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
			self.startAngle = self.startAngle + 90 * 16
		elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
			self.startAngle = self.startAngle - 90 * 16
	
	def updateBound(self):
		""" The bound where the user can click in to do a certain action, is set here. This bound is tightly set around the object """
		pointBegin = QtCore.QPointF(0.0, 0.0)
		pointBegin.setX((self.paintRect.width()/2.0) * math.cos(math.radians(self.startAngle/16.0)))
		pointBegin.setY((self.paintRect.height()/2.0) * math.sin(math.radians(self.startAngle/16.0)))
		
		pointEnd = QtCore.QPointF(0.0, 0.0)
		pointEnd.setX((self.paintRect.width()/2.0) * math.cos(math.radians((self.startAngle+self.spanAngle)/16.0)))
		pointEnd.setY((self.paintRect.height()/2.0) * math.sin(math.radians((self.startAngle+self.spanAngle)/16.0)))
		
		pointMiddle = QtCore.QPointF(0.0, 0.0)
		halfDegree = (self.startAngle+(self.spanAngle/2.0))/16.0
		pointMiddle.setX((self.paintRect.width()/2.0) * math.cos(math.radians(halfDegree)))
		pointMiddle.setY((self.paintRect.height()/2.0) * math.sin(math.radians(halfDegree)))
		
		if pointBegin.x() < pointMiddle.x() and pointBegin.x() < pointEnd.x():
			self.boundary.setLeft(pointBegin.x())
		elif pointMiddle.x() < pointEnd.x():
			self.boundary.setLeft(pointMiddle.x())
		else:
			self.boundary.setLeft(pointEnd.x())
		
		if self.boundary.left() > 0.0:
			self.boundary.setLeft(0.0)
			
		if pointBegin.x() > pointMiddle.x() and pointBegin.x() > pointEnd.x():
			self.boundary.setRight(pointBegin.x())
		elif pointMiddle.x() > pointEnd.x():
			self.boundary.setRight(pointMiddle.x())
		else:
			self.boundary.setRight(pointEnd.x())
		
		if self.boundary.right() < 0.0:
			self.boundary.setRight(0.0)
		
		if pointBegin.y() < pointMiddle.y() and pointBegin.y() < pointEnd.y():
			self.boundary.setBottom(pointBegin.y())
		elif pointMiddle.y() < pointEnd.y():
			self.boundary.setBottom(pointMiddle.y())
		else:
			self.boundary.setBottom(pointEnd.y())
		
		if self.boundary.bottom() > 0.0:
			self.boundary.setBottom(0.0)
		
		if pointBegin.y() > pointMiddle.y() and pointBegin.y() > pointEnd.y():
			self.boundary.setTop(pointBegin.y())
		elif pointMiddle.y() > pointEnd.y():
			self.boundary.setTop(pointMiddle.y())
		else:
			self.boundary.setTop(pointEnd.y())
		
		if self.boundary.top() < 0.0:
			self.boundary.setTop(0.0)
		
		self.__translateBound()

		
	def __translateBound(self):
		""" Translation of the boundary, so that it fits exactly around the figure"""
		self.boundary.setLeft(self.boundary.left()+self.paintRect.center().x())
		self.boundary.setRight(self.boundary.right()+self.paintRect.center().x())
		self.boundary.setTop(-self.boundary.top()+self.paintRect.center().y())
		self.boundary.setBottom(-self.boundary.bottom()+self.paintRect.center().y())
	
	def shape(self):	
		""" Overridden function to set the boundary wherein the user can perform an action """
		path = QtGui.QPainterPath()
		path.addRect(self.boundary)
		return path
			
	def boundingRect(self):
		""" Overridden function where a update area is determined for painting and returned """
		return self.paintRect
	
	def paint(self, painter, option, widget):
		""" Visualisation of a clusteritem """
		painter.setPen(QtGui.QColor(0,155,50))

		if self.flag != None:
			if self.flag == GeometricCluster.OK:
				painter.setBrush(QtGui.QBrush(self.compositionView.wellConstrainedColor))
			elif self.flag == GeometricCluster.I_UNDER or self.flag == GeometricCluster.S_UNDER:
				painter.setBrush(QtGui.QBrush(self.compositionView.underConstrainedColor))
			elif self.flag == GeometricCluster.I_OVER or self.flag == GeometricCluster.S_OVER:
				painter.setBrush(QtGui.QBrush(self.compositionView.overConstrainedColor))
			elif self.flag == GeometricCluster.UNSOLVED:
				painter.setBrush(QtGui.QBrush(self.compositionView.unsolvedColor))
		painter.drawPie(self.paintRect, self.startAngle, self.spanAngle)
		
	def setInfoOverlay(self):
		constrInfo = QtCore.QString("")
		if self.flag == GeometricCluster.OK:
			 constrInfo = QtCore.QString("Well-Constrained\n")
		elif self.flag == GeometricCluster.I_UNDER:
			 constrInfo = QtCore.QString("Inc. Underconstrained\n")
		elif self.flag == GeometricCluster.S_UNDER:
			constrInfo = QtCore.QString("Struct. Underconstrained\n")
		elif self.flag == GeometricCluster.I_OVER:
			constrInfo = QtCore.QString("Inc. Overconstrained\n")
		elif self.flag == GeometricCluster.S_OVER:
			constrInfo = QtCore.QString("Struct. Overconstrained\n")
		elif self.flag == GeometricCluster.UNSOLVED:
			constrInfo = QtCore.QString("Unsolved\n")
		constrInfo.append("Points: ")
		
		for point in self.variables:
			pointObject = self.compositionView.prototypeManager.getObjectByKey(point)
			if pointObject != None:
				constrInfo.append(pointObject.name)
				if point != self.variables[-1]:
					constrInfo.append(", ")
		
		self.compositionView.infoOverlay.infoText = constrInfo

		#painter.setBrush(QtCore.Qt.NoBrush)
		#painter.drawRect(self.bound)
			
	def mousePressEvent(self, event):
		""" Handling the mouse press, where the cluster (visualisation) and tree can be updated 
		
		Parameters:
			event	- pressed mousebutton
		"""
		if event.button() == QtCore.Qt.LeftButton:
			self.updateCluster()
			self.updateBound()
			self.compositionView.updateTree()
		elif event.button() == QtCore.Qt.RightButton:
			if not self.clusterActive:
				self.permanentCluster()
				self.clusterActive = True
				self.fixGraphic.show()
				self.compositionView.stateChange(self.identifier, True)
			else:
				self.compositionView.prototypeManager.removeClusterObjects([self.permCluster], True, True)
				self.clusterActive = False
				self.fixGraphic.hide()
				self.compositionView.stateChange(self.identifier, False)
				self.permCluster = None
				self.compositionView.prototypeManager.setObjectVisibilityByClusters()
			self.compositionView.updateViewports()

	def hoverEnterEvent(self, event):
		self.setZValue(2)
		self.setInfoOverlay()
		self.compositionView.infoOverlay.setPosition(event.scenePos())
		self.compositionView.infoOverlay.show()
		if not self.clusterActive:
			self.compositionView.prototypeManager.selectObjectsByKeys(self.variables)
			self.highlightCluster()
		self.compositionView.update()
		self.compositionView.updateViewports()	
		
	def hoverMoveEvent(self, event):
		self.overlayPosition = self.compositionView.ui.graphicsView.mapFromScene(event.scenePos())
		self.compositionView.infoOverlay.setPosition(event.scenePos())
		
		self.compositionView.updateConnections()
		self.compositionView.update()
		
	def hoverLeaveEvent(self, event):
		self.setZValue(0)
		self.compositionView.infoOverlay.infoText = ""
		self.compositionView.infoOverlay.hide()
		self.compositionView.infoOverlay.update()
		if not self.clusterActive:
			self.compositionView.prototypeManager.deselectAllObjects()
			self.compositionView.prototypeManager.removeClusterObjects([self.clusterHighlight], True, False)
			self.compositionView.updateViewports()
		
	def updateCluster(self):
		""" Cluster update, where the cluster is (un-)collapsed depending on the state of the cluster, to visualise a certain part of the tree """
		if self.canCollapse:
			if self.isCollapsed:
				self.isCollapsed = False
				self.showChildren()
				height = self.paintRect.height()*0.5
				width = self.paintRect.width()*0.5
				height2 = self.paintRect.height()
				if self.compositionView.tree.orientation == TreeOrientation.TOP:
					self.paintRect.setTop(self.paintRect.top() + height )
					self.paintRect.setBottom(self.paintRect.bottom() + height)
				elif self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
					self.paintRect.setTop(self.paintRect.top()- height )
					self.paintRect.setBottom(self.paintRect.bottom() - height)
				elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
					self.paintRect.setLeft(self.paintRect.left() + width)
					self.paintRect.setRight(self.paintRect.right() + width)
				elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
					self.paintRect.setLeft(self.paintRect.left() - width)
					self.paintRect.setRight(self.paintRect.right() - width)
			else:
				self.isCollapsed = True
				self.showChildren()
				height = self.paintRect.height()*0.5
				width = self.paintRect.width()*0.5
				height2 = self.paintRect.height()
				if self.compositionView.tree.orientation == TreeOrientation.TOP:
					self.paintRect.setTop(self.paintRect.top() - height)
					self.paintRect.setBottom(self.paintRect.bottom() - height)
				elif self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
					self.paintRect.setTop(self.paintRect.top() + height)
					self.paintRect.setBottom(self.paintRect.bottom() + height)
				elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
					self.paintRect.setLeft(self.paintRect.left() - width)
					self.paintRect.setRight(self.paintRect.right() - width)
				elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
					self.paintRect.setLeft(self.paintRect.left() + width)
					self.paintRect.setRight(self.paintRect.right() + width)
			
			if self.compositionView.tree.orientation == TreeOrientation.LEFT or self.compositionView.tree.orientation == TreeOrientation.RIGHT:
				self.startAngle = self.startAngle + 180 * 16
			else:
				self.startAngle = -self.startAngle
				self.spanAngle = -self.spanAngle
	
	def highlightCluster(self):
		if self.clusterHighlight != None:
			if self.clusterHighlight.temporary:
				self.compositionView.prototypeManager.addClusterObject(self.clusterHighlight)
			self.clusterHighlight.selected = True
		else:
			self.clusterHighlight = self.compositionView.prototypeManager.selectClusterObjectByKeys(self.variables)
			if self.clusterHighlight == None:
				self.clusterHighlight = self.compositionView.prototypeManager.createCluster(self.variables)
				if self.clusterHighlight != None:
					self.clusterHighlight.temporary = True
			if self.clusterHighlight != None:
				self.clusterHighlight.selected = True 
	
	def permanentCluster(self):
		if self.permCluster == None:
			self.permCluster = self.compositionView.prototypeManager.createCluster(self.variables, self.flag)
			self.permCluster.temporary = True
			self.permCluster.fixed = True
			self.compositionView.prototypeManager.setObjectVisibilityByClusters()
		else:
			self.compositionView.prototypeManager.addClusterObject(self.permCluster)
		self.permCluster.selected = False
			
	def showChildren(self):
		""" Show the children of this node """
		if self.isCollapsed or (self.isVisible()==False):
			for child in self.children:
				child.hide()
				child.showChildren()
				if child.clusterActive:
					child.fixGraphic.hide()
		else:
			for child in self.children:
				child.show()
				child.showChildren()
				if child.clusterActive:
					child.fixGraphic.show()
				else:
					child.fixGraphic.hide()
	
	def collapseFromResult(self):
		if self.flag == GeometricCluster.I_UNDER or self.flag == GeometricCluster.S_UNDER or self.flag == GeometricCluster.I_OVER or self.flag == GeometricCluster.S_OVER or self.flag == GeometricCluster.UNSOLVED:
			return True
		else:
			return False
	
	def collapse(self):
		if not self.isCollapsed:
			self.updateCluster()
			self.updateBound()
	
	def expand(self):
		if self.isCollapsed:
			self.updateCluster()
			self.updateBound()
				
class CVPoint(QtGui.QGraphicsItem, Node):
	""" Visualisation of the leaves of the 'leaf' clusters in the tree """
	def __init__(self, compView, parentNode, id, parent=None):
		QtGui.QGraphicsItem.__init__(self, parent)
		Node.__init__(self, parentNode)
		
		self.compositionView = compView
		self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setAcceptsHoverEvents(True)
		self.startAngle = 0
		self.spanAngle = 0
		self.paintRect = QtCore.QRectF(0, 0, self.width/2, self.height/2)
		self.fixGraphic = QtGui.QGraphicsSimpleTextItem("F", self)
		self.fixGraphic.hide()
		self.bezierCurve = None
		self.flag = None
		self.prtRef = None
		self.boundary = self.paintRect
		self.clusterHighlight = None
		self.permCluster = None
		self.clusterActive = False
		self.identifier = id

	def paint(self, painter, option, widget):
		painter.setPen(QtGui.QColor(0,155,50))
		painter.setBrush(QtGui.QBrush(QtGui.QColor(0,155,50)))
		painter.drawEllipse(self.paintRect)
		
	def setInfoOverlay(self):
		constrInfo = QtCore.QString("Points \n")
		if self.prtRef != None:
			constrInfo += "Name: " + self.prtRef.name + "\n"
			constrInfo += "Position: (" + str(round(self.prtRef.position[0],2)) + " , " + str(round(self.prtRef.position[1])) + " , " + str(round(self.prtRef.position[2])) + ")"
		self.compositionView.infoOverlay.infoText = constrInfo
	
	def mousePressEvent(self, event):
		""" Handling the mouse press, where the cluster (visualisation) is handled 
		
		Parameters:
			event	- pressed mousebutton
		"""
		if event.button() == QtCore.Qt.RightButton:
			if not self.clusterActive:
				self.permanentCluster()
				self.clusterActive = True
				self.fixGraphic.show()
				self.compositionView.stateChange(self.identifier, True)
			else:
				self.compositionView.prototypeManager.removeClusterObjects([self.permCluster], True, True)
				self.clusterActive = False
				self.permCluster = None
				self.fixGraphic.hide()
				self.compositionView.stateChange(self.identifier, False)
				self.compositionView.prototypeManager.setObjectVisibilityByClusters()
			self.compositionView.updateViewports()
				
	def hoverEnterEvent(self, event):
		self.setZValue(2)
		self.setInfoOverlay()
		self.compositionView.infoOverlay.setPosition(event.scenePos())
		self.compositionView.infoOverlay.show()

		if not self.clusterActive:
			self.compositionView.prototypeManager.selectObject(self.prtRef)
			self.highlightCluster()
		self.compositionView.update()
		self.compositionView.updateViewports()
		
	def hoverMoveEvent(self, event):
		self.compositionView.infoOverlay.setPosition(event.scenePos())
		self.compositionView.update()
		
	def hoverLeaveEvent(self, event):
		self.setZValue(0)
		self.compositionView.infoOverlay.infoText = ""
		self.compositionView.infoOverlay.hide()
		self.compositionView.infoOverlay.update()
		if not self.clusterActive:
			self.compositionView.prototypeManager.deselectAllObjects()
			self.compositionView.prototypeManager.removeClusterObjects([self.clusterHighlight], True)
			self.compositionView.updateViewports()
				
	def highlightCluster(self):
		if self.clusterHighlight != None:
			if self.clusterHighlight.temporary:
				self.compositionView.prototypeManager.addClusterObject(self.clusterHighlight)
			self.clusterHighlight.selected = True
		else:
			self.clusterHighlight = self.compositionView.prototypeManager.selectClusterObjectByKeys([self.prtRef.key])
			if self.clusterHighlight == None:
				self.clusterHighlight = self.compositionView.prototypeManager.createCluster([self.prtRef.key])
				if self.clusterHighlight != None:
					self.clusterHighlight.temporary = True
			if self.clusterHighlight != None:
				self.clusterHighlight.selected = True 
	
	def permanentCluster(self):
		if self.permCluster == None:
			self.permCluster = self.compositionView.prototypeManager.createCluster([self.prtRef.key])
			self.permCluster.temporary = True
			self.permCluster.fixed = True
			self.compositionView.prototypeManager.setObjectVisibilityByClusters()
		else:
			self.compositionView.prototypeManager.addClusterObject(self.permCluster)
		self.permCluster.selected = False
				
	def boundingRect(self):
		return self.paintRect
	
	def setWidthAndHeight(self, width, height):
		self.width = width
		self.height = height
		self.paintRect.setWidth(width)
		self.paintRect.setHeight(height)
								
	def showChildren(self):
		""" Show the children of this node """
		if self.isCollapsed or (self.isVisible()==False):
			for child in self.children:
				child.hide()
				child.showChildren()
		else:
			for child in self.children:
				child.show()
				child.showChildren()
	
	def collapse(self):
		self.isCollapsed = True
	
	def expand(self):
		self.isCollapsed = False

class CVInfoOverlay(QtGui.QGraphicsItem):
	def __init__(self, compView, parent=None):
		QtGui.QGraphicsItem.__init__(self, parent)
		self.node = None
		self.compositionView = compView
		self.infoText = QtCore.QString("")
		self.setZValue(3)
		self.infoOverlay = QtCore.QRectF(0, 0, 140, 50)
		self.overlayPosition = QtCore.QPointF()
		self.scenePosition = QtCore.QPointF()

		self.overlayBGColor = QtGui.QColor(204, 251, 255, 200)
		self.overlayLineColor = QtGui.QColor(33, 116, 154)
		self.overlayTextColor = QtGui.QColor(0, 0, 0)
				
	def paint(self, painter, option, widget):
		painter.save()
		painter.resetMatrix()
		painter.translate(self.overlayPosition)
		painter.translate(10.0, 10.0)
		painter.setPen(self.overlayLineColor)
		painter.setBrush(self.overlayBGColor)
		painter.drawRect(self.infoOverlay)
		
		infoFont = QtGui.QFont("Arial", 7)
		infoFont.setStyleStrategy(QtGui.QFont.ForceOutline)
		painter.setFont(infoFont)
		painter.setRenderHint(QtGui.QPainter.TextAntialiasing, False)
		painter.setPen(self.overlayTextColor)
		textRect = QtCore.QRect(self.infoOverlay.left()+4, self.infoOverlay.top(), self.infoOverlay.width()-3, self.infoOverlay.height()-3)
		
		painter.drawText(textRect, QtCore.Qt.AlignLeft|QtCore.Qt.TextWordWrap, self.infoText)
		painter.restore()
	
	def setPosition(self, position):
		self.scenePosition = position
		self.overlayPosition = self.compositionView.ui.graphicsView.mapFromScene(position)
	
	def boundingRect(self):
		check = QtCore.QRectF(self.infoOverlay)
		return check
			
class CVConnection(QtGui.QGraphicsItem):
	""" Visualisation of the connections between the clusters, where two types of visualisation can be chosen: Bezier(default) and Lines """
	def __init__(self, compView, nodeFrom , nodeTo, parent=None):
		QtGui.QGraphicsItem.__init__(self, parent)
		self.settings = Settings()
		self.compositionView = compView
		self.nodeFrom = nodeFrom
		self.nodeTo = nodeTo
		self.connectType = self.settings.dvData.treeConnection
		#self.boundRect = QtCore.QRectF(0.0, 0.0, 0.0, 0.0)
		self.beziercurve = None
		self.paintRect = QtCore.QRectF(0, 0, 0, 0)
		self.setZValue(1)
		
	def paint(self, painter, option, widget):
		""" Visualisation of the connection between two nodes """
		if self.nodeFrom != None and self.nodeTo != None:
			painter.setPen(QtGui.QColor(0,0,0))
			
			diffPosExt = self.paintRect
			endPoint = self.determineEndpoint(diffPosExt)

			if self.connectType == ConnectionType.BEZIER:	
				""" display a bezier curve as connection """
				self.beziercurve = QtGui.QPainterPath()
				
				if self.compositionView.tree.orientation == TreeOrientation.TOP:
					self.beziercurve.moveTo(diffPosExt.x(), diffPosExt.y())
					firstPoint = QtCore.QPointF(diffPosExt.x(), diffPosExt.height()*0.5)
				elif self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
					self.beziercurve.moveTo(diffPosExt.x(), diffPosExt.bottom())
					firstPoint = QtCore.QPointF(diffPosExt.x(), -diffPosExt.height()*0.5 + self.nodeTo.paintRect.height()) 
				elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
					self.beziercurve.moveTo(diffPosExt.x(), diffPosExt.y())
					firstPoint = QtCore.QPointF(diffPosExt.width()*0.5, diffPosExt.y()) 
				elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
					self.beziercurve.moveTo(diffPosExt.x(), diffPosExt.y())
					firstPoint = QtCore.QPointF(self.nodeTo.paintRect.width() + diffPosExt.width()*0.5,diffPosExt.y())
					
				if self.compositionView.tree.orientation == TreeOrientation.TOP:
					secondPoint = QtCore.QPointF(diffPosExt.right(),diffPosExt.height()*0.5)
				elif self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
					secondPoint = QtCore.QPointF(diffPosExt.right(), self.nodeTo.paintRect.height() - diffPosExt.height()*0.5)
				elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
					secondPoint = QtCore.QPointF(diffPosExt.width()*0.5, diffPosExt.bottom())
				elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
					secondPoint = QtCore.QPointF(self.nodeTo.paintRect.width() + diffPosExt.width()*0.5, diffPosExt.bottom())

				self.beziercurve.cubicTo(firstPoint, secondPoint, endPoint)
				painter.drawPath(self.beziercurve)

			elif self.connectType == ConnectionType.LINES:
				""" draw a straight line """
				if self.compositionView.tree.orientation == TreeOrientation.TOP:
					painter.drawLine(QtCore.QPointF(self.nodeTo.paintRect.width()*0.5, 0.0), QtCore.QPointF(endPoint.x(), endPoint.y()))
				elif self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
					painter.drawLine(QtCore.QPointF(self.nodeTo.paintRect.width()*0.5, self.nodeTo.paintRect.height()), QtCore.QPointF(endPoint.x(), endPoint.y()))
				elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
					painter.drawLine(QtCore.QPointF(0.0, self.nodeTo.paintRect.height()*0.5), QtCore.QPointF(endPoint.x(), endPoint.y()))
				elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
					painter.drawLine(QtCore.QPointF(self.nodeTo.paintRect.width(), self.nodeTo.paintRect.height()*0.5), QtCore.QPointF(endPoint.x(), endPoint.y()))			
	
	def areaBetweenNodes(self):
		diffPos = self.nodeTo.position - self.nodeFrom.position
		area = QtCore.QRectF(0.0, 0.0, 0.0 , 0.0)
		if self.compositionView.tree.orientation == TreeOrientation.TOP:
			area.setX(self.nodeTo.paintRect.width()*0.5)
			area.setY(0.0)
			area.setRight(self.nodeFrom.paintRect.width()*0.5 - diffPos.x())
			area.setBottom(self.nodeTo.boundary.height()-diffPos.y())
		elif self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
			area.setX(self.nodeTo.paintRect.width()*0.5)
			area.setY(-diffPos.y()+self.nodeFrom.boundary.height())
			area.setRight(-diffPos.x()+self.nodeFrom.paintRect.width()*0.5)
			area.setBottom(self.nodeTo.paintRect.height())
		elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
			area.setX(0.0)
			area.setY(self.nodeTo.paintRect.height()*0.5)
			area.setRight(-diffPos.x()+self.nodeFrom.boundary.width())
			area.setBottom(-diffPos.y() + self.nodeFrom.paintRect.height()*0.5)
		elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
			area.setX(self.nodeTo.paintRect.width())
			area.setY(self.nodeTo.paintRect.height()*0.5)
			area.setRight(-diffPos.x() + self.nodeFrom.paintRect.width()*0.5)
			area.setBottom(-diffPos.y() + self.nodeFrom.paintRect.height()*0.5)
		return area
			
	def determineEndpoint(self, area):
		endPoint = QtCore.QPointF(0.0, 0.0)

		if self.compositionView.tree.orientation == TreeOrientation.TOP:
			endPoint.setX(area.right())
			endPoint.setY(area.height())
		elif self.compositionView.tree.orientation == TreeOrientation.BOTTOM:
			endPoint.setX(area.right())
			endPoint.setY(area.y())
		elif self.compositionView.tree.orientation == TreeOrientation.LEFT:
			endPoint.setX(area.right())
			endPoint.setY(area.bottom())
		elif self.compositionView.tree.orientation == TreeOrientation.RIGHT:
			endPoint.setX(area.right())
			endPoint.setY(area.bottom())
		return endPoint
		
	def boundingRect(self):
		""" Overridden function where a update area is determined for painting and returned """	
		self.paintRect = self.areaBetweenNodes()	
		return self.paintRect
