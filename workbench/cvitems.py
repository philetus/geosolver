from includes import *
from geosolver import GeometricCluster
from parameters import Settings

class CVCluster(QtGui.QGraphicsItem): 
    """ Visualisation of the clusters (nodes) in the decompositionView """
    def __init__(self, compView, cluster, x,y):
        QtGui.QGraphicsItem.__init__(self)
        
        self.compositionView = compView
        self.cluster = cluster
        self.position = QtCore.QPointF(x, y)

        self.textGraphic = QtGui.QGraphicsSimpleTextItem(str(list(self.cluster.variables)), self)
        #self.textGraphic.translate(x,y) 
        self.paintRect = self.textGraphic.boundingRect()
        #self.paintRect.translate(x,y)
        self.translate(x,y)
    
    def boundingRect(self):
        """ Overridden function where a update area is determined for painting and returned """
        return self.paintRect
 
    def paint(self, painter, option, widget):
        """ Visualisation of a clusteritem """
        painter.setPen(QtGui.QColor(0,155,50))

        if self.cluster.flag != None:
            if self.cluster.flag == GeometricCluster.OK:
                painter.setBrush(QtGui.QBrush(self.compositionView.wellConstrainedColor))
            elif self.cluster.flag == GeometricCluster.I_UNDER or self.cluster.flag == GeometricCluster.S_UNDER:
                painter.setBrush(QtGui.QBrush(self.compositionView.underConstrainedColor))
            elif self.cluster.flag == GeometricCluster.I_OVER or self.cluster.flag == GeometricCluster.S_OVER:
                painter.setBrush(QtGui.QBrush(self.compositionView.overConstrainedColor))
            elif self.cluster.flag == GeometricCluster.UNSOLVED:
                painter.setBrush(QtGui.QBrush(self.compositionView.unsolvedColor))
        painter.drawRect(self.paintRect)
        
           
        
class CVConnection(QtGui.QGraphicsItem):
    """ Visualisation of the connections between the clusters, where two types of visualisation can be chosen: Bezier(default) and Lines """
    def __init__(self, compView, nodeFrom , nodeTo):
        QtGui.QGraphicsItem.__init__(self)
        self.settings = Settings()
        self.compositionView = compView
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        self.beziercurve = None
        self.paintRect = None
        self.setZValue(1)
        
        self.determinePath()

    def determinePath(self):
        if self.nodeFrom != None and self.nodeTo != None:
            self.beziercurve = QtGui.QPainterPath()
            x1 = self.nodeFrom.position.x() + self.nodeFrom.paintRect.width()/2  
            x2 = self.nodeTo.position.x() + self.nodeTo.paintRect.width()/2  
            y1 = self.nodeFrom.position.y() 
            y2 = self.nodeTo.position.y() + self.nodeFrom.paintRect.height()    
            p1 = QtCore.QPointF(x1,y1)
            p2 = QtCore.QPointF(x1,y1+(y2-y1)/2)
            p3 = QtCore.QPointF(x2,y1+(y2-y1)/2)
            p4 = QtCore.QPointF(x2,y2)
            self.beziercurve.moveTo(p1)
            self.beziercurve.cubicTo(p2,p3,p4)
   
    def paint(self, painter, option, widget):
        """ Visualisation of the connection between two nodes """
        if self.beziercurve:
            painter.drawPath(self.beziercurve)
   
    def boundingRect(self):
        """ Overridden function where a update area is determined for painting and returned """    
        return self.beziercurve.boundingRect() 
 
