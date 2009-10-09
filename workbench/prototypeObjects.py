"""    Creational Pattern: Prototype pattern"""
from copy import copy, deepcopy
from includes import *
from parameters import Settings
from quaternion import *
from singleton import *
import geosolver  
from geosolver import GeometricCluster 
import delaunay._qhull as qhull
import delaunay.core as dcore
from geosolver.matfunc import Vec
import numpy.numarray as Numeric

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    app = QtGui.QApplication( sys.argv )
    QtGui.QMessageBox.critical( None, "OpenGL grabber", "PyOpenGL must be installed to run this example.", 
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton )
    sys.exit( 1 )

class PrototypeManager( Singleton ):
    """ The prototype manager handles the objects needed for the different viewports. Also it handles the connection
    with the geometric constraint solver, e.g. when a new object is added (deleted) it will also be added (deleted) 
    to (from) the constraint graph. Updates for visualisation or constraint solving is handled too."""
    def __init__( self ):
        """ The initilization of the class is done once, else the one and only instance is returned. """
        Singleton.__init__( self )
        if self._isNew:
            self.prtObjects = []
            self.clsObjects = []
            self.importedObjs = []
            self.copyOfObjects = []
            self.transpPrtObjects = []
            self.axis = Axis( [0.0, 0.0, 0.0], 1.0, 40.0 )
            self.objectSelected = None
            self.objectIsSelected = False
            self.showAxis = False
            self.objectNr = 1
            self.geoProblem = geosolver.GeometricProblem( dimension=3 )
            self.selectCounter = 0
            self.panel = None
            self.result = None
            self.visualiseClusters = True
            self.settings = Settings()
            self.createTriggers()
            self.nrOfImports = 0
    
    def createTriggers(self):
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("pointSizeChanged"), self.updateSize)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("fPointSizeChanged"), self.updateSize)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("lineSizeChanged"), self.updateSize)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("distanceSizeChanged"), self.updateSize)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("pointColorChanged"), self.updateColor)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("fPointColorChanged"), self.updateColor)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("lineColorChanged"), self.updateColor)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("angleColorChanged"), self.updateColor)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("selectionColorChanged"), self.updateColor)
        QtCore.QObject.connect(self.settings.sketcherData,QtCore.SIGNAL("distanceColorChanged"), self.updateColor)
        
    def updateSize(self):
        for prtObject in self.prtObjects:
            if prtObject.objType == ObjectType.POINT:
                prtObject.radius = self.settings.sketcherData.pointRadius
            elif prtObject.objType == ObjectType.FIXED_POINT:
                prtObject.radius = self.settings.sketcherData.fPointRadius
            elif prtObject.objType == ObjectType.DISTANCE_HELPER:
                prtObject.radius = self.settings.sketcherData.lineRadius
            elif prtObject.objType == ObjectType.DISTANCE_CONSTRAINT:
                prtObject.radius = self.settings.sketcherData.distanceRadius
            # Rick 20090519
            #elif prtObject.objType == ObjectType.DISTANCE_CLUSTER:
            #    prtObject.radius = self.settings.sketcherData.distanceRadius * 1.5
            # but which to choose for these?
            #elif prtObject.objType == ObjectType.POINT_CLUSTER: 
            #    prtObject.radius = self.settings.sketcherData.pointRadius * 1.5 
            #    prtObject.radius = self.settings.sketcherData.fpointRadius * 1.5 
   
    def updateColor(self):
        for prtObject in self.prtObjects:
            if prtObject.objType == ObjectType.POINT:
                prtObject.color = self.settings.sketcherData.pointColor
            elif prtObject.objType == ObjectType.FIXED_POINT:
                prtObject.color = self.settings.sketcherData.fPointColor
            elif prtObject.objType == ObjectType.DISTANCE_HELPER:
                prtObject.color = self.settings.sketcherData.lineColor
            elif prtObject.objType == ObjectType.DISTANCE_CONSTRAINT:
                prtObject.color = self.settings.sketcherData.distanceColor
            elif prtObject.objType == ObjectType.ANGLE_CONSTRAINT:
                prtObject.color = self.settings.sketcherData.angleColor
            prtObject.selectColor = self.settings.sketcherData.selectColor
                
    def addObject( self, prtobject ):    
        """ Try to add a new object to the constraint graph 
        
        Parameters:
            prtobject - prototype object which must be added to the constraint graph    
        """
        if not prtobject.ghost:
            if prtobject.objType == ObjectType.POINT:
                self.geoProblem.add_point( prtobject.key, Vec( [prtobject.position[0], prtobject.position[1], prtobject.position[2]] ) )
            elif prtobject.objType == ObjectType.FIXED_POINT:
                self.geoProblem.add_point( prtobject.key, Vec( [prtobject.position[0], prtobject.position[1], prtobject.position[2]] ) )
                self.geoProblem.add_constraint(geosolver.FixConstraint( prtobject.key, Vec ( [prtobject.position[0], prtobject.position[1], prtobject.position[2]] ) ) )
            elif prtobject.objType == ObjectType.DISTANCE_CONSTRAINT:
                prtobject.con = geosolver.DistanceConstraint( prtobject.pointBegin.key, prtobject.pointEnd.key, prtobject.distance )
                self.geoProblem.add_constraint( prtobject.con )
            elif prtobject.objType == ObjectType.ANGLE_CONSTRAINT:
                prtobject.con = geosolver.AngleConstraint( prtobject.pointBegin.key, prtobject.pointMiddle.key, prtobject.pointEnd.key, prtobject.angle )
                self.geoProblem.add_constraint( prtobject.con )
            """ if the addition of the new object succeeds add it to the list in the panel """
            self.panel.addItemToSelectionList( prtobject.name, prtobject.objType )
        self.prtObjects += [prtobject]
    
        self.objectNr += 1
    
    def addClusterObject(self, clsObject):
        if clsObject != None:
            self.clsObjects += [clsObject]
    
    def addTransparentObject( self, prtobject ):
        self.transpPrtObjects += [prtobject]
        self.objectNr += 1
    
    def __handleResult(self):
        """ Create the clusterobjects for the sketcher """
        if self.result != None:
            collPoints = []
            clusters = []
            #self.result.flag = GeometricCluster.S_OVER
            if self.result.flag == GeometricCluster.I_UNDER or self.result.flag == GeometricCluster.S_UNDER:
                clusters = self.result.subs
                for cluster in clusters:
                    self.__createCluster(cluster)
            elif self.result.flag == GeometricCluster.I_OVER or self.result.flag == GeometricCluster.S_OVER:
                self.__getOverConstrainedClusters(self.result, clusters)
                wellClusters = []                
                self.__getWellConstrainedClusters(self.result, wellClusters, 1)
                for cluster in clusters:
                    self.__createCluster(cluster)
                for wellCluster in wellClusters:
                    self.__createCluster(wellCluster)
            elif self.result.flag == GeometricCluster.OK:
                cluster = self.result
                self.__createCluster(cluster)

    def __createCluster(self, cluster):
        collPoints = []
        if len(cluster.variables) > 2:
            ptObjects = filter(lambda x: x.key in cluster.variables, self.prtObjects)
            prtCluster = ClusterI(cluster.flag)
            prtCluster.clusterPoints = ptObjects
            prtCluster.update()
            self.clsObjects += [prtCluster]
        elif len(cluster.variables) == 2:
            collPoints = filter(lambda x: x.key in cluster.variables, self.prtObjects)
            if len(collPoints) == 2:
                prtCluster = DistanceCluster(collPoints[0], collPoints[1])
                prtCluster.update()
                self.clsObjects += [prtCluster]
        elif len(cluster.variables) == 1:
            collPoints = filter(lambda x: x.key in cluster.variables, self.prtObjects)
            prtCluster = PointCluster(collPoints[0].position, collPoints[0].radius*1.5, collPoints[0])
            self.clsObjects += [prtCluster]
                
    def createCluster(self, variables, constrainedness = None):
        """ Clusters are created from a list of variables """
        prtCluster = None
        if len(variables) == 1:
            point = filter(lambda x: x.key in variables, self.prtObjects)
            if point != []:
                prtCluster = PointCluster(point[0].position, point[0].radius*1.5, point[0])
        elif len(variables) == 2:
            collPoints = filter(lambda x: x.key in variables, self.prtObjects)
            if collPoints != []:
                prtCluster = DistanceCluster(collPoints[0], collPoints[1])
        elif len(variables) > 2:
            prtCluster = ClusterI(constrainedness)
            ptObjects = filter(lambda x: x.key in variables, self.prtObjects)
            if ptObjects != []:
                prtCluster.clusterPoints = ptObjects
            else:
                prtCluster = None
        
        if prtCluster != None:
            prtCluster.update()
            self.clsObjects += [prtCluster]
        return prtCluster
                        
    def __getOverConstrainedClusters(self,parent, ocClusters):
        """ Get the highest cluster levels in the tree where overconstrainedness occurs.
        This is a recursive function to receive the highest level overconstrained clusters.
        
        Parameters:
            parent - parent node
            ocClusters - overconstrained clusters
        
        Return:
            level - highest level overconstrained clusters
        """
        overconstrainedFound = False
        for cluster in parent.subs:
            if cluster.flag == GeometricCluster.I_OVER or cluster.flag == GeometricCluster.S_OVER:
                self.__getOverConstrainedClusters(cluster, ocClusters)
                overconstrainedFound = True
        
        if not overconstrainedFound:
            ocClusters += [parent]

    def __getWellConstrainedClusters(self, parent, wellClusters, level=0, currentLevel=0):
        if level == 0:
            return
            
        currentLevel += 1    
        for cluster in parent.subs:
            if currentLevel != level:
                self.__getWellConstrainedClusters(cluster, wellClusters, level, currentLevel)
            elif cluster.flag == GeometricCluster.OK:
                wellClusters += [cluster]
    
    def getMergedConstraints(self, prtObj, withPrtObj):
        """ Merge two points, with its constraints. Constraints which will merge or needs to be deleted, are returned.
        
        Parameters:
            prtObj - the point which needs to be merged with the withPrtObj
            withPrtObj - the point which is merged with
        
        Return:
            list - list of merged or deleted constraints """
          
        mergedDConstraints = []
        mergedAConstraints = []
        
        """ Filter all the distance constraints and distance helpers where the from and with objects
        are represented in. The objects are first filtered, to minimize the comparison between the
        constraints. """
        dConstraints = filter(lambda x:(x.objType == ObjectType.DISTANCE_CONSTRAINT or x.objType == ObjectType.DISTANCE_HELPER) and (x.pointBegin == prtObj or x.pointEnd == prtObj or x.pointBegin == withPrtObj or x.pointEnd == withPrtObj), self.prtObjects)
        
        """ Now the constraints are filtered they need to be checked whether they have points in common. When this is 
        the case and both of the constraints consist out of one of the parameters, then they should be
        merged. """
        for dConstraint in dConstraints:
            for dConstraint2 in dConstraints:
                if ((dConstraint.pointBegin == dConstraint2.pointBegin or dConstraint.pointEnd == dConstraint2.pointEnd) or \
                    (dConstraint.pointEnd == dConstraint2.pointBegin or dConstraint.pointBegin == dConstraint2.pointEnd)) and \
                    (dConstraint.pointBegin == prtObj or dConstraint.pointEnd == prtObj) and \
                    (dConstraint2.pointBegin == withPrtObj or dConstraint2.pointEnd == withPrtObj):
                    mergedDConstraints += [dConstraint]
                    break
        
        #mergedDConstraints = self.__getMergedDistanceConstraints(mergedDConstraints, prtObj, withPrtObj)
        
        """ Handling the angle constraint is similar to the distance constraint, only it needs to be
        extended because the angle consists of 3 points instead of 2. """
        aConstraints = filter(lambda x:x.objType == ObjectType.ANGLE_CONSTRAINT and (x.pointBegin == prtObj or x.pointMiddle == prtObj or x.pointEnd == prtObj or x.pointBegin == withPrtObj or x.pointMiddle == withPrtObj or x.pointEnd == withPrtObj), self.prtObjects)
        for aConstraint in aConstraints:
            for aConstraint2 in aConstraints:
                if ((aConstraint.pointBegin == aConstraint2.pointBegin or aConstraint.pointMiddle == aConstraint2.pointMiddle or aConstraint.pointEnd == aConstraint2.pointEnd) or \
                    (aConstraint.pointBegin == aConstraint2.pointMiddle or aConstraint.pointBegin == aConstraint2.pointEnd) or \
                    (aConstraint.pointMiddle == aConstraint2.pointBegin or aConstraint.pointMiddle == aConstraint2.pointEnd) or \
                    (aConstraint.pointEnd == aConstraint2.pointBegin or aConstraint.pointEnd == aConstraint2.pointMiddle)) and \
                    (aConstraint.pointBegin == prtObj or aConstraint.pointMiddle == prtObj or aConstraint.pointEnd == prtObj) and \
                    (aConstraint2.pointBegin == withPrtObj or aConstraint2.pointMiddle == withPrtObj or aConstraint2.pointEnd == withPrtObj):
                    mergedAConstraints += [aConstraint]
                    break
        
        #mergedAConstraints = self.__getMergedAngleConstraints(mergedAConstraints, prtObj, withPrtObj)
                
        mergedConstraints = mergedAConstraints + mergedDConstraints
        
        return mergedConstraints
                
    def __getMergedDistanceConstraints(self,mergedDistanceConstraints, prtObj, withPrtObj):
        deleteConstraints = []
        dConstraints = filter(lambda x:((x.objType == ObjectType.DISTANCE_CONSTRAINT or x.objType == ObjectType.DISTANCE_HELPER) and (x.pointBegin == withPrtObj or x.pointEnd == withPrtObj)), self.prtObjects)

        for mConstraint in mergedDistanceConstraints:
            for dConstraint in dConstraints:
                if (mConstraint.pointBegin == dConstraint.pointBegin and mConstraint.pointEnd == dConstraint.pointEnd) or \
                      (mConstraint.pointBegin == dConstraint.pointEnd and mConstraint.pointEnd == dConstraint.pointBegin):
                    deleteConstraints += [mConstraint]
                    break

        return deleteConstraints
                   
    def __getMergedAngleConstraints(self,mergedAngleConstraints, prtObj, withPrtObj):
        deleteConstraints = []
        aConstraints = filter(lambda x:((x.objType == ObjectType.ANGLE_CONSTRAINT) and (x.pointBegin == withPrtObj or x.pointMiddle == withPrtObj or x.pointEnd == withPrtObj)), self.prtObjects)

        for mConstraint in mergedAngleConstraints:
            for aConstraint in aConstraints:
                if (mConstraint.pointBegin == aConstraint.pointBegin and mConstraint.pointMiddle == aConstraint.pointMiddle and mConstraint.pointEnd == aConstraint.pointEnd) or \
                   (mConstraint.pointBegin == aConstraint.pointBegin and mConstraint.pointMiddle == aConstraint.pointEnd and mConstraint.pointEnd == aConstraint.pointMiddle) or \
                   (mConstraint.pointBegin == aConstraint.pointMiddle and mConstraint.pointMiddle == aConstraint.pointBegin and mConstraint.pointEnd == aConstraint.pointEnd) or \
                   (mConstraint.pointBegin == aConstraint.pointMiddle and mConstraint.pointMiddle == aConstraint.pointEnd and mConstraint.pointEnd == aConstraint.pointMiddle) or \
                   (mConstraint.pointBegin == aConstraint.pointEnd and mConstraint.pointMiddle == aConstraint.pointBegin and mConstraint.pointEnd == aConstraint.pointMiddle) or \
                      (mConstraint.pointBegin == aConstraint.pointEnd and mConstraint.pointMiddle == aConstraint.pointMiddle and mConstraint.pointEnd == aConstraint.pointBegin):
                    deleteConstraints += [mConstraint]
                    break

        return deleteConstraints
    
    def getConstraintInfoAsText(self):
        if self.result != None:
            if self.result.flag == GeometricCluster.I_UNDER:
                return "Incidentally Underconstrained (change distance/angle values)"
            elif self.result.flag == GeometricCluster.S_UNDER:
                return "Structurally Underconstrained (assign more distances/angles)"
            elif self.result.flag == GeometricCluster.I_OVER:
                return "Incidentally Overconstrained (change distance/angle values)"
            elif self.result.flag == GeometricCluster.S_OVER:
                return "Structurally Overconstrained (remove distances/angles)"
            elif self.result.flag == GeometricCluster.OK:
                return "Well Constrained"
            else:
                return ""
        else:
            return ""
                
    def removeAllObjects(self):
        """ Removing all of the objects in the scene. """
        self.removeObjects(self.prtObjects)
        self.removeAllClusters()
        self.objectNr = 1
    
    def removeAllClusters(self):
        self.removeClusterObjects(self.clsObjects)
        
    def removeObjects( self, objects ):
        """ Removing the objects from the list. The objects are also removed from the
            constraint graph. The order of removal is important. 
        
        Parameters:    
            objects - objects that are to be removed
        """
        for obj in objects:
            if obj.objType == ObjectType.ANGLE_CONSTRAINT and not obj.ghost:
                obj.con = self.geoProblem.get_angle( obj.pointBegin.key, obj.pointMiddle.key, obj.pointEnd.key )
                self.geoProblem.rem_constraint( obj.con )
        #print "removal of Angles succeeded """ 
        for obj in objects:
            if obj.objType == ObjectType.DISTANCE_CONSTRAINT and not obj.ghost:
                #print " distance constr keys: ", obj.pointBegin.key, obj.pointEnd.key
                obj.con = self.geoProblem.get_distance( obj.pointBegin.key, obj.pointEnd.key )
                #print " got it "
                self.geoProblem.rem_constraint( obj.con )
        #print "removal of Distance Constraints succeeded """ 
        for obj in objects:
            if obj.objType == ObjectType.POINT and not obj.ghost:
                self.geoProblem.rem_point( obj.key )
        
        for obj in objects:
            if obj.objType == ObjectType.FIXED_POINT and not obj.ghost:
                self.geoProblem.rem_constraint( self.geoProblem.get_fix( obj.key ) )
        #print "removal of Fixed points succeeded """ 
        self.panel.removeItems( map( lambda x:x.name, objects ) )
        self.prtObjects = filter( lambda x:x not in objects, self.prtObjects ) 
        #print "removal of All other succeeded """ 
    
    def removeClusterObjects(self, clsObjects, removeOnlyTemp=False, removeFixed=False):
        if removeOnlyTemp and removeFixed:    
            self.clsObjects =  filter(lambda x:x not in clsObjects or (not x.temporary or not x.fixed), self.clsObjects)
        elif removeOnlyTemp:
            self.clsObjects =  filter(lambda x:x not in clsObjects or not x.temporary, self.clsObjects)
        else:
            self.clsObjects =  filter(lambda x:x not in clsObjects, self.clsObjects)
            
    def deleteObject( self, removeObject ):
        """ Delete the object from the list of prototypes. If other objects are dependent on the deleted object, then
        they will be removed too. 
        
        Paramaters:
            removeObject - remove the object from the list of prototype objects.
        """
        
        dellist = []
        for prtObject in self.prtObjects:
            if prtObject.objType == ObjectType.ANGLE_CONSTRAINT:
                if prtObject.pointBegin == removeObject or prtObject.pointMiddle == removeObject or prtObject.pointEnd == removeObject:
                    dellist += [prtObject]
            
            if prtObject.objType == ObjectType.DISTANCE_CONSTRAINT or prtObject.objType == ObjectType.DISTANCE_HELPER:
                if prtObject.pointBegin == removeObject or prtObject.pointEnd == removeObject:
                    dellist += [prtObject]
        dellist += [removeObject]
        self.removeObjects( dellist )
    
    def deleteSelectedObjects(self):
        selectedObjects = self.getSelectedObjects()
        for selObj in selectedObjects:
            exists = filter(lambda x:x==selObj, self.prtObjects)
            if len(exists) > 0:
                self.deleteObject(selObj)
    
    def getSelectedObjects(self):
        return filter(lambda x:x.selected, self.prtObjects)
                   
    def updateObjects( self ):
        """ Update all the objects, this might also be a ghost object (object that does not really exist, but is visualised). """
        for prtObject in self.prtObjects:
            prtObject.update()
            if prtObject.objType == ObjectType.POINT and not prtObject.ghost:
                pointPosition = self.geoProblem.get_point( prtObject.key )
                pointPosition[0] = prtObject.position[0]
                pointPosition[1] = prtObject.position[1]
                pointPosition[2] = prtObject.position[2]
            elif prtObject.objType == ObjectType.DISTANCE_CONSTRAINT and not prtObject.ghost:
                if prtObject.distance != None:
                    self.updateConstraint(prtObject, prtObject.distance)
            elif prtObject.objType == ObjectType.ANGLE_CONSTRAINT and not prtObject.ghost:
                if prtObject.angle != None:
                    self.updateConstraint(prtObject, prtObject.angle)

        for transpPrtObject in self.transpPrtObjects:
            transpPrtObject.update()
    
    def updateConstraint( self, obj, value ):
        """ Update an existing constraint, with a new value. This value is also passed to the constraint graph.
            
        Parameters:
            obj - prototype object which needs to be updated.
            value - the new value for the object.
        """
        if obj.objType == ObjectType.DISTANCE_CONSTRAINT:
            obj.distance = value
            dConstraint = self.geoProblem.get_distance( obj.pointBegin.key, obj.pointEnd.key )
            if dConstraint != None:
                dConstraint._value = obj.distance
    
        elif obj.objType == ObjectType.ANGLE_CONSTRAINT:
            obj.angle = value
            dAngle = self.geoProblem.get_angle( obj.pointBegin.key, obj.pointMiddle.key, obj.pointEnd.key )
            if dAngle != None:
                dAngle._value = math.radians(obj.angle)
                
    def updateConstraintKeys(self, oldKey, newKey):
        """ Update the keyvalues of a constraint. To update a key value, the constraints
        must first be found which have the old key. Once found it must be replaced with the
        new one. The constraint with the old key is therefore first to be removed from the graph 
        and then to be added again with the new key.
        
        Parameters:
            oldKey - the old key of the constraint, used for lookup of the constraints
            newKey - the new key which has to be set for the constraints """
        
        for prtObj in self.prtObjects:
            if prtObj.objType == ObjectType.DISTANCE_CONSTRAINT:
                if prtObj.pointBegin.key == oldKey or prtObj.pointEnd.key == oldKey:
                    dConstraint = self.geoProblem.get_distance(prtObj.pointBegin.key, prtObj.pointEnd.key)
                    if dConstraint != None:
                        self.geoProblem.rem_constraint(dConstraint)
                        if prtObj.pointBegin.key == oldKey:
                            prtObj.con = geosolver.DistanceConstraint( newKey, prtObj.pointEnd.key, prtObj.distance )
                        elif prtObj.pointEnd.key == oldKey:
                            prtObj.con = geosolver.DistanceConstraint( prtObj.pointBegin.key, newKey, prtObj.distance )
                        self.geoProblem.add_constraint(prtObj.con)

            elif prtObj.objType == ObjectType.ANGLE_CONSTRAINT:
                if prtObj.pointBegin.key == oldKey or prtObj.pointMiddle.key == oldKey or prtObj.pointEnd.key == oldKey:
                    aConstraint = self.geoProblem.get_angle(prtObj.pointBegin.key, prtObj.pointMiddle.key, prtObj.pointEnd.key)
                    self.geoProblem.rem_constraint(aConstraint)
                    if aConstraint != None:
                        if prtObj.pointBegin.key == oldKey:
                            prtObj.con = geosolver.AngleConstraint( newKey, prtObj.pointMiddle.key, prtObj.pointEnd.key, prtObj.angle )
                        elif prtObj.pointMiddle.key == oldKey:
                            prtObj.con = geosolver.AngleConstraint( prtObj.pointBegin.key, newKey, prtObj.pointEnd.key, prtObj.angle )
                        elif prtObj.pointEnd.key == oldKey:
                            prtObj.con = geosolver.AngleConstraint( prtObj.pointBegin.key, prtObj.pointMiddle.key, newKey, prtObj.angle )
                        self.geoProblem.add_constraint(prtObj.con)
                                
    def getImportedObjsByKey(self, key):
        for impObj in self.importedObjs:
            if (impObj.objType == ObjectType.POINT or impObj.objType == ObjectType.FIXED_POINT) and impObj.importKey == key:
                return impObj
    
    def addConstraint( self, obj ):
        """ Add a constraint to an existing object.
        
        Parameters:
            obj - object for which the constraint must be added.
        """
        if obj.objType == ObjectType.POINT:
            self.geoProblem.add_constraint( geosolver.FixConstraint( obj.key, Vec( [obj.position[0], obj.position[1], obj.position[2]] ) ) )
            newObj = FixedPoint( obj.key, obj.position, obj.radius )
            self.replaceObject( obj, newObj )
    
    def removeConstraint( self, obj ):
        """ Remove a constraint from an existing object.
        
        Parameters:
            obj - object from which the constraint must be removed.
        """
        if obj.objType == ObjectType.FIXED_POINT:
            self.geoProblem.rem_constraint( self.geoProblem.get_fix( obj.key ) )
            newObj = Point( obj.key, obj.position, obj.radius )
            self.replaceObject( obj, newObj )
    
    def replaceObject( self, oldObj, newObj ):
        """ Replace object, when a constraint is added to an existing object it is replaced with a new type of object.
        Because of this a new instance is created, which is not known by other prototype objects, so al the references 
        must be set correct. 
        
        Parameters:
            oldObj - old object where some objects may reference to.
            newObj - new object where must be referenced to.
        """
        for prtObject in self.prtObjects:
            prtObject.setNewReference( oldObj, newObj )
    
        if self.objectSelected == oldObj:
            self.objectSelected = newObj
    
        self.prtObjects = filter( lambda x:x is not oldObj, self.prtObjects )
        self.prtObjects += [newObj]
        
    def replaceConstrainedObject( self, oldCstrObj, newCstrObj ):
        """ Replace object, when a constraint is added to an existing object it is replaced with a new type of object.
        Because of this a new instance is created, which is not known by other prototype objects, so al the references 
        must be set correct. 
        
        Parameters:
            oldCstrObj - old object where some objects may reference to.
            newCstrObj - new object where must be referenced to.
        """
        mergedConstraints = self.getMergedConstraints(oldCstrObj, newCstrObj)
        self.removeObjects(mergedConstraints)
        self.updateConstraintKeys(oldCstrObj.key, newCstrObj.key)
        for prtObject in self.prtObjects:
            prtObject.setNewReference( oldCstrObj, newCstrObj )
            
        if self.objectSelected == oldCstrObj:
            self.objectSelected = newCstrObj
    
        self.prtObjects = filter( lambda x:x is not oldCstrObj, self.prtObjects )
        self.removeObjects([oldCstrObj])
        
    def deselectObject( self ):
        """ Deselect the selected object, which is selected """
        if self.objectSelected != None:
            self.objectSelected.selected = False
        self.objectSelected = None
        self.axis.selected = -1
        self.showAxis = False
        self.panel.updateEdit()     
    
    def deselectAllObjects(self, dsClObjects=True, onlyTemp=False):
        """ Deselect all of the objects. """
        
        for prtObject in self.prtObjects:
            if onlyTemp:
                if prtObject.temporarySelected:
                    prtObject.selected = False
                    prtObject.temporarySelected = False
            else:
                prtObject.selected = False
        
        if dsClObjects:
            for clsObject in self.clsObjects:
                clsObject.selected = False
         
    def drawObjects( self ):
        """ Draw all of the objects. """
        for prtObject in self.prtObjects:
            if prtObject.selected and prtObject.showAxis and self.showAxis:
                self.axis.draw()
            if prtObject.isVisible:
                prtObject.draw()
        if self.visualiseClusters:
            for clsObject in self.clsObjects:
                if clsObject.isVisible:
                    clsObject.draw()
     
    def drawTransparentObjects( self ):
        """ Draw the transparent objects. (Obsolete) """
        for transpPrtObject in self.transpPrtObjects:
            if transpPrtObject.selected and transpPrtObject.showAxis and self.showAxis:
                self.axis.draw()
            transpPrtObject.draw()
            
    def drawWithPicking( self ):
        """ Draw objects with picking, so they can be selected with the mouse. This is done by setting an unique id for
        every object. """
        self.selectCounter=0
        for prtObject in self.prtObjects:
            if not prtObject.ghost:
                glPushName( self.selectCounter )
                prtObject.selectionId = self.selectCounter
                if prtObject.selected:
                    self.axis.drawWithPicking()
                prtObject.draw()
                glPopName()
                self.selectCounter += 1

    def drawTransparentWithPicking( self ):
        """ Draw transparent objects with picking, so they can be selected with the mouse. This is done by setting 
        an unique id for every object. """
        for transpPrtObject in self.transpPrtObjects:
            glPushName( self.selectCounter )
            transpPrtObject.selectionId = self.selectCounter
            if transpPrtObject.selected:
                self.axis.drawWithPicking()
            transpPrtObject.draw()
            glPopName()
            self.selectCounter += 1
    
    def setVisibilityOfObjects(self, visible=True):
        for prtObject in self.prtObjects:
            prtObject.isVisible = visible
        for clsObject in self.clsObjects:
            clsObject.isVisible = visible
    
    def setObjectVisibilityByClusters(self):
        self.setVisibilityOfObjects(False)
        found = False
        for clsObject in self.clsObjects:
            if clsObject.fixed == True:
                found = True
                if clsObject.objType == ObjectType.POINT:
                    points = filter(lambda x:(x.objType == ObjectType.POINT or x.objType == ObjectType.FIXED_POINT) and clsObject.relPoint==x, self.prtObjects)
                    for point in points:
                        point.isVisible = True
                elif clsObject.objType == ObjectType.DISTANCE_HELPER:
                    distances = filter(lambda x:(x.objType == ObjectType.DISTANCE_CONSTRAINT or x.objType == ObjectType.DISTANCE_HELPER) and ((clsObject.pointBegin==x.pointBegin and clsObject.pointEnd == x.pointEnd) or (clsObject.pointBegin==x.pointEnd and clsObject.pointEnd == x.pointBegin)), self.prtObjects)
                    for distance in distances:
                        distance.isVisible = True
                        distance.pointBegin.isVisible = True
                        distance.pointEnd.isVisible = True
                elif clsObject.objType == ObjectType.CLUSTER:
                    for point in clsObject.getClusterPoints():
                        pointObjs = filter(lambda x:(x.objType == ObjectType.POINT or x.objType == ObjectType.FIXED_POINT) and x == point,self.prtObjects)
                        for pointObj in pointObjs:
                            pointObj.isVisible = True
                                            
                    distances = filter(lambda x:x.objType == ObjectType.DISTANCE_CONSTRAINT or x.objType == ObjectType.DISTANCE_HELPER, self.prtObjects)
                    for distance in distances:
                        pBegin = filter(lambda x:x == distance.pointBegin, clsObject.getClusterPoints())
                        pEnd = filter(lambda x:x == distance.pointEnd, clsObject.getClusterPoints())
                        if len(pBegin) > 0 and len(pEnd) > 0:
                            distance.isVisible = True
                    
                    angles = filter(lambda x:x.objType == ObjectType.ANGLE_CONSTRAINT, self.prtObjects)
                    for angle in angles:
                        pBegin = filter(lambda x:x == angle.pointBegin, clsObject.getClusterPoints())
                        pMiddle = filter(lambda x:x == angle.pointMiddle, clsObject.getClusterPoints())
                        pEnd = filter(lambda x:x == angle.pointEnd, clsObject.getClusterPoints())
                        if len(pBegin) > 0 and len(pMiddle) > 0 and len(pEnd) > 0:
                            angle.isVisible = True
        for clsObject in self.clsObjects:
            if clsObject.fixed == True:
                clsObject.isVisible = True
        if not found:
            self.setVisibilityOfObjects(True)

    def isObjectSelected( self ):
        """ Check whether an object is selected. """
        return self.objectIsSelected
        
    def setObjectSelected( self, selected ):
        """ Set whether the object is selected. 
        
        Parameters:
            selected - whether the selected object is activated or not.
        """
        self.objectIsSelected = selected
    
    def selectObjectByName( self, name ):
        """ Select an object by name. This name is NOT the key of an object, but the name which is filled in by
        the user in the control panel. 
        
        Parameters:
            name - the name of the object which must be selected
        """
        for prtObject in self.prtObjects:
            if prtObject.name == name: 
                self.deselectObject()
                self.objectSelected = prtObject
                self.objectSelected.selected = True
                break

    def selectObject(self, obj):
        """ Select the given object.
        
        Parameters:
            obj - select this object.
        """
        self.deselectObject()
        self.objectSelected = obj
        self.objectSelected.selected = True
        self.panel.selectItemByName( obj.name )

    def selectObjectsByKeys(self, variables):
        """ Select multiple objects by their keys. These are unique and are the same as the keys in the solver. 
        
        Parameters:
            variables - keys which needs to be selected
        """
        #self.deselectAllObjects()
        for prtobject in self.prtObjects:
            keyfound = filter( lambda x:x == prtobject.key, variables ) 
            if keyfound:
                 prtobject.selected = True
    
    def selectClusterObjectByKeys(self, variables):
        """ Get a clusterObject based on the keys given
        
        Parameters:
            variables - key that must be part of the clusterobject
        """ 
        for clsObject in self.clsObjects:
            clsPoints = clsObject.getClusterPoints()
            if len(variables) == len(clsPoints):
                variablesInCluster = True
                for variable in variables:
                    if len(filter(lambda x:x.key == variable, clsPoints)) == 0:
                        variablesInCluster = False
                        break
                if variablesInCluster:
                    return clsObject
        return None
            
                     
    def getObjectByKey( self, key ):
        """ Get an object by its unique key.
        
        Parameters:
            key - key of an object
        """
        for prtObject in self.prtObjects:
            if prtObject.key == key:
                return prtObject
        return None
    
    def setSelectedObject( self, selectionId, bOnlySelect=False, bDeselectSelected = True ):
        """ Set a selected object, by the selection id obtained from OpenGL. 
            
            Parameters:
                selectionId - the selection id, which is the object that the user has chosen.
                bOnlySelect - if it must only be highlighted, but further actions are not allowed.
        """
        found = False
        for prtObject in self.prtObjects:
            if bDeselectSelected:
                prtObject.selected = False

            if prtObject.selectionId == selectionId[0][0] and not prtObject.ghost:
                found = True
                prtObject.selected = True
                if not bOnlySelect:
                    self.objectSelected = prtObject
                elif prtObject.isMovable:
                    prtObject.selected = False
                self.panel.updateSelection = False
                self.panel.selectItemByName( prtObject.name )
                self.panel.updateSelection = True
                
        if not found:
            for transPrtObject in self.transpPrtObjects:
                transPrtObject.selected = False
                if transPrtObject.selectionId == selectionId[0][0]:
                    found = True
                    transPrtObject.selected = True
                    if not bOnlySelect:
                        self.objectSelected = transPrtObject    
                    elif prtObject.isMovable:
                        prtObject.selected = False
    
    def changeSelection(self, selectionId):
        for prtObject in self.prtObjects:
            found = False
            if prtObject.selectionId == selectionId[0][0]:
                if prtObject.selected:
                    prtObject.selected = False
                else:
                    prtObject.selected = True
                found = True
                break   
    
    def setSelectedObjects( self, selectionIds, deselectObjects=True, temporarySel=False ): 
        for prtObject in self.prtObjects:
            found = False
            for selectionId in selectionIds:
                if prtObject.selectionId == selectionId[0]:
                    prtObject.selected = True
                    if temporarySel:
                        prtObject.temporarySelected = True
                    found = True
                    break
            if not found and deselectObjects:
                prtObject.selected = False
    
    def convertTemporySelection(self):
        for prtObject in self.prtObjects:            
            if prtObject.temporarySelected:
                prtObject.temporarySelected = False
                
    def setPanel( self, panel ):
        """ Set the panel in the main window for access, for updating information 
        
        Parameters:
            panel - panel from the main window.
        
        """
        self.panel = panel
    
    def isNameUnique( self, oldName, newName ):
        """ Check whether the name given by the user is unique. 
        
        Parameters:
            oldName - the old name for the object.
            newName - the new name for the object.
        
        Return:
            boolean - whether the name is unique or not.
        """
        for prtObject in self.prtObjects:
            if prtObject.name == newName and newName != oldName:
                return False
        return True
    
    def setObjectName( self, oldName, newName ):
        """ Set a new name for an object. 
        
        Parameters:    
            oldName - old name of an object for comparison
            newName - new name for an object
        """
        for prtObject in self.prtObjects:
            if prtObject.name == oldName:
                prtObject.name = newName
                return True
        return False
       
    def showClusters(self):
           if self.visualiseClusters:
               self.visualiseClusters = False
           else:
               self.visualiseClusters = True
       
    def getParameterRange(self, prtObject):
        if self.result != None:
            if self.result.flag == GeometricCluster.OK  and prtObject.parameterRange == []:
                if prtObject.objType == ObjectType.DISTANCE_CONSTRAINT:
                    dConstraint = self.geoProblem.get_distance(prtObject.pointBegin.key, prtObject.pointEnd.key)
                    prtObject.parameterRange = geosolver.prange.sample_prange(self.geoProblem, dConstraint, 0.0, prtObject.distance+100.0,0.5)
                elif prtObject.objType == ObjectType.ANGLE_CONSTRAINT:
                    aConstraint = self.geoProblem.get_angle(prtObject.pointBegin.key, prtObject.pointMiddle.key, prtObject.pointEnd.key)
                    prtObject.parameterRange = geosolver.prange.sample_prange(self.geoProblem, aConstraint, 0.0, 360.0,0.1)
                return prtObject.parameterRange
            elif self.result.flag == GeometricCluster.OK and prtObject.parameterRange != []:
                return prtObject.parameterRange
        return []
       
    def resetParameterRange(self):
           for prtObj in self.prtObjects:
               if prtObj.objType == ObjectType.DISTANCE_CONSTRAINT or prtObj.objType == ObjectType.ANGLE_CONSTRAINT:
                    prtObj.parameterRange = []
                   
    def solve( self ):
        """ Solve the system of GCS. If there is a solution, then this is provided in the Solution View. The decomposition
        is shown in the Decomposition View. """
        print self.geoProblem
        self.removeAllClusters()
        self.resetParameterRange()
        self.setVisibilityOfObjects(True)
        geoSolver = geosolver.GeometricSolver( self.geoProblem )
        self.result = geoSolver.get_result()
        self.__handleResult()
        # 20090521 - geoSolver is deleted in this context, but it is not deleted because geoProblem refers to it via Listener interface
        # 20090521 - now fixed this bug
        print self.result
        print "solve finished"
    
    def save(self, domDocument ):
        pointNode = QtXml.QDomElement( domDocument.createElement( "Prototypes" ) )
        pointNode.setAttribute( "number", self.objectNr )
        pointNode.setAttribute( "numberOfImports", self.nrOfImports )
        return pointNode
    
    def load( self, domElements ):
        """ Load the objects from a XML file.
        
        Parameters: 
            domElements: different saved objects.
        """
        elements = domElements.firstChild()
        while not elements.isNull():
            element = elements.toElement()
            if not element.isNull():
                prtObject = None
                if element.tagName() == "Point":
                    prtObject = Point("", Vec([0.0, 0.0, 0.0]), 5.0)
                elif element.tagName() == "FixedPoint":
                    prtObject = FixedPoint("", Vec([0.0, 0.0, 0.0]), 5.0)
                elif element.tagName() == "AngleConstraint":
                    prtObject = AngleConstraint("", None, None, None)
                elif element.tagName() == "Distance":
                    prtObject = Distance("", None, None)
                elif element.tagName() == "DistanceConstraint":
                    prtObject = DistanceConstraint("", None, None)
                elif element.tagName() == "Prototypes":
                    self.setObjectNumber(element)
                else:
                    raise StandardError, "Unable to load unkown object", element.tagName()                

                if prtObject != None:                                
                    prtObject.load(element)
                    self.addObject(prtObject)

            elements = elements.nextSibling()    
        self.updateObjects()
    
    def importScene(self, domElements):
        """ Import the objects from a XML file.
        
        Parameters: 
            domElements: different saved objects.
        """
        elements = domElements.firstChild()
        while not elements.isNull():
            element = elements.toElement()
            if not element.isNull():
                prtObject = None
                if element.tagName() == "Point":
                    prtObject = Point("", Vec([0.0, 0.0, 0.0]), 5.0)
                elif element.tagName() == "FixedPoint":
                    prtObject = FixedPoint("", Vec([0.0, 0.0, 0.0]), 5.0)
                elif element.tagName() == "AngleConstraint":
                    prtObject = AngleConstraint("", None, None, None)
                elif element.tagName() == "Distance":
                    prtObject = Distance("", None, None)
                elif element.tagName() == "DistanceConstraint":
                    prtObject = DistanceConstraint("", None, None)
                else:
                    raise StandardError, "Unable to import unkown object", element.tagName()                

                if prtObject != None:                                
                    prtObject.importItem(element, self.nrOfImports, self.objectNr )
                    self.importedObjs += [prtObject]
                    self.addObject(prtObject)

            elements = elements.nextSibling()    
        self.updateObjects()
        self.nrOfImports += 1
        self.importedObjs = []

    # Rick 20090522
    def setProblem(self, problem):
        """ Import the objects from a GeometricProblem.
        
        Parameters: 
           problem: a GeometricProblem instance
        """
        # remove all objects first
        # self.removeAllObjects()
        # add point variabels and store a mapping
        map = {}
        vars = problem.cg.variables();
        for var in vars:
                if problem.has_point(var):
                    prtObject = Point(var, Vec(problem.get_point(var)), 5.0)
                    map[var]=prtObject
                    self.addObject(prtObject)
                else:
                    raise StandardError, "Unable to import non-point variable: "+str(var)
        # add constraints
        constraints = problem.cg.constraints();
        count = 0
        for con in constraints:
                if isinstance(con, geosolver.DistanceConstraint):
                    name = "dist_"+str(con.variables()[0])+"_"+str(con.variables()[1])
                    count += 1
                    prtObject = DistanceConstraint(name,
                        map[con.variables()[0]], 
                        map[con.variables()[1]]
                    )
                    self.addObject(prtObject)
                elif isinstance(con, geosolver.AngleConstraint):
                    name = "angle_"+str(con.variables()[0])+"_"+str(con.variables()[1])+str(con.variables()[2])
                    count += 1
                    prtObject = AngleConstraint(name,
                        map[con.variables()[0]], 
                        map[con.variables()[1]],
                        map[con.variables()[2]]
                    )
                    self.addObject(prtObject)
                else:
                    raise StandardError, "Unable to import constraint: "+str(con)
        # compute object visulisation, etc
        self.updateObjects()


    def setObjectNumber(self, domElement):
        self.objectNr = domElement.attribute("number", "").toInt()[0]
        self.nrOfImports = domElement.attribute("numberOfImports", "").toInt()[0]
        
            
class Object:
    """ The general prototype object class. All objects which must be visualised, or have a connection with the constraint
    solver must be subclassed from the Object class. """
    def __init__( self ):
        self.settings = Settings()
        self.selectionId = 0
        self.selectColor = self.settings.sketcherData.selectColor
        self.selected = False
        self.temporarySelected = False
        self.quadric = gluNewQuadric()
        gluQuadricNormals(self.quadric, GLU_SMOOTH)
        self.ghost = False
        self.showAxis = False
        self.isMovable = False
        self.isVisible = True

    def draw( self ):
        """ A virtual draw function, for drawing the object. """
        raise NotImplementedError( caller + ' must be implemented in subclass' )
    
    def clone( self ):
        """ A virtual clone function, to clone an object. """
        raise NotImplementedError( caller + ' must be implemented in subclass' )
    
    def update( self ):
        """ A virtual update function, to update an object. """
        raise NotImplementedError( caller + ' must be implemented in subclass' )
    
    def setNewReference( self, oldObj, newObj ):
        """ A virtual set new reference function, to dereference an old object and reference to the new one. 
        
        Parameters:
            oldObj - old object which must be dereferenced
            newObj - new object where must be referenced to
        """
        raise NotImplementedError( caller + ' must be implemented in subclass' )
    
    def load(self, domElement):
        """ A virtual load function to load the object from a XML file and set the initial values. 
        
        Parameters:
            domElement - an element which contains information about an object.
        """
        raise NotImplementedError( caller + ' must be implemented in subclass' )
        
    def save( self, domDocument ):
        """ A virtual save function to save the object to a XML file. 
        
        Parameters:
            domDocument - a document where must be saved to.
        """
        raise NotImplementedError( caller + ' must be implemented in subclass' )

    def importItem(self, domElement, nrOfImports=0, objNr=0):
        """ A virtual importItem function to import the object from a XML file into the scene. 
        
        Parameters:
            domElement  - an element which contains information about an object.
            nrOfImports - a number added to the name of the import, to make it unique
            objNr         - total number of objects already in the scene
        """
        raise NotImplementedError( caller + ' must be implemented in subclass' )
    
class Point( Object ):
    def __init__( self, name, position, radius ):
        Object.__init__( self )
        self.name = name
        self.key = name
        self.importKey = name
        self.position = position
        self.radius = self.settings.sketcherData.pointRadius
        self.color = self.settings.sketcherData.pointColor
        self.showAxis = True
        self.objType = ObjectType.POINT
        self.fixed = False
        self.ghost = False
        self.needUpdate = True

    def draw( self ):
        if self.selected:
            glColor3fv( [self.selectColor.redF(),self.selectColor.greenF(), self.selectColor.blueF()])
        else:
            glColor3fv( [self.color.redF(),self.color.greenF(), self.color.blueF()])
        glPushMatrix()

        glTranslatef( self.position[0], self.position[1], self.position[2] )
        gluSphere( self.quadric, self.radius, 10, 10 )
        glPopMatrix()

    def updatePosition( self, translation ):
        self.position[0] += translation[0]
        self.position[1] += translation[1]
        self.position[2] += translation[2]

    def setPosition( self, position ):
        self.position[0] = position[0]
        self.position[1] = position[1]
        self.position[2] = position[2]
   
    def update( self ):
        pass
    
    def setNewReference( self, oldObj, newObj ):
        pass
    
    def clone( self, **attr ):
        obj = deepcopy( self )
        obj.__dict__.update( attr )
        return obj
    
    def setTexture( self, texture ):
        pass

    def load (self, domElement):
        self.key = str(domElement.attribute("key", ""))
        self.name = str(domElement.attribute("name", ""))
        self.position[0] = domElement.attribute("posX", "").toFloat()[0]
        self.position[1] = domElement.attribute("posY", "").toFloat()[0]
        self.position[2] = domElement.attribute("posZ", "").toFloat()[0]

    def importItem(self, domElement, nrOfImports=0, objNr=0):
        self.key = "p" + str(objNr)
        self.importKey = str(domElement.attribute("key", ""))
        self.name = str(domElement.attribute("name", ""))
        self.name += "_" + str(nrOfImports)
        self.position[0] = domElement.attribute("posX", "").toFloat()[0]
        self.position[1] = domElement.attribute("posY", "").toFloat()[0]
        self.position[2] = domElement.attribute("posZ", "").toFloat()[0]

    def save( self, domDocument ):
        pointNode = QtXml.QDomElement( domDocument.createElement( "Point" ) )
        pointNode.setAttribute( "key", self.key )
        pointNode.setAttribute( "name", self.name )
        pointNode.setAttribute( "posX", str(self.position[0]))
        pointNode.setAttribute( "posY", str(self.position[1]) )
        pointNode.setAttribute( "posZ", str(self.position[2]) )
        
        return pointNode

class FixedPoint( Point ):
    def __init__( self, name, position, radius ):
        Point.__init__( self, name, position, radius )
        self.objType = ObjectType.FIXED_POINT
        self.radius = self.settings.sketcherData.fPointRadius
        self.color = self.settings.sketcherData.fPointColor
        
    def draw( self ):
        if self.selected:
            glColor3fv( [self.selectColor.redF(),self.selectColor.greenF(), self.selectColor.blueF()])
        else:
            glColor3fv( [self.color.redF(),self.color.greenF(), self.color.blueF()])
        glPushMatrix()

        glTranslatef( self.position[0], self.position[1], self.position[2] )
        gluSphere( self.quadric, self.radius, 10, 10 )
        glPopMatrix()
    
    def load (self, domElement):
        Point.load(self, domElement)        
        
    def importItem(self, domElement, nrOfImports=0, objNr=0):
        Point.importItem(self, domElement, imported=False, nrOfImports=0, objNr=0)
        self.key = "f" + str(objNr)
        
    def save( self, domDocument ):
        pointNode = QtXml.QDomElement( domDocument.createElement( "FixedPoint" ) )
        pointNode.setAttribute( "key", self.key )
        pointNode.setAttribute( "name", self.name )
        pointNode.setAttribute( "posX", str(self.position[0]) )
        pointNode.setAttribute( "posY", str(self.position[1]) )
        pointNode.setAttribute( "posZ", str(self.position[2]) )
        
        return pointNode   
        
class AngleConstraint( Object ):
    def __init__( self, name, pBegin, pMiddle, pEnd ):
        Object.__init__( self )
        self.pointBegin = pBegin
        self.pointMiddle = pMiddle
        self.pointEnd = pEnd
        self.key = name
        self.name = name
        self.realAngle = 0.0
        self.angle = None
        self.con = None
        self.showAxis = False
        self.objType = ObjectType.ANGLE_CONSTRAINT
        self.color = self.settings.sketcherData.angleColor
        self.height = 25.0
        self.angleDisc = Quaternion()
        self.rotAngleMatrix = Numeric.identity(4)
        self.normVec = Vec([0.0, 0.0, 0.0])
        self.parameterRange=[]
        self.fixed = False
        # rick 20090519
        self.height1 = None
        self.height2 = None
        self.orientation1 = Quaternion()
        self.orientation2 = Quaternion()
        self.radius = 0.0 # self.settings.sketcherData.distanceRadius 
        self.update()

    def draw( self ):
        """ Visualisation of the angle constraint """ 
        
        # first draw disk
        glPushMatrix()
        # Rick 20090519 glMultMatrixd doesn't work properly, see above
        # glMultMatrixd( self.rotAngleMatrix )
        axis = -self.angleDisc.axis()
        angle = self.angleDisc.angle()
        pos = self.pointMiddle.position
        glTranslate(pos[0],pos[1],pos[2])
        glRotate(angle*180/math.pi, axis[0], axis[1], axis[2])

        #glDisable( GL_DEPTH_TEST )
        glEnable ( GL_BLEND )

        if self.selected:
            glColor4fv( [self.selectColor.redF(),self.selectColor.greenF(), self.selectColor.blueF(),self.selectColor.alphaF()])
        else:
            glColor4fv( [self.color.redF(),self.color.greenF(), self.color.blueF(), self.color.alphaF()])
        
        """ Visualisate angle constraint as transparent partial disk """ 
        gluPartialDisk(self.quadric, self.pointMiddle.radius, self.height, 20, 10, 0.0, self.realAngle)
        
        glDisable ( GL_BLEND )
        #glEnable( GL_DEPTH_TEST )
        
        glPopMatrix()
        glPushMatrix()
        self.drawAxis()
        glPopMatrix()
        
        # draw cylinder1
        glPushMatrix()
        if self.selected:
            glColor3fv( [self.selectColor.redF(),self.selectColor.greenF(), self.selectColor.blueF()])
        else:
            glColor3fv( [self.color.redF(),self.color.greenF(), self.color.blueF()])
        
        if self.height1 == 0.0:
            self.height1 = 0.001
            
        if self.radius == 0:
            glBegin(GL_LINES)
            glVertex3f(self.pointBegin.position[0], self.pointBegin.position[1], self.pointBegin.position[2])
            glVertex3f(self.pointMiddle.position[0], self.pointMiddle.position[1], self.pointMiddle.position[2])
            glEnd()
        else:
            #glMultMatrixd( self.rotMatrix )
            # there is either a bug in glMultMatrixd or in Quaternion.getRotationMatrix
            # or maybe it has to do with Numpy -> Numeric transition?
            # now doing it with glTranslate/Rotate
            axis = -self.orientation1.axis()
            angle = self.orientation1.angle()
            pos = self.pointBegin.position
            glTranslate(pos[0],pos[1],pos[2])
            glRotate(angle*180/math.pi, axis[0], axis[1], axis[2])
            #print "gluCylinder ", self.radius, self.radius, self.height, 10, 10
            gluCylinder( self.quadric, float(self.radius), float(self.radius), float(self.height1), 10, 10 )
        
        glPopMatrix()

        # draw cylinder2
        glPushMatrix()
        if self.selected:
            glColor3fv( [self.selectColor.redF(),self.selectColor.greenF(), self.selectColor.blueF()])
        else:
            glColor3fv( [self.color.redF(),self.color.greenF(), self.color.blueF()])
        
        if self.height2 == 0.0:
            self.height2 = 0.001
            
        if self.radius == 0:
            glBegin(GL_LINES)
            glVertex3f(self.pointMiddle.position[0], self.pointMiddle.position[1], self.pointMiddle.position[2])
            glVertex3f(self.pointEnd.position[0], self.pointEnd.position[1], self.pointEnd.position[2])
            glEnd()
        else:
            #glMultMatrixd( self.rotMatrix )
            # there is either a bug in glMultMatrixd or in Quaternion.getRotationMatrix
            # or maybe it has to do with Numpy -> Numeric transition?
            # now doing it with glTranslate/Rotate
            axis = -self.orientation2.axis()
            angle = self.orientation2.angle()
            pos = self.pointMiddle.position
            glTranslate(pos[0],pos[1],pos[2])
            glRotate(angle*180/math.pi, axis[0], axis[1], axis[2])
            #print "gluCylinder ", self.radius, self.radius, self.height, 10, 10
            gluCylinder( self.quadric, float(self.radius), float(self.radius), float(self.height2), 10, 10 )
        
        glPopMatrix()



    def drawAxis( self ):
        pass
        
    def update( self ):
        """ The vector is calculated where to rotate to. This is the up-vector relative
        to the plane where the angle constraint must be visualised """
        # compute transform for cylinder1: height1 and orientation1
        self.height1 = (self.pointBegin.position - self.pointMiddle.position ).norm()
        if self.height1 == 0.0:
            self.height1 = 0.001
        diff = self.pointMiddle.position - self.pointBegin.position
        self.orientation1.fromDirection( Vec( [0.0, 0.0, self.height1] ), diff )
        
        # compute transform for cylinder2: height2 and orientation2
        self.height2 = (self.pointEnd.position - self.pointMiddle.position ).norm()
        if self.height2 == 0.0:
            self.height2 = 0.001
        diff = self.pointEnd.position - self.pointMiddle.position
        self.orientation2.fromDirection( Vec( [0.0, 0.0, self.height2] ), diff )

        # compute transform for disk
        diffToBegin = self.pointBegin.position - self.pointMiddle.position
        diffToEnd = self.pointEnd.position - self.pointMiddle.position
        diffBeginEnd = diffToEnd - diffToBegin

        vMiddlePoint = self.pointMiddle.position - self.pointBegin.position
        vMiddleMiddle = (diffBeginEnd*0.5) - vMiddlePoint
        
        diffBeginEnd.normalize()
        vAngleStart = copy(vMiddleMiddle)
        vMiddleMiddle.normalize()
        if diffToBegin.norm() > 1e10:
            diffToBegin.normalize()
        #else: 
        #    diffToBegin = Vec([1.0,0,0])
        if diffToEnd.norm() > 1e10:
            diffToEnd.normalize()
        #else:
        #    diffToEnd = Vec([0,1,0])
        
        """ Retrieve the up-vector, and rotate based upon this vector and the starting direction """        
        rotateTo = vMiddleMiddle.cross(diffBeginEnd)
        self.angleDisc.fromDirection(Vec( [0.0, 0.0, 1.0] ), rotateTo )

        """ Retrieve the part of the disk that needs to be visualised """
        angleFromTo = Quaternion()
        angleFromTo.fromDirection( diffToBegin, diffToEnd )
        self.realAngle = math.degrees( angleFromTo.angle() )
        
        if not self.ghost and not self.fixed:
            self.angle = self.realAngle
        
        """ Rotate to the location from where to start the visualisation of the partial disk """
        angleStartPartialDisk = Quaternion()
        self.inverseRot = self.angleDisc.inverseRotate(Vec([0.0, 1.0, 0.0]))
        
        if self.angle > 180.0:
            self.realAngle = 360.0-self.realAngle
            angleStartPartialDisk.fromDirection(self.inverseRot, diffToBegin)
        else: 
            angleStartPartialDisk.fromDirection(self.inverseRot, diffToEnd)        
            
        self.angleDisc = self.angleDisc * angleStartPartialDisk
            
        """ Translate the partial disk to the middle point and store the matrix """        
        self.angleDisc.getRotationMatrix( self.rotAngleMatrix )
        self.rotAngleMatrix[3][0] = self.pointMiddle.position[0]
        self.rotAngleMatrix[3][1] = self.pointMiddle.position[1]
        self.rotAngleMatrix[3][2] = self.pointMiddle.position[2]
        self.rotAngleMatrix[3][3] = 1.0 
    
    def setNewReference( self, oldObj, newObj ):
        """ When objects change properties new references must be set """
        if self.pointBegin == oldObj:
            self.pointBegin = newObj
        elif self.pointMiddle == oldObj:
            self.pointMiddle = newObj
        elif self.pointEnd == oldObj:
            self.pointEnd = newObj
                
    def clone( self, **attr ):
        """ Create a copy of this object """
        obj = deepcopy( self )
        obj.__dict__.update( attr )
        return obj   
    
    def load (self, domElement):
        """ Load the angle constraint from the xml-file """
        self.key = str(domElement.attribute("key", ""))
        self.name = str(domElement.attribute("name", ""))
        pBeginKey = str(domElement.attribute("pBeginKey", ""))
        pMiddleKey = str(domElement.attribute("pMiddleKey", ""))
        pEndKey = str(domElement.attribute("pEndKey", ""))
        self.pointBegin = PrototypeManager().getObjectByKey(pBeginKey)
        self.pointMiddle = PrototypeManager().getObjectByKey(pMiddleKey)
        self.pointEnd = PrototypeManager().getObjectByKey(pEndKey)
        self.angle = domElement.attribute("angle", "").toDouble()[0]
        if domElement.attribute("fixed", "") == "True":
            self.fixed = True
        else:
            self.fixed = False    
    
    def importItem(self, domElement, nrOfImports=0, objNr=0):
        self.key = "a" + str(objNr)
        self.importKey = str(domElement.attribute("key", ""))
        self.name = str(domElement.attribute("name", ""))
        self.name += "_" + str(nrOfImports)
        
        pBeginKey = str(domElement.attribute("pBeginKey", ""))
        pMiddleKey = str(domElement.attribute("pMiddleKey", ""))
        pEndKey = str(domElement.attribute("pEndKey", ""))
        self.pointBegin = PrototypeManager().getImportedObjsByKey(pBeginKey)
        self.pointMiddle = PrototypeManager().getImportedObjsByKey(pMiddleKey)
        self.pointEnd = PrototypeManager().getImportedObjsByKey(pEndKey)
        self.angle = domElement.attribute("angle", "").toDouble()[0]
        if domElement.attribute("fixed", "") == "True":
            self.fixed = True
        else:
            self.fixed = False     

    def save( self, domDocument ):
        """ Save the angle constraint to the xml-file """
        angleNode = QtXml.QDomElement( domDocument.createElement( "AngleConstraint" ) )
        angleNode.setAttribute( "pBeginKey", self.pointBegin.key )
        angleNode.setAttribute( "pMiddleKey", self.pointMiddle.key )
        angleNode.setAttribute( "pEndKey", self.pointEnd.key )
        angleNode.setAttribute( "key", self.key )
        angleNode.setAttribute( "name", self.name )
        angleNode.setAttribute( "angle", str(self.angle) )
        angleNode.setAttribute( "fixed", str(self.fixed) )
        
        return angleNode

class Distance( Object ):
    def __init__( self, name, pBegin, pEnd ):
        Object.__init__( self )
        self.pointBegin = pBegin
        self.pointEnd = pEnd
        self.radius = self.settings.sketcherData.lineRadius
        self.name = name
        self.key = name
        self.orientation = Quaternion()
        self.rotMatrix = Numeric.identity(4)
        self.height = 0.1
        self.fixed = False
                
        self.showAxis = False
        self.objType = ObjectType.DISTANCE_HELPER
        self.color = self.settings.sketcherData.lineColor
        if self.pointBegin != None and self.pointEnd != None:
            self.distance = (self.pointBegin.position - self.pointEnd.position ).norm()
        else:
            self.distance = 0.0

    def update( self ):
        self.height = (self.pointBegin.position - self.pointEnd.position ).norm()
        if self.height == 0.0:
            self.height = 0.001
          
        diff = self.pointEnd.position - self.pointBegin.position
        self.orientation.fromDirection( Vec( [0.0, 0.0, self.height] ), diff )
        #print "cylinder orientation:",self.orientation
        #print "axis:",self.orientation.axis(), "angle:", self.orientation.angle()
        self.orientation.getRotationMatrix( self.rotMatrix )
        self.rotMatrix[3][0] = self.pointBegin.position[0]
        self.rotMatrix[3][1] = self.pointBegin.position[1]
        self.rotMatrix[3][2] = self.pointBegin.position[2]
        self.rotMatrix[3][3] = 1.0
        #print "cylinder rotMatix:",self.rotMatrix

    def draw( self ):
        glPushMatrix()
        if self.selected:
            glColor3fv( [self.selectColor.redF(),self.selectColor.greenF(), self.selectColor.blueF()])
        else:
            glColor3fv( [self.color.redF(),self.color.greenF(), self.color.blueF()])
        
        if self.height == 0.0:
            self.height = 0.001
            
        if self.radius == 0:
            glBegin(GL_LINES)
            glVertex3f(self.pointBegin.position[0], self.pointBegin.position[1], self.pointBegin.position[2])
            glVertex3f(self.pointEnd.position[0], self.pointEnd.position[1], self.pointEnd.position[2])
            glEnd()
        else:
            #glMultMatrixd( self.rotMatrix )
            # there is either a bug in glMultMatrixd or in Quaternion.getRotationMatrix
            # or maybe it has to do with Numpy -> Numeric transition?
            # now doing it with glTranslate/Rotate
            axis = -self.orientation.axis()
            angle = self.orientation.angle()
            pos = self.pointBegin.position
            glTranslate(pos[0],pos[1],pos[2])
            glRotate(angle*180/math.pi, axis[0], axis[1], axis[2])
            #print "gluCylinder ", self.radius, self.radius, self.height, 10, 10
            gluCylinder( self.quadric, float(self.radius), float(self.radius), float(self.height), 10, 10 )
        
        glPopMatrix()

    def setNewReference( self, oldObj, newObj ):
        if self.pointBegin == oldObj:
            self.pointBegin = newObj
        elif self.pointEnd == oldObj:
            self.pointEnd = newObj

    def clone( self, **attr ):
        obj = deepcopy( self )
        obj.__dict__.update( attr )
        return obj

    def load (self, domElement):
        self.key = str(domElement.attribute("key", ""))
        self.name = str(domElement.attribute("name", ""))

        pBeginKey = str(domElement.attribute("pBeginKey", ""))
        pEndKey = str(domElement.attribute("pEndKey", ""))
        self.pointBegin = PrototypeManager().getObjectByKey(pBeginKey)
        self.pointEnd = PrototypeManager().getObjectByKey(pEndKey)
        self.distance = domElement.attribute("distance", "").toDouble()[0]

    def importItem(self, domElement, nrOfImports=0, objNr=0):
        self.key = "l" + str(objNr)
        self.importKey = str(domElement.attribute("key", ""))
        self.name = str(domElement.attribute("name", ""))
        self.name += "_" + str(nrOfImports)
        
        pBeginKey = str(domElement.attribute("pBeginKey", ""))
        pEndKey = str(domElement.attribute("pEndKey", ""))
        self.pointBegin = PrototypeManager().getImportedObjsByKey(pBeginKey)
        self.pointEnd = PrototypeManager().getImportedObjsByKey(pEndKey)
        self.distance = domElement.attribute("distance", "").toDouble()[0]   
    
    def save( self, domDocument ):
        distanceNode = QtXml.QDomElement( domDocument.createElement( "Distance" ) )
        distanceNode.setAttribute( "pBeginKey", self.pointBegin.key )
        distanceNode.setAttribute( "pEndKey", self.pointEnd.key )
        distanceNode.setAttribute( "key", self.key )
        distanceNode.setAttribute( "name", self.name )
        distanceNode.setAttribute( "distance", str(self.distance) )
        
        return distanceNode

class DistanceConstraint( Distance ):
    def __init__( self, name, pBegin, pEnd ):
        Distance.__init__( self, name, pBegin, pEnd )
        self.radius = self.settings.sketcherData.distanceRadius
        self.objType = ObjectType.DISTANCE_CONSTRAINT
        self.con = None
        self.color = self.settings.sketcherData.distanceColor
        self.texture = None
        self.fixed = False
        self.parameterRange=[]
        
    def clone( self, **attr ):
        obj = deepcopy( self )
        obj.__dict__.update( attr )
        return obj
    
    def update(self):
        Distance.update(self)
        if not self.fixed and not self.ghost:
            self.distance = self.height
    
    def load (self, domElement):
        Distance.load(self, domElement)
        if domElement.attribute("fixed", "") == "True":
            self.fixed = True
        else:
            self.fixed = False

    def importItem(self, domElement, nrOfImports=0, objNr=0):
        Distance.importItem(self, domElement, nrOfImports, objNr)
        self.key = "d" + str(objNr)
        print "Distance: ", self.key, self.name, self.pointBegin.key, self.pointEnd.key
        if domElement.attribute("fixed", "") == "True":
            self.fixed = True
        else:
            self.fixed = False

    def save( self, domDocument ):
        distanceNode = QtXml.QDomElement( domDocument.createElement( "DistanceConstraint" ) )
        distanceNode.setAttribute( "pBeginKey", self.pointBegin.key )
        distanceNode.setAttribute( "pEndKey", self.pointEnd.key )
        distanceNode.setAttribute( "key", self.key )
        distanceNode.setAttribute( "name", self.name )
        distanceNode.setAttribute( "distance", str(self.distance) )
        distanceNode.setAttribute( "fixed", str(self.fixed) )
        
        return distanceNode  

class Cluster( Object ):
    def __init__(self, pBegin, pMiddle, pEnd):
        Object.__init__( self )
        self.name = ""
        self.pointBegin = pBegin
        self.pointMiddle = pMiddle
        self.pointEnd = pEnd
        self.objType = None
        self.color = [1.0, 0.0, 0.0, 0.15]
        self.height = 40.0
    
    def draw( self ):
        glPushMatrix()

        glDisable( GL_DEPTH_TEST )
        glEnable ( GL_BLEND )
        glColor4fv( self.color )
                
        glBegin(GL_TRIANGLES)            
        glVertex3f(self.pointBegin.position[0], self.pointBegin.position[1], self.pointBegin.position[2])
        glVertex3f(self.pointMiddle.position[0], self.pointMiddle.position[1], self.pointMiddle.position[2])
        glVertex3f(self.pointEnd.position[0], self.pointEnd.position[1], self.pointEnd.position[2])
        glEnd()
        
        glDisable ( GL_BLEND )
        glEnable( GL_DEPTH_TEST )
        
        glPopMatrix()

    def update( self ):
        pass

class Axis( Object ):
    def __init__( self, position, width, height ):
        Object.__init__( self )
        self.position = position
        self.width = width
        self.height = height
        self.selected = False
        self.selectionID = 0
        self.isMovable = True
         
    def draw( self ):
        glPushMatrix()
        glTranslate( self.position[0], self.position[1], self.position[2] )
        self.drawXAxis()
        self.drawYAxis()
        self.drawZAxis()
        glPopMatrix()
     
    def drawWithPicking( self ):
        glPushMatrix()
        glTranslate( self.position[0], self.position[1], self.position[2] )
        glPushName( 1 )
        self.drawXAxis()
        glPopName()
        glPushName( 2 )
        self.drawYAxis()
        glPopName()
        glPushName( 3 )
        self.drawZAxis()
        glPopName()
        glPopMatrix()
             
    def clone( self, **attr ):
        obj = deepcopy( self )
        obj.__dict__.update( attr )
        return obj
       
    def updatePosition( self, position ):
        self.position = position
    
    def drawXAxis( self ):
        # x axis    
        glPushMatrix()
        if self.selected == True and self.selectionId == 1:
            glColor3fv( [1.0, 1.0, 0.0] )
        else:
            glColor3fv( [1.0, 0.0, 0.0] )
        glTranslate( -1.0, 0.0, 0.0 )
        glRotate( 90, 0.0, 1.0 , 0.0 )
        #glRotate(180, 1.0, 0.0, 0.0)
        gluCylinder( self.quadric, self.width, self.width, self.height, 10, 10 )
        glPushMatrix()
        glTranslatef( 0.0, 0.0, self.height )
        gluCylinder( self.quadric, self.width*2.5, 0.0, self.height/5, 10, 10 )
        glPopMatrix()
        glPopMatrix()

    def drawYAxis( self ):
        # y axis
        glPushMatrix()
        if self.selected == True and self.selectionId == 2:
            glColor3fv( [1.0, 1.0, 0.0] )
        else:
            glColor3fv( [0.0, 1.0, 0.0] )
        glRotate( -90, 1.0, 0.0 , 0.0 )
        gluCylinder( self.quadric, self.width, self.width, self.height, 10, 10 )
        glPushMatrix()
        glTranslatef( 0.0, 0.0, self.height )
        gluCylinder( self.quadric, self.width*2.5, 0.0, self.height/5, 10, 10 )
        
        newFont = QtGui.QFont()
        newFont.setStyleStrategy( QtGui.QFont.OpenGLCompatible ) 
        #self.activeViewport.renderText(14.0, 10.0, 1.0, 'XY', newFont)
        #glEnable(GL_LIGHTING)
        glPopMatrix()
        glPopMatrix()

    def drawZAxis( self ):
        # z axis
        glPushMatrix()
        if self.selected == True and self.selectionId == 3:
            glColor3fv( [1.0, 1.0, 0.0] )
        else:
            glColor3fv( [0.0, 0.0, 1.0] )
        glRotate( 180, 0.0, 1.0 , 0.0 )
        gluCylinder( self.quadric, self.width, self.width, self.height, 10, 10 )
        glPushMatrix()
        glTranslatef( 0.0, 0.0, self.height )
        gluCylinder( self.quadric, self.width*2.5, 0.0, self.height/5, 10, 10 )
        glPopMatrix()
        glPopMatrix()
     
    def setNewReference( self, oldObj, newObj ):
        pass

class PointCluster ( Point ):
    def __init__( self, position, radius, relatedPoint ):
        Point.__init__(self,"", position, radius)
        self.color = [1.0, 0.0, 0.0, 0.4]
        self.selectColor = [1.0, 1.0, 0.0, 0.4]
        self.temporary = False
        self.fixed = False
        self.relPoint = relatedPoint
        
    def draw( self ):
        glPushMatrix()
        glEnable ( GL_BLEND )
        if self.selected:
            glColor4fv( self.selectColor )
        else:
            glColor4fv( self.color )
        glTranslatef( self.position[0], self.position[1], self.position[2] )
        gluSphere( self.quadric, self.radius, 10, 10 )
        glDisable ( GL_BLEND )
        glPopMatrix()
    
    def getClusterPoints(self):
        clusterPoints = []
        clusterPoints += [self]
        return clusterPoints

class DistanceCluster( Distance ):
    def __init__( self, pBegin, pEnd ):    
        Distance.__init__(self,"", pBegin, pEnd)
        # Rick 20090519 - set radius from preferences 
        #self.radius = 3.0
        self.radius = self.settings.sketcherData.distanceRadius * 1.5
        self.color = [1.0, 0.0, 0.0, 0.4]
        self.selectColor = [1.0, 1.0, 0.0, 0.4]
        self.temporary = False
        self.fixed = False
                
    def draw( self ):
        glPushMatrix()
        if self.selected:
            glColor4fv( self.selectColor )
        else:
            glColor4fv( self.color )
        glEnable ( GL_BLEND )
        
        # Rick 20090519 glMultMatrixd doesn't work properly, see above
        # glMultMatrixd( self.rotMatrix )
        axis = -self.orientation.axis()
        angle = self.orientation.angle()
        pos = self.pointBegin.position
        glTranslate(pos[0],pos[1],pos[2])
        glRotate(angle*180/math.pi, axis[0], axis[1], axis[2])

        if self.height == 0.0:
            self.height = 0.1

        gluCylinder( self.quadric, float(self.radius), float(self.radius), float(self.height), 10, 10 )
        glDisable ( GL_BLEND )
        glPopMatrix()
    
    def getClusterPoints(self):
        clusterPoints = []
        clusterPoints += [self.pointBegin]
        clusterPoints += [self.pointEnd]
        return clusterPoints
        
class ClusterI( Object ):
    def __init__(self, constrainedness):
        Object.__init__( self )
        self.name = ""
        self.points = ""
        self.dimension = 3
        self.zeroIndex = None
        self.objType = ObjectType.CLUSTER
        self.constrainedness = constrainedness
        self.color = [1.0, 0.0, 0.0, 0.2]
        self.underconstrainedClr = [1.0, 0.0, 0.0, 0.2]
        self.overconstrainedClr = [0.0, 0.0, 1.0, 0.2]
        self.wellconstrainedClr = [0.0, 1.0, 0.0, 0.2]
        self.selectColor = [1.0, 1.0, 0.0, 0.15]
        self.clusterPoints = []
        self.pickColor()
        self.temporary = False
        self.fixed = False
        self.hull = None
        
    def pickColor(self):
        if self.constrainedness == GeometricCluster.I_UNDER or self.constrainedness == GeometricCluster.S_UNDER:
            self.color = self.underconstrainedClr
        elif self.constrainedness == GeometricCluster.I_OVER or self.constrainedness == GeometricCluster.S_OVER:
            self.color = self.overconstrainedClr
        elif self.constrainedness == GeometricCluster.OK:
            self.color = self.wellconstrainedClr
        
    def draw( self ):
        glPushMatrix()

        if self.selected:
            glColor4fv( self.selectColor )
        else:
            glColor4fv( self.color )
                            
        if self.hull != None:
            for triangle in self.hull:
                #glDisable( GL_DEPTH_TEST)
                glEnable ( GL_BLEND )
                glBegin(GL_TRIANGLES)
                for vertex in triangle:    
                    glVertex3f(vertex[0], vertex[1], vertex[2])
                glEnd()
                glDisable ( GL_BLEND )
                #glEnable( GL_DEPTH_TEST)
                glBegin(GL_LINES)
                glVertex3f(triangle[0][0], triangle[0][1], triangle[0][2])
                glVertex3f(triangle[1][0], triangle[1][1], triangle[1][2])
                glVertex3f(triangle[1][0], triangle[1][1], triangle[1][2])
                glVertex3f(triangle[2][0], triangle[2][1], triangle[2][2])
                glVertex3f(triangle[2][0], triangle[2][1], triangle[2][2])
                glVertex3f(triangle[0][0], triangle[0][1], triangle[0][2])
                glEnd()
        else:
            glDisable( GL_DEPTH_TEST)
            glEnable ( GL_BLEND )
            glBegin(GL_POLYGON)
            for clsPoint in self.clusterPoints:
                glVertex3f(clsPoint.position[0], clsPoint.position[1], clsPoint.position[2])
            glEnd()
            glDisable ( GL_BLEND )
            glEnable( GL_DEPTH_TEST)
        glPopMatrix()

    def update( self ):
        points = []
        for clsPoint in self.clusterPoints:
            points += [clsPoint.position]

        self.determineDimension(points)
        if self.dimension == 2:
            if len(self.clusterPoints) < 4:
                self.hull = [points]
                return
        elif self.dimension == 3:
            if len(self.clusterPoints) == 4:
                self.hull = self.createTetrahedron(points)
                return
            elif len(self.clusterPoints) == 3:
                self.hull = [points]
                return
        
        """ handle the creation of a hull for more than 3 points in 2D and more than 4 point in 3D. """        
        if self.dimension == 2:
            points = self.convert3DTo2D(points)
        triangulation = dcore.Triangulation(points, self.dimension)

        if self.dimension == 2:
            indexHull = self.createFaces(triangulation.get_elements_indices())
        if self.dimension == 3:
            indexHull = self.createHull(triangulation.get_elements_indices())

        self.hull = []
        for iHull in indexHull:
            face = map(lambda x:points[x], iHull)
            self.hull += [face]
        
        if self.dimension == 2:
            self.hull = self.convert2DTo3D(self.hull)
                    
    def getClusterPoints(self):
        return self.clusterPoints

    def createHull(self, tetraIndex):
        faces = self.createFaces(tetraIndex)

        faces.sort()
        uniqueFaces = []
            
        for face in faces:
            if faces.count(face) == 1:
                uniqueFaces += [face]
        return uniqueFaces

    def createFaces(self, tetrahedra):
        faces = []
        if self.dimension==2:
            for face in tetrahedra:
                if self.zeroIndex == 0:
                    faces += [[face[0], face[1], face[2]]]
                elif self.zeroIndex == 1:
                    faces += [[face[0], face[1], face[2]]]
                elif self.zeroIndex == 2:
                    faces += [[face[0], face[1], face[2]]]
            
        elif self.dimension==3:
            for tetrahedron in tetrahedra:
                faces += [[tetrahedron[0], tetrahedron[1],tetrahedron[2]]]
                faces += [[tetrahedron[1], tetrahedron[2],tetrahedron[3]]]
                faces += [[tetrahedron[2], tetrahedron[3],tetrahedron[0]]]
                faces += [[tetrahedron[3], tetrahedron[0],tetrahedron[1]]]
                
        for face in faces:
            face.sort()
        return faces
        
    def determineDimension(self, points):    
        pointsOfTwoDimensions = filter(lambda x:x[0] == 0.0, points)
        if len(pointsOfTwoDimensions) == len(points):
            self.dimension = 2
            self.zeroIndex = 0
            return
        
        pointsOfTwoDimensions = filter(lambda x:x[1] == 0.0, points)
        if len(pointsOfTwoDimensions) == len(points):
            self.dimension = 2
            self.zeroIndex = 1
            return
        
        pointsOfTwoDimensions = filter(lambda x:x[2] == 0.0, points)
        if len(pointsOfTwoDimensions) == len(points):
            self.dimension = 2
            self.zeroIndex = 2
            return
        
        self.dimension = 3 
    
    def convert3DTo2D(self, points):
        newDimension = []
        if self.dimension == 2:
            for point in points:
                if self.zeroIndex == 0:
                    newDimension += [[point[1], point[2]]]
                elif self.zeroIndex == 1:
                    newDimension += [[point[0], point[2]]]
                elif self.zeroIndex == 2:
                    newDimension += [[point[0], point[1]]]
        return newDimension
    
    def convert2DTo3D(self, triangles):
        newDimension = []
        if self.dimension == 2:
            index = 0
            for triangle in triangles:
                newDimension += [[]]
                for point in triangle:
                    if self.zeroIndex == 0:
                        newDimension[index] += [[0.0, point[0], point[1]]]
                    elif self.zeroIndex == 1:
                        newDimension[index] += [[point[0], 0.0, point[1]]]
                    elif self.zeroIndex == 2:
                        newDimension[index] += [[point[0], point[1], 0.0]]
                index += 1
        return newDimension
    
    def createTetrahedron(self, points):
        hull = []
        if len(points) == 4:
            hull += [[points[0], points[1], points[2]]]
            hull += [[points[0], points[1], points[3]]]
            hull += [[points[0], points[2], points[3]]]
            hull += [[points[1], points[2], points[3]]]
        return hull
        
