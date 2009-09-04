# no more nasty rounding with integer divisions
from __future__ import division
#import Numeric
import numpy.numarray as Numeric
from includes import *
from geosolver.matfunc import Vec
from quaternion import *
from prototypeObjects import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL grabber","PyOpenGL must be installed to run this example.",
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)
    sys.exit(1)

class CameraType:
        PERSPECTIVE, ORTHOGRAPHIC, OVERLAY = range(3)

class Camera:
    def __init__(self, glViewport, camType):
        self.cameraType = camType
        self.setScreenWidthAndHeight(800,600)
        self.farPlane = 2000.0
        self.nearPlane = 0.01
        self.zFarCoef = math.sqrt(3.0)
        self.zNearCoef = 0.005
        self.position = Vec([0.0, 0.0, 0.0])
        self.orientation = Quaternion()
        self.sceneCenter = Vec([0.0, 0.0, 0.0])
        self.target = self.sceneCenter
        self.upVec = Vec([0.0, 1.0, 0.0])
        self.sceneRadius = 1.0

        self.aspectRatio = 0.0
        self.cameraIsEdited = False
        self.fieldOfView = 45.0
        self.orthoCoef = math.tan(self.fieldOfView/2.0)
        self.sceneRadius = 300.0
        self.revolveAroundPoint = Vec([0.0, 0.0, 0.0])
        self.glViewport = glViewport
        self.modelViewMatrix = Numeric.identity(4)
                
    """Slots"""
    def cameraIsEdited(self):
        self.cameraIsEdited = True
        
    """Gets"""
    def getWindowWidth(self):
        return self.screenWidth
    
    def getWindowHeight(self):
        return self.screenHeight

    def getFarPlane(self):
        zFar = self.getDistanceToSceneCenter() + self.getZClippingCoefficient()*self.getSceneRadius()
        return zFar
    
    def getNearPlane(self):
        z = self.getDistanceToSceneCenter() - self.getZClippingCoefficient() * self.getSceneRadius()
        zMin = self.getZNearCoefficient() * self.getZClippingCoefficient() * self.getSceneRadius()

        if z < zMin:
            if self.cameraType == CameraType.PERSPECTIVE:
                z = zMin
            elif self.cameraType == CameraType.ORTHOGRAPHIC:
                z = 0.0
        return z

    def getPosition(self):
        return self.position
    
    def getCameraType(self):
        return self.cameraType

    def getScreenWidth(self):
        return self.screenWidth

    def getScreenHeight(self):
        return self.screenHeight

    def getAspectRatio(self):
        return self.screenWidth/self.screenHeight
    
    def getFieldOfView(self):
        return self.fieldOfView
    
    def getHorizontalFov(self):
        return 2.0 * math.atan(math.tan(self.getFieldOfView()/2.0) * self.getAspectRatio())
        
    def getOrthoWidth(self):
        revolvePoint = self.coordinatesOf(self.getRevolveAroundPoint())
        dist = self.orthoCoef * math.fabs(revolvePoint[2])
        if self.getAspectRatio() < 1.0:
            return dist 
        else:
            return dist * self.getAspectRatio()
            
    def getOrthoHeight(self):
        revolvePoint = self.coordinatesOf(self.getRevolveAroundPoint())
        dist = self.orthoCoef * math.fabs(revolvePoint[2])
        if self.getAspectRatio() < 1.0:
            return dist * 1.0/self.getAspectRatio()
        else:
            return dist

    def getSceneCenter(self):
        return self.sceneCenter

    def getCameraType(self):
        return self.cameraType

    def getOrientation(self):
        return self.orientation
    
    def getSceneRadius(self):
        return self.sceneRadius

    def getRevolveAroundPoint(self):
        return self.revolveAroundPoint

    def getDistanceToSceneCenter(self):
        sceneCenter = self.coordinatesOf(self.getSceneCenter())
        return math.fabs(sceneCenter[2])

    def getZClippingCoefficient(self):
        return self.zFarCoef

    def getZNearCoefficient(self):
        return self.zNearCoef
    
    def getSceneRadius(self):
        return self.sceneRadius

    def getViewport(self):
        viewport = Numeric.array([0, self.getScreenHeight(), self.getScreenWidth(), -self.getScreenHeight()])
        return viewport
    
    def getViewDirection(self):
        return Vec([0.0, 0.0, -1.0])
        
    """Sets"""
    def setScreenWidthAndHeight(self, width, height):
        self.screenWidth = width
        self.screenHeight = height
        self.setAspectRatio(width, height)
        
    def setAspectRatio(self, width, height):
        if height == 0:
            height = 1
        if self.screenWidth >= self.screenHeight:
            self.aspectRatio = width/height
        else:
            self.aspectRatio = height/width

    def setFieldOfView(self, fov):
        self.fieldOfView = fov

    def setPosition(self, position):
        self.position = Vec(position)

    def setUpVec(self, upVec):
        self.upVec = upVec
    
    def setSceneCenter(self, sceneCenter):
        self.sceneCenter = sceneCenter

    def setOrientation(self, qOrientation):
        self.orientation = qOrientation

    def setAltOrientation(self, qOrientation):
        #print "setAltOrientation",qOrientation
        deltaQ = self.orientation.inverse() * qOrientation
        deltaQ.normalize()
        self.setOrientation(self.orientation*deltaQ)
        self.orientation.normalize()
        
    """ Projection / Modelview """
    def computeModelView(self):
        self.orientation.getRotationMatrix(self.modelViewMatrix)
        #print self.orientation.quaternion
        v = Vec([0.0, 0.0, 0.0])
        v = self.orientation.inverseRotate(self.position)
        
        self.modelViewMatrix[3][0] = -v[0]
        self.modelViewMatrix[3][1] = -v[1]
        self.modelViewMatrix[3][2] = -v[2]
        self.modelViewMatrix[3][3] = 1.0
        
    def loadProjection(self, reset=True):
        glMatrixMode(GL_PROJECTION)
        if reset == True:
            glLoadIdentity()
        
        if self.getCameraType() == CameraType.PERSPECTIVE:
            gluPerspective(180.0*self.getFieldOfView()/math.pi, self.getAspectRatio(), self.getNearPlane(), self.getFarPlane())
        elif self.getCameraType() == CameraType.ORTHOGRAPHIC:
            if self.getOrthoWidth() >= self.getOrthoHeight():
                glOrtho(-self.getOrthoWidth(), self.getOrthoWidth(), 
                        -self.getOrthoHeight(), self.getOrthoHeight(), self.getNearPlane(), self.getFarPlane())
            elif self.getOrthoWidth() < self.getOrthoHeight():
                glOrtho(-self.getOrthoWidth(), self.getOrthoWidth(), -self.getOrthoHeight(),
                        self.getOrthoHeight(), self.getNearPlane(), self.getFarPlane())
        #elif self.getCameraType() == CameraType.OVERLAY:
        #    glOrtho(0, self.getScreenWidth(), 0, self.getScreenHeight(), -0.1, 100.0)

    def loadModelView(self):
        glMatrixMode(GL_MODELVIEW)
        self.computeModelView()
        glLoadMatrixd(self.modelViewMatrix)
        #glLoadIdentity()
        #print "position[x,y,z]: ", self.position[0], self.position[1], self.position[2], " target: ", self.target[0], self.target[1], self.target[2], " upvector: ", self.upVec[0], self.upVec[1], self.upVec[2]
        #if not self.getCameraType() == CameraType.OVERLAY:
        #    gluLookAt(self.position[0], self.position[1], self.position[2], 
        #              self.target[0], self.target[1], self.target[2], 
        #              self.upVec[0], self.upVec[1], self.upVec[2])

    def lookAt(self, target):
        self.target = target
        # print target, self.getPosition()
        self.setViewDirection(target - self.getPosition())
        
    def setViewDirection(self, direction):
        if direction.normSquared() < 1E-10:
            return

        xAxis = Vec(direction.cross(self.upVec))
        if xAxis.normSquared() < 1E-10:
            xAxis = Vec([1.0, 0.0, 0.0])
        #piet = xAxis.cross(direction)
        #print "xAxis: ", xAxis, " direction: ", direction, " cross: " , piet
        q = Quaternion()
        q.setFromRotatedBasis(xAxis, xAxis.cross(direction), -direction)
        self.setAltOrientation(q)

    def printPosition(self):
        print "Camera Position(x, y, z): ", self.position[0], self.position[1], self.position[2]

    def coordinatesOf(self, src):
        tempCoOf = Vec([0.0,0.0,0.0])
        tempCoOf[0] = src[0] - self.position[0]
        tempCoOf[1] = src[1] - self.position[1]
        tempCoOf[2] = src[2] - self.position[2]
        return self.getOrientation().inverseRotate(tempCoOf)

    def projectedCoordinatesOf(self, src):
        # Rick 20090311 - gives "Projection failed" error using pyopengl 3.0.2
        # projCoord = gluProject(src[0],src[1],src[2],self.modelViewMatrix, None, None)
        # and this doesn't give the correct result (y coords flipped)
        # projCoord = gluProject(src[0],src[1],src[2], None, None, None)
        model = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj = glGetDoublev(GL_PROJECTION_MATRIX)
        # Rick 20090519 - okay this is weird, on my work system I need to use GL_VIEWPORT
        # but on my home system I need to use getViewPort (different viewport coordinates!) 
        view = glGetIntegerv(GL_VIEWPORT)
        #view = self.getViewport()
        #print "before gluProject"
        #print "model=",model
        #print "proj=",proj
        #print "view=",view
        projCoord = gluProject(src[0],src[1],src[2], model, proj, view)
        return projCoord;

    def unprojectedCoordinatesOf(self, src):
        # Rick 20090311 - gives "Projection failed" error using pyopengl 3.0.2
        # unProjCoord = gluUnProject(src[0],src[1],src[2],self.modelViewMatrix, None, self.getViewport())
        # and this doesn't give the correct result (y coords flipped)
        # UnProjCoord = gluProject(src[0],src[1],src[2], None,None,None)
        model = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj = glGetDoublev(GL_PROJECTION_MATRIX)
        # Rick 20090519 - okay this is weird, on my work system I need to use GL_VIEWPORT
        # but on my home system I need to use getViewPort (different viewport coordinates!) 
        view = glGetIntegerv(GL_VIEWPORT)
        #view = self.getViewport()
        #print "before gluUnProject"
        #print "src = ",src
        #print "model=",model
        #print "proj=",proj
        #print "view=",view
        unProjCoord = gluUnProject(float(src[0]),float(src[1]),float(src[2]), model, proj, view)
        #print "unProjCoord = ",unProjCoord
        return unProjCoord

    def getPositionOnXPlane(self, pointPosition):
        positionOnPlane = Vec([0.0, 0.0, 0.0])
        if self.position[0] == pointPosition[0]:
            t = -pointPosition[0]
        else:
            t = -pointPosition[0] / (self.position[0] - pointPosition[0])
        positionOnPlane[1] = self.position[1]*t + (1-t)*pointPosition[1]
        positionOnPlane[2] = self.position[2]*t + (1-t)*pointPosition[2]

        return positionOnPlane

    def getPositionOnYPlane(self, pointPosition):
        positionOnPlane = Vec([0.0, 0.0, 0.0])
        #print "  camera position: ", self.position[0], self.position[1], self.position[2]
        if self.position[1] == pointPosition[1]:
            t = -pointPosition[1]
        else:
            t = -pointPosition[1] / (self.position[1] - pointPosition[1])
        positionOnPlane[0] = self.position[0]*t + (1-t)*pointPosition[0]
        positionOnPlane[2] = self.position[2]*t + (1-t)*pointPosition[2]

        return positionOnPlane
    
    def getPositionOnZPlane(self, pointPosition):
        positionOnPlane = Vec([0.0, 0.0, 0.0])
        if self.position[2] == pointPosition[2]:
            t = -pointPosition[2]
        else:
            t = -pointPosition[2] / (self.position[2] - pointPosition[2])
        positionOnPlane[0] = self.position[0]*t + (1-t)*pointPosition[0]
        positionOnPlane[1] = self.position[1]*t + (1-t)*pointPosition[1]

        return positionOnPlane
        
    def setSceneRadius(self, radius):
        self.setFocusDistance(self.sceneRadius / math.tan(self.fieldOfView/2.0))
        self.sceneRadius = radius

    def setFocusDistance(self, distance):
        self.focusDistance = distance

    def setSceneCenter(self, center):
        self.sceneCenter = center
        self.setRevolveAroundPoint(self.sceneCenter)
    
    def setRevolveAroundPoint(self, point):
        prevDist = math.fabs(self.coordinatesOf(self.revolveAroundPoint[2]))
        self.revolveAroundPoint = point
        newDist = math.fabs(self.coordinatesOf(self.revolveAroundPoint[2]))

        if (prevDist > 1E-9) and (newDist > 1E-9):
            self.orthoCoef *= prevDist / newDist

        

        
