""" Behavioral pattern: State pattern """

from includes import *
from singleton import *
from prototypeObjects import *
from geosolver.matfunc import Vec

class Tool(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.prototypeObject = None
        self.prototypeManager = PrototypeManager()
        self.toolType = None
        self.lastPosition = Vec([0.0,0.0,0.0])
        self.needUpdate = False
        self.needPicking = False
        self.multipleSelect = False
    
    def setPrototypeObjectToAdjust(self, object):
        self.prototypeObject = object
    
    def manipulate(self):
        raise NotImplementedError(caller + ' must be implemented in subclass')
    
    def handleMousePress(self, mouseEvent, camera, viewportType):
        raise NotImplementedError(caller + ' must be implemented in subclass')
    
    def handleMouseRelease(self):
        raise NotImplementedError(caller + ' must be implemented in subclass')
    
    def handleMouseMove(self, mouseEvent):
        raise NotImplementedError(caller + ' must be implemented in subclass')

    def handleMouseRelease(self, mouseEvent, selection):
        raise NotImplementedError(caller + ' must be implemented in subclass')
    
    def handleKeyPress(self, keyEvent):
        pass
       
    def handleKeyRelease(self, keyEvent):
        pass


class SelectTool(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.SELECT
        self.needPicking = True
        self.selectionStarted = False
        self.beginSelPoint = QtCore.QPoint()
        self.endSelPoint = QtCore.QPoint()
        self.holdShift = False  
        self.multipleSelect = True    
        
    def manipulate(self):
        pass
        
    def handleMousePress(self, mouseEvent, camera, viewportType, selection):
        self.prototypeManager.showAxis = False
        if self.beginSelPoint.isNull():
            self.beginSelPoint.setX(mouseEvent.x())
            self.beginSelPoint.setY(mouseEvent.y())

        if selection != -1:
            if self.holdShift:
                self.prototypeManager.changeSelection(selection)
            else:
                self.prototypeManager.setSelectedObject(selection)
        elif selection == -1 and not self.holdShift:
            self.prototypeManager.deselectAllObjects()

        self.needUpdate = True
            
    def handleKeyPress(self, keyEvent):
        if keyEvent.key() == QtCore.Qt.Key_Delete:
            self.prototypeManager.deleteSelectedObjects()
        if keyEvent.key() == QtCore.Qt.Key_Shift:
            self.holdShift = True
    
    def handleKeyRelease(self, keyEvent):
        if keyEvent.key() == QtCore.Qt.Key_Shift:
            self.holdShift = False
                
    def handleMouseMove(self, mouseEvent, camera, viewportType, selection):
        self.endSelPoint.setX(mouseEvent.x())
        self.endSelPoint.setY(mouseEvent.y())
        if mouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.selectionStarted = True
        if selection != -1 and mouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.prototypeManager.setSelectedObjects(selection, True, True)
        elif selection == -1:
            self.prototypeManager.deselectAllObjects(True, True) 
        self.needUpdate = True
    
    def handleMouseRelease(self, mouseEvent, selection):
        self.beginSelPoint.setX(0)
        self.beginSelPoint.setY(0)
        self.endSelPoint.setX(0)
        self.endSelPoint.setY(0)
        self.prototypeManager.convertTemporySelection()
        self.selectionStarted = False
        self.needUpdate = True
              
class PlacePointTool(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.PLACE_POINT
        self.newPoint = None
        # Rick 20090519
        self.needPicking = True
        
    def manipulate(self):
        pass
        
    def handleMousePress(self, mouseEvent, camera, viewPortType, selection):
        translation = Vec(camera.unprojectedCoordinatesOf([mouseEvent.x(), mouseEvent.y(), 1.0]))
        if viewPortType == ViewportType.PERSPECTIVE:
            position = camera.getPositionOnYPlane(translation)  
        else:
            position = translation
        
        if viewPortType == ViewportType.FRONT:
            position[2] = 0.0
        elif viewPortType == ViewportType.SIDE:
            position[0] = 0.0
        elif viewPortType == ViewportType.TOP:
            position[1] = 0.0
        
        #print " position position: " , position[0], position[1], position[2]
        pName = "p" + str(self.prototypeManager.objectNr)
        self.newPoint = Point(pName, Vec([position[0], position[1], position[2]]), 5.0)
        self.prototypeManager.addObject(self.newPoint)
        self.needUpdate = True
    
    def handleMouseMove(self, mouseEvent, camera, viewPortType, selection):
        # Rick 20090519
        # self.needUpdate = True
        pass

    def handleMouseRelease(self, mouseEvent, selection):
        pass
    
class PlaceFixedConstraintTool(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.PLACE_FIXEDCONSTRAINT
        # Rick 20090519
        self.needPicking = True
        

    def handleMousePress(self, mouseEvent, camera, viewPortType, selection):
        translation = Vec(camera.unprojectedCoordinatesOf([mouseEvent.x(), mouseEvent.y(), 1.0]))
        if viewPortType == ViewportType.PERSPECTIVE:
            position = camera.getPositionOnYPlane(translation)  
        else:
            position = translation
        
        if viewPortType == ViewportType.FRONT:
            position[2] = 0.0
        elif viewPortType == ViewportType.SIDE:
            position[0] = 0.0
        elif viewPortType == ViewportType.TOP:
            position[1] = 0.0
        
        fixedPoints = filter(lambda x:x.objType == ObjectType.FIXED_POINT, self.prototypeManager.prtObjects)

        pName = "f" + str(self.prototypeManager.objectNr)
        newFixedConstraint = FixedPoint(pName, Vec([position[0], position[1], position[2]]), 5.0)
        self.prototypeManager.addObject(newFixedConstraint)
        self.needUpdate = True

    def handleMouseMove(self, mouseEvent, camera, viewPortType, selection):
        # Rick 20090519
        # self.needUpdate = True
        pass

    def handleMouseRelease(self, mouseEvent, selection):
        pass

class PlaceDistanceTool(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.PLACE_DISTANCE
        self.pointBegin = None
        self.pointEnd = None
        self.needPicking = True
        self.ghostPoint = None
        self.ghostDistance = None
        
    def manipulate(self):
        pass
    
    def handleMousePress(self, mouseEvent, camera, viewportType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
            
        if selection != -1 and mouseEvent.buttons() == QtCore.Qt.LeftButton and (
        self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT):
            selectedObject = self.prototypeManager.objectSelected
            
            if self.pointBegin == None:
                self.pointBegin = selectedObject
                selectedObject.selected = True
                self.createGhosts(self.pointBegin)
            
            elif self.pointEnd == None and self.pointBegin != selectedObject:
                self.pointEnd = selectedObject
                exists = self.validate()
                if not exists:
                    dcName = "l" + str(self.prototypeManager.objectNr)
                    newDistance = Distance(dcName,self.pointBegin, self.pointEnd)            
                    self.prototypeManager.addObject(newDistance)
                    self.pointBegin = self.pointEnd
                    self.pointEnd = None
                    self.removeGhosts()
                    self.createGhosts(self.pointBegin)
                else:
                    self.pointEnd = None
                self.needUpdate = True 
            
        elif mouseEvent.buttons() == QtCore.Qt.LeftButton:
            if self.pointBegin == None:
                self.createPoint(viewportType, camera, mouseEvent)
            elif self.pointEnd == None:
                self.createPoint(viewportType, camera, mouseEvent)
                dcName = "l" + str(self.prototypeManager.objectNr)
                newDistance = Distance(dcName,self.pointBegin, self.pointEnd)            
                self.prototypeManager.addObject(newDistance)
                self.pointBegin = self.pointEnd
                self.pointEnd = None
                self.removeGhosts()
            
            self.createGhosts(self.pointBegin)
            self.needUpdate = True
            
        elif mouseEvent.buttons() == QtCore.Qt.RightButton:
            self.needUpdate = True
            self.removeGhosts()
            self.pointBegin.selected = False
            self.pointEnd = None
            self.pointBegin = None
        else:
            self.prototypeManager.objectSelected.selected = False

    def createPoint(self, viewPortType, camera, mouseEvent):    
        createPoint = PlacePointTool()
        createPoint.handleMousePress(mouseEvent, camera, viewPortType, -1)
        if createPoint.newPoint != None:
            if self.pointBegin == None:
                self.pointBegin = createPoint.newPoint
            elif self.pointEnd == None:
                self.pointEnd = createPoint.newPoint
    
    def createGhosts(self, point):
        pName = "p" + str(self.prototypeManager.objectNr)
        self.ghostPoint = Point(pName, Vec([point.position[0], point.position[1], point.position[2]]), 5.0)
        self.ghostPoint.ghost = True
        self.prototypeManager.addObject(self.ghostPoint)
        dcName = "l" + str(self.prototypeManager.objectNr)
        self.ghostDistance = Distance(dcName, point, self.ghostPoint)            
        self.ghostDistance.ghost = True
        self.prototypeManager.addObject(self.ghostDistance)

    def removeGhosts(self):
        if self.ghostDistance != None and self.ghostPoint != None:
            removeObjects = []
            removeObjects += [self.ghostDistance]
            removeObjects += [self.ghostPoint]
            self.prototypeManager.removeObjects(removeObjects)
            self.ghostPoint = None
            self.ghostDistance = None
        
    def validate(self):
        for obj in self.prototypeManager.prtObjects:
            if obj.objType == ObjectType.DISTANCE_HELPER:
                if (obj.pointBegin == self.pointBegin and obj.pointEnd == self.pointEnd) or (obj.pointBegin == self.pointEnd and obj.pointEnd == self.pointBegin):
                    return True
        return False

    def handleMouseMove(self, mouseEvent, camera, viewPortType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
        if self.ghostPoint != None:
            translation = Vec(camera.unprojectedCoordinatesOf([mouseEvent.x(), mouseEvent.y(), 1.0]))
            if viewPortType == ViewportType.PERSPECTIVE:
                position = camera.getPositionOnYPlane(translation)  
            else:
                position = translation
            
            if viewPortType == ViewportType.FRONT:
                position[2] = 0.0
            elif viewPortType == ViewportType.SIDE:
                position[0] = 0.0
            elif viewPortType == ViewportType.TOP:
                position[1] = 0.0
            self.ghostPoint.setPosition(position)
            self.needUpdate = True
            
        if selection != -1 and self.prototypeManager.objectSelected != None and (
           self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT):
            selectedObject = self.prototypeManager.objectSelected
            selectedObject.selected = True
            self.needUpdate = True
        elif self.prototypeManager.objectSelected != None:
            self.prototypeManager.deselectObject()
            self.needUpdate = True
                            
    def handleMouseRelease(self, mouseEvent, selection):
        pass
    
class PlaceDistanceConstraintTool(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.PLACE_DISTANCE_CONSTRAINT
        self.pointBegin = None
        self.pointEnd = None
        self.needPicking = True
        self.ghostPoint = None
        self.ghostDistance = None
        
    def manipulate(self):
        pass
    
    def handleMousePress(self, mouseEvent, camera, viewportType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
            
        if selection != -1 and mouseEvent.buttons() == QtCore.Qt.LeftButton and (
        self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT):
            selectedObject = self.prototypeManager.objectSelected
            
            if self.pointBegin == None:
                self.pointBegin = selectedObject
                selectedObject.selected = True
                self.createGhosts(self.pointBegin)
            
            elif self.pointEnd == None and self.pointBegin != selectedObject:
                self.pointEnd = selectedObject
                exists = self.validate()
                if not exists:
                    self.createDistanceConstraint()
                    self.createGhosts(self.pointBegin)
                else:
                    self.pointEnd = None
                    
                self.needUpdate = True 
            
        elif mouseEvent.buttons() == QtCore.Qt.LeftButton:
            if self.pointBegin == None:
                self.createPoint(viewportType, camera, mouseEvent)
            elif self.pointEnd == None:
                self.createPoint(viewportType, camera, mouseEvent)
                self.createDistanceConstraint()
            
            self.createGhosts(self.pointBegin)
            self.needUpdate = True

        elif mouseEvent.buttons() == QtCore.Qt.RightButton:
            self.needUpdate = True
            self.removeGhosts()
            self.pointBegin.selected = False
            self.pointEnd = None
            self.pointBegin = None
        else:
            self.prototypeManager.objectSelected.selected = False
       
    def createPoint(self, viewPortType, camera, mouseEvent):
        createPoint = PlacePointTool()
        createPoint.handleMousePress(mouseEvent, camera, viewPortType, -1)
        if createPoint.newPoint != None:
            if self.pointBegin == None:
                self.pointBegin = createPoint.newPoint
            elif self.pointEnd == None:
                self.pointEnd = createPoint.newPoint
    
    def createDistanceConstraint(self):
        dcName = "d" + str(self.prototypeManager.objectNr)
        newDistance = DistanceConstraint(dcName, self.pointBegin, self.pointEnd)     
        self.prototypeManager.addObject(newDistance)
        self.pointBegin = self.pointEnd
        self.pointEnd = None
        self.removeGhosts()
        
    def createGhosts(self, point):
        pName = "p" + str(self.prototypeManager.objectNr)
        self.ghostPoint = Point(pName, Vec([point.position[0], point.position[1], point.position[2]]), 5.0)
        self.ghostPoint.ghost = True
        self.prototypeManager.addObject(self.ghostPoint)
        dcName = "d" + str(self.prototypeManager.objectNr)
        self.ghostDistance = DistanceConstraint(dcName, point, self.ghostPoint)            
        self.ghostDistance.ghost = True
        self.prototypeManager.addObject(self.ghostDistance)
            
    def removeGhosts(self):
        if self.ghostDistance != None and self.ghostPoint != None:
            removeObjects = []
            removeObjects += [self.ghostDistance]
            removeObjects += [self.ghostPoint]
            self.prototypeManager.removeObjects(removeObjects)
            self.ghostPoint = None
            self.ghostDistance = None
            
    def validate(self):
        for obj in self.prototypeManager.prtObjects:
            if obj.objType == ObjectType.DISTANCE_CONSTRAINT:
                if (obj.pointBegin == self.pointBegin and obj.pointEnd == self.pointEnd) or (obj.pointBegin == self.pointEnd and obj.pointEnd == self.pointBegin):
                    return True
            if obj.objType == ObjectType.DISTANCE_HELPER:
                if (obj.pointBegin == self.pointBegin and obj.pointEnd == self.pointEnd) or (obj.pointBegin == self.pointEnd and obj.pointEnd == self.pointBegin):
                    self.prototypeManager.removeObjects([obj])
                    return False
                
        return False
               
    def handleMouseMove(self, mouseEvent, camera, viewPortType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
        if self.ghostPoint != None:
            translation = Vec(camera.unprojectedCoordinatesOf([mouseEvent.x(), mouseEvent.y(), 1.0]))
            if viewPortType == ViewportType.PERSPECTIVE:
                position = camera.getPositionOnYPlane(translation)  
            else:
                position = translation

            if viewPortType == ViewportType.FRONT:
                position[2] = 0.0
            elif viewPortType == ViewportType.SIDE:
                position[0] = 0.0
            elif viewPortType == ViewportType.TOP:
                position[1] = 0.0
            self.ghostPoint.setPosition(position)
            self.needUpdate = True
            
        if selection != -1 and self.prototypeManager.objectSelected != None and (
           self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT):
            selectedObject = self.prototypeManager.objectSelected
            selectedObject.selected = True
            self.needUpdate = True
        elif self.prototypeManager.objectSelected != None:
            self.prototypeManager.deselectObject()
            self.needUpdate = True
    
    def handleMouseRelease(self, mouseEvent, selection):
        pass

class PlaceAngleConstraintTool(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.PLACE_ANGLE_CONSTRAINT
        self.pointBegin = None
        self.pointMiddle = None
        self.pointEnd = None
        self.distanceSelected = None
        self.needPicking = True
        self.newDistances = []
        # Rick 20090519
        self.ghostPoint = None
        self.ghostDistance = None
        self.ghostAngle = None

    def manipulate(self):
        pass
    
    def handleMousePress(self, mouseEvent, camera, viewportType, selection):
        """ Handle the mouse press to place an angle constraint, the mouse constraint
            consists of 3 (fixed) points. The user may select other constraints which
            consist of points """
        if selection != -1 and mouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.prototypeManager.setSelectedObject(selection)
            selectedObject = self.prototypeManager.objectSelected
            self.createAngleBySelection(selectedObject) 
        elif selection == -1 and mouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.createAngleByPlacingPoints(mouseEvent, camera, viewportType) 
        elif mouseEvent.buttons() == QtCore.Qt.RightButton:
            self.cleanUp()
            
        self.needUpdate = True
    
    def createAngleBySelection(self, selectedObject):
        """ Check which of the points are already set to create the angle constraint. When 
                the last point is set, the angle constraint is created. During the determination
                of the points the view is updated with new selection information. """
        if self.pointBegin == None:
            """ Check which object or constraint is selected. """
            if selectedObject.objType == ObjectType.POINT:
                self.pointBegin = selectedObject
            elif selectedObject.objType == ObjectType.DISTANCE_CONSTRAINT or selectedObject.objType == ObjectType.DISTANCE_HELPER:
                self.pointBegin = selectedObject.pointBegin
                self.pointMiddle = selectedObject.pointEnd
                self.distanceSelected = selectedObject
            # Rick 20090519
            self.createGhosts(self.pointBegin)
        elif self.pointMiddle == None:
            """ Check which object or constraint is selected. """
            if selectedObject.objType == ObjectType.POINT:
                if not self.isConnection(self.pointBegin, selectedObject):
                    self.newDistances += [[self.pointBegin, selectedObject]]
                self.pointBegin.selected = True
                self.pointMiddle = selectedObject
                self.pointMiddle.selected = True
            elif selectedObject.objType == ObjectType.DISTANCE_CONSTRAINT or selectedObject.objType == ObjectType.DISTANCE_HELPER:
                if not self.isConnection(self.pointBegin, selectedObject.pointBegin):
                    self.newDistances += [[self.pointBegin, selectedObject.pointBegin]]
                self.pointMiddle = selectedObject.pointBegin
                self.pointEnd = selectedObject.pointEnd
                self.createConstraint()
            # Rick 20090519
            self.removeGhosts()
            self.createGhosts(self.pointMiddle)
        elif self.pointEnd == None:
            """ Check which object or constraint is selected. 
                Create an angle constraint """
            if selectedObject.objType == ObjectType.POINT:
                if not self.isConnection(self.pointMiddle, selectedObject):
                    self.newDistances += [[self.pointMiddle, selectedObject]]
                if selectedObject != self.pointBegin and selectedObject != self.pointMiddle:
                    self.pointEnd = selectedObject
                    self.createConstraint()
            elif (selectedObject.objType == ObjectType.DISTANCE_CONSTRAINT or selectedObject.objType == ObjectType.DISTANCE_HELPER) and self.distanceSelected != selectedObject:        
                if self.pointMiddle == selectedObject.pointBegin:
                    self.pointEnd = selectedObject.pointEnd
                elif self.pointMiddle == selectedObject.pointEnd:
                    self.pointEnd = selectedObject.pointBegin
                elif self.pointBegin == selectedObject.pointBegin:
                    tempPoint = self.pointMiddle
                    self.pointMiddle = self.pointBegin
                    self.pointBegin = tempPoint
                    self.pointEnd = selectedObject.pointEnd
                elif self.pointBegin == selectedObject.pointEnd:
                    tempPoint = self.pointMiddle
                    self.pointMiddle = self.pointBegin
                    self.pointBegin = tempPoint
                    self.pointEnd = selectedObject.pointBegin
                else:
                    """ The user made a faulty selection, let him try again """
                    return
                self.createConstraint()
    
    def createAngleByPlacingPoints(self, mouseEvent, camera, viewportType):
        createPoint = PlacePointTool()
        createPoint.handleMousePress(mouseEvent, camera, viewportType, -1)
        if createPoint.newPoint != None:
            if self.pointBegin == None:
                self.pointBegin = createPoint.newPoint
                # Rick 20090519
                self.createGhosts(self.pointBegin)
            elif self.pointMiddle == None:
                self.pointMiddle = createPoint.newPoint
                self.newDistances += [[self.pointBegin, self.pointMiddle]]
                # Rick 20090519
                self.removeGhosts()
                self.createGhosts(self.pointMiddle)
            elif self.pointEnd == None:
                self.pointEnd = createPoint.newPoint
                self.newDistances += [[self.pointMiddle, self.pointEnd]]
                self.createConstraint()

    
    def createConstraint(self):
        """ The actual creation of the angle constraint. A new unique name is created and is added to the GCS"""
        if self.pointBegin != None and self.pointMiddle != None and self.pointEnd != None:
            try:
                aName = "a" + str(self.prototypeManager.objectNr)
                newAngleConstraint = AngleConstraint(aName, self.pointBegin, self.pointMiddle, self.pointEnd)
                #newCluster = Cluster(self.pointBegin, self.pointMiddle, self.pointEnd)
                self.prototypeManager.addObject(newAngleConstraint)
                newAngleConstraint.update()
                self.prototypeManager.updateConstraint(newAngleConstraint, newAngleConstraint.angle)
                #self.prototypeManager.addObject(newCluster)
                
            except StandardError:
                self.cleanUp()
                return
                
            #self.addNewDistances()
            self.cleanUp()

    def isConnection(self, pBegin, pEnd):
        """ For clarity, an angle constraint is drawn between two distances. 
            This is a check whether a distance is already defined between two points. """
        for prObject in self.prototypeManager.prtObjects:
            if prObject.objType == ObjectType.DISTANCE_CONSTRAINT or prObject.objType == ObjectType.DISTANCE_HELPER:
                if (prObject.pointBegin == pBegin and prObject.pointEnd == pEnd) or (prObject.pointBegin == pEnd and prObject.pointEnd == pBegin):
                    return True
        return False
    
    # Rick 20090519 now in disuse
    def addNewDistances(self):
        """ New distances are added to the list of objects. Most of the time this function
            is called after determining whether a new distance is needed to draw the 
            angle constraint (see isConnection) """
        for distance in self.newDistances:
            dcName = "d" + str(self.prototypeManager.objectNr)
            newDistance = Distance(dcName, distance[0], distance[1])
            self.prototypeManager.addObject(newDistance)
            
        self.newDistances = []
               
    def handleMouseMove(self, mouseEvent, camera, viewPortType, selection):
        # Rick 20090519
        # was: pass 
        # now adding a ghost!
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
        if self.ghostPoint != None:
            translation = Vec(camera.unprojectedCoordinatesOf([mouseEvent.x(), mouseEvent.y(), 1.0]))
            if viewPortType == ViewportType.PERSPECTIVE:
                position = camera.getPositionOnYPlane(translation)  
            else:
                position = translation

            if viewPortType == ViewportType.FRONT:
                position[2] = 0.0
            elif viewPortType == ViewportType.SIDE:
                position[0] = 0.0
            elif viewPortType == ViewportType.TOP:
                position[1] = 0.0
            self.ghostPoint.setPosition(position)
            self.needUpdate = True
            
        if selection != -1 and self.prototypeManager.objectSelected != None and (
           self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT):
            selectedObject = self.prototypeManager.objectSelected
            selectedObject.selected = True
            self.needUpdate = True
        elif self.prototypeManager.objectSelected != None:
            self.prototypeManager.deselectObject()
            self.needUpdate = True
 
    def createGhosts(self, point):
        pName = "p" + str(self.prototypeManager.objectNr)
        self.ghostPoint = Point(pName, Vec([point.position[0], point.position[1], point.position[2]]), 5.0)
        self.ghostPoint.ghost = True
        self.prototypeManager.addObject(self.ghostPoint)
        dcName = "d" + str(self.prototypeManager.objectNr)
        self.ghostDistance = Distance(dcName, point, self.ghostPoint)            
        self.ghostDistance.ghost = True
        self.prototypeManager.addObject(self.ghostDistance)
        # Rick 20090519
        if self.pointMiddle != None:
            acName = "ghost_angle" + str(self.prototypeManager.objectNr)
            self.ghostAngle = AngleConstraint(acName, self.pointBegin, self.pointMiddle, self.ghostPoint)            
            self.ghostAngle.ghost = True
            self.prototypeManager.addObject(self.ghostAngle)
         
    def removeGhosts(self):
        removeObjects = []
        if self.ghostPoint != None:
            removeObjects += [self.ghostPoint]
        if self.ghostDistance != None:
            removeObjects += [self.ghostDistance]
        if self.ghostAngle != None:
            removeObjects += [self.ghostAngle]
        self.prototypeManager.removeObjects(removeObjects)
        self.ghostPoint = None
        self.ghostDistance = None
        self.ghostAngle = None
     
    def handleMouseRelease(self, mouseEvent, selection):
        pass
    
    def cleanUp(self):
        """ Cleanup the angle constraint when cancelled or finished """ 
        # Rick 20090519
        self.removeGhosts()
        if self.distanceSelected != None:
            self.distanceSelected = False
            self.distanceSelected = None
        if self.pointBegin != None:
            self.pointBegin.selected = False
            self.pointBegin = None
        if self.pointMiddle != None:
            self.pointMiddle.selected = False
            self.pointMiddle = None
        if self.pointEnd != None:
            self.pointEnd.selected = False
            self.pointEnd = None
        
class MoveTool(Tool):
    def __init__(self):
        Tool.__init__(self)   
        self.toolType = ToolType.MOVE
        self.needPicking = True
        self.lastPosition = Vec([0.0, 0.0, 0.0])
        self.selectionStarted = False
        self.beginSelPoint = QtCore.QPoint()
        self.endSelPoint = QtCore.QPoint()
        self.holdShift = False
        self.multipleSelect = True
            
    def manipulate(self):
        pass
        
    def handleMousePress(self, mouseEvent, camera, viewportType, selection): 
        # check if we have a hit
        if self.beginSelPoint.isNull():
            self.beginSelPoint.setX(mouseEvent.x())
            self.beginSelPoint.setY(mouseEvent.y())
        self.prototypeManager.showAxis = False
        
        if selection != -1:
            if len(selection[0]) > 1:
                self.prototypeManager.axis.selected = True
                self.prototypeManager.axis.selectionId = selection[0][1]
            elif len(selection[-1]) > 1:
                self.prototypeManager.axis.selected = True
                self.prototypeManager.axis.selectionId = selection[-1][1]
            else:
                self.prototypeManager.axis.selected = False
                
            if self.holdShift:
                self.prototypeManager.changeSelection(selection)
            elif not self.prototypeManager.axis.selected:
                self.prototypeManager.setSelectedObject(selection)
            else:
                self.prototypeManager.setSelectedObject(selection, False, False)

        elif selection == -1 and not self.holdShift:
            self.prototypeManager.deselectAllObjects()
            self.prototypeManager.axis.selected = False
            self.prototypeManager.axis.selectionId = 0

        self.needUpdate = True

    def handleMouseMove(self, mouseEvent, camera, viewportType, selection):
        self.needUpdate = False
            
        newPos = Vec(camera.unprojectedCoordinatesOf([mouseEvent.x(), mouseEvent.y(), 1.0]))
        translation = newPos - self.lastPosition
                
        selectedObjs = self.prototypeManager.getSelectedObjects()
        pointObjs = filter(lambda x:x.objType == ObjectType.POINT or x.objType == ObjectType.FIXED_POINT, selectedObjs)
            
        if mouseEvent.buttons() == QtCore.Qt.LeftButton:
            if len(pointObjs) > 0 and not self.selectionStarted:
                if viewportType == ViewportType.FRONT:
                    if self.prototypeManager.axis.selectionId == 1:
                        translation[1] = 0.0
                        translation[2] = 0.0
                    elif self.prototypeManager.axis.selectionId == 2:
                        translation[0] = 0.0
                        translation[2] = 0.0
                    else:
                        translation[2] = 0.0
                elif viewportType == ViewportType.SIDE: 
                    if self.prototypeManager.axis.selectionId == 2:
                        translation[0] = 0.0
                        translation[2] = 0.0
                    elif self.prototypeManager.axis.selectionId == 3:
                        translation[0] = 0.0
                        translation[1] = 0.0
                    else:
                        translation[0] = 0.0
                elif viewportType == ViewportType.TOP: 
                    if self.prototypeManager.axis.selectionId == 1:
                        translation[1] = 0.0
                        translation[2] = 0.0
                    elif self.prototypeManager.axis.selectionId == 3:
                        translation[0] = 0.0
                        translation[1] = 0.0
                    else:
                        translation[1] = 0.0
                        
                elif viewportType == ViewportType.PERSPECTIVE:
                    translation *= 0.3
                    if self.prototypeManager.axis.selectionId == 1:
                        translation[1] = 0.0
                        translation[2] = 0.0
                    elif self.prototypeManager.axis.selectionId == 2:
                        translation[0] = 0.0
                        translation[2] = 0.0
                    elif self.prototypeManager.axis.selectionId == 3:
                        translation[0] = 0.0
                        translation[1] = 0.0
                        
                for pointObj in pointObjs:
                    pointObj.updatePosition(translation)
            else:
                self.endSelPoint.setX(mouseEvent.x())
                self.endSelPoint.setY(mouseEvent.y())
                self.selectionStarted = True
                                
                if selection != -1 and not self.prototypeManager.axis.selected:
                    self.prototypeManager.setSelectedObjects(selection, True, True)
                elif selection == -1 and not self.prototypeManager.axis.selected:
                    self.prototypeManager.deselectAllObjects(True, True)
        else:
            if selection != -1:
                if len(selection[0]) > 1:
                    self.prototypeManager.axis.selected = True
                    self.prototypeManager.axis.selectionId = selection[0][1]
                elif len(selection[-1]) > 1:
                    self.prototypeManager.axis.selected = True
                    self.prototypeManager.axis.selectionId = selection[-1][1]

        self.lastPosition[0] = newPos[0]
        self.lastPosition[1] = newPos[1]
        self.lastPosition[2] = newPos[2]
        self.needUpdate = True    
           
    def handleMouseRelease(self, mouseEvent, selection):
        self.beginSelPoint.setX(0)
        self.beginSelPoint.setY(0)
        self.endSelPoint.setX(0)
        self.endSelPoint.setY(0)
        self.prototypeManager.convertTemporySelection()
        self.selectionStarted = False
        selectedObjs = self.prototypeManager.getSelectedObjects()
        pointObjs = filter(lambda x:x.objType == ObjectType.POINT or x.objType == ObjectType.FIXED_POINT, selectedObjs)
        
        if len(pointObjs) > 0:
            self.prototypeManager.showAxis = True
            self.prototypeManager.axis.updatePosition(pointObjs[0].position)
        
        if selection != -1:
            if len(selection[0]) == 0 and len(selection[-1]) == 0:
                self.prototypeManager.axis.selected = False
        
        self.needUpdate = True
        
    def handleKeyPress(self, keyEvent):
        if keyEvent.key() == QtCore.Qt.Key_Delete:
            self.prototypeManager.deleteSelectedObjects()
        if keyEvent.key() == QtCore.Qt.Key_Shift:
            self.holdShift = True
    
    def handleKeyRelease(self, keyEvent):
        if keyEvent.key() == QtCore.Qt.Key_Shift:
            self.holdShift = False

class ConnectTool(Tool):
    """ Connects two or more prototype objects. At this moment two different points can be connected, where the constraints
    are reassigned from the old point to the new one. """

    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.CONNECT
        self.needPicking = True
        self.selectedObjects = []

    def manipulate(self):
        pass
    
    def handleMousePress(self, mouseEvent, camera, viewportType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
            self.selectSelectedObjects()
            if self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT:
                self.selectedObjects += [self.prototypeManager.objectSelected]
                
        elif selection == -1:
            self.selectedObjects = []
            self.prototypeManager.deselectObject()
                    
        self.handleConnection()
        self.needUpdate = True
    
    def handleConnection(self):
        """ Handles the connection of two or more objects """
        connectedPoints = filter(lambda x:x.objType == ObjectType.POINT or x.objType == ObjectType.FIXED_POINT, self.selectedObjects)
        """ Connection of two arbitraty points """
        if len(connectedPoints) == 2:
            self.prototypeManager.replaceConstrainedObject(connectedPoints[0], connectedPoints[1])
            self.selectedObjects = []
    
    def handleMouseMove(self, mouseEvent, camera, viewportType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
            self.selectSelectedObjects()
        if selection != -1 and self.prototypeManager.objectSelected != None and (
           self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT):
            selectedObject = self.prototypeManager.objectSelected
            selectedObject.selected = True
            self.needUpdate = True
        elif self.prototypeManager.objectSelected != None:
            self.prototypeManager.deselectObject()
            self.selectSelectedObjects()
            self.needUpdate = True
    
    def selectSelectedObjects(self):
        for obj in self.selectedObjects:
            obj.selected = True
                    
    def handleMouseRelease(self, mouseEvent, selection):
        pass

class DisconnectTool(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.toolType = ToolType.DISCONNECT
        self.needPicking = True
        self.selectedObjects = []

    def manipulate(self):
        pass
    
    def handleMousePress(self, mouseEvent, camera, viewportType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
            if self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT:
                self.selectedObjects += [self.prototypeManager.objectSelected]
                
        elif selection == -1:
            self.selectedObjects = []
            self.prototypeManager.deselectObject()
                    
        self.handleDisconnection()
        self.needUpdate = True
    
    def handleDisconnection(self):
        connectedPoints = filter(lambda x:x.objType == ObjectType.POINT or x.objType == ObjectType.FIXED_POINT, self.selectedObjects)
        """ Connection of two arbitraty points """
        if len(connectedPoints) == 2:
            self.prototypeManager.replaceConstrainedObject(connectedPoints[0], connectedPoints[1])
    
    def handleMouseMove(self, mouseEvent, camera, viewportType, selection):
        if selection != -1:
            self.prototypeManager.setSelectedObject(selection)
        if selection != -1 and self.prototypeManager.objectSelected != None and (
           self.prototypeManager.objectSelected.objType == ObjectType.POINT or self.prototypeManager.objectSelected.objType == ObjectType.FIXED_POINT):
            selectedObject = self.prototypeManager.objectSelected
            selectedObject.selected = True
            self.needUpdate = True
        elif self.prototypeManager.objectSelected != None:
            self.prototypeManager.deselectObject()
            self.needUpdate = True
            
    def handleMouseRelease(self, mouseEvent, selection):
        pass
