from includes import *
from camera import *
from geosolver.matfunc import Vec

class CameraHandler(QtCore.QObject):
	""" The camerahandler handles the rotation, translation, zooming, fitting and other actions of the camera. """
	def __init__(self, glViewport, parent = None):
		""" Initialization of the camerhandler.
		
		Parameters:
			glViewport: the viewport which is controlled by the camera 
			parent: parent of the camerahandler
		"""
			
		QtCore.QObject.__init__(self, parent)
		self.resolvePoint = Vec([0.0, 0.0, 0.0])
		self.lastMousePos = QtCore.QPoint(0,0)
		self.lastMousePosOnSphere = Vec([0.0, 0.0, 0.0])
		self.activeMouseAction = None
		self.glViewport = glViewport
		self.spinningQuaternion = Quaternion()

	def mouseMoveEvent(self, mouseEvent, camera):
		""" Handle the camera when there is a mousemove event. This can result in different actions, dependent on the chosen action by the user.
		
		Parameters:
			mouseEvent - mouse event, which contains the current position in the view
			camera - the camera for which the action must be handled
		"""
		dx = mouseEvent.x() - self.lastMousePos.x()
		dy = mouseEvent.y() - self.lastMousePos.y()
		proj = self.projectToTrackball(camera, mouseEvent.x(), mouseEvent.y())
		
		if self.activeMouseAction == None:
			pass
		elif self.activeMouseAction == MouseAction.TRANSLATE:
			if mouseEvent.buttons() == self.glViewport.getMouseState(self.activeMouseAction):
				self.handleMouseMove(camera, dx, dy)
		elif self.activeMouseAction == MouseAction.ZOOM:
			if mouseEvent.buttons() == self.glViewport.getMouseState(self.activeMouseAction):
				self.handleMouseZoom(camera, dx, dy)
		elif self.activeMouseAction == MouseAction.ROTATE:
			if mouseEvent.buttons() == self.glViewport.getMouseState(self.activeMouseAction):
				self.handleMouseRotate(camera, mouseEvent.x(), mouseEvent.y(), dx, dy, proj)	
		elif self.activeMouseAction == MouseAction.FIT:
			if mouseEvent.buttons() == self.glViewport.getMouseState(self.activeMouseAction):
				self.handleFit(camera)
				
		self.lastMousePosOnSphere = proj		
		self.lastMousePos.setX(mouseEvent.pos().x())
		self.lastMousePos.setY(mouseEvent.pos().y())

	def handleMouseMove(self, camera, dx, dy):
		""" Handle the translation of the camera based on the current and last mouse position.
		
		Parameters:
			camera - the camera that needs to be translated
			dx - current x mouseposition in the view
			dy - current y mouseposition in the view
		"""
		translation = Vec([dx, -dy, 0.0])
		if camera.getCameraType() == CameraType.PERSPECTIVE:
			#check = camera.coordinatesOf([0.0,0.0,0.0])
			#print "check: " , check[2]
			#choke = 2.0 * math.tan(check[2]) / camera.getScreenHeight()
			
			#print "choke: " , choke
			#translation *= choke
			#print translation
			translation[0] *= 2.0
			translation[1] *= 2.0
			#cameraPos[2] += dy*trans
		else:
			cameraPos = camera.getPosition()
			translation[1] *= 2.0
			translation[0] *= 2.0

		self.translate(camera, translation)

	def handleMouseZoom(self, camera, dx, dy):
		""" Handle the zooming of the camera based on the current and last mouse position.
		
		Parameters:
			camera - the camera that needs to zoom
			dx - difference between the last and current x mouse position
			dy - difference between the last and current y mouse position
		"""
		self.translate(camera, Vec([0.0, 0.0, dy*2.0]))
			
	def handleMouseRotate(self, camera, newMouseX, newMouseY, dx, dy, projection):
		""" Handle the rotation of the camera based on the current and last mouse position.
		
		Parameters:
			camera - the camera that needs to be rotated
			newMouseX - current x mouseposition in the view
			newMouseY - current y mouseposition in the view
			dx - difference between the last and current x mouse position
			dy - difference between the last and current y mouse position
			projection - projection of the mouseposition on a trackball
		"""
		#camera.orientation = camera.orientation * rotQuat
		self.translate(camera, Vec([dx, dy, 0.0]))
		camera.lookAt(self.resolvePoint)
		#print "position: ",camera.getPosition()
		#print "orientation: ",camera.getOrientation()
		#print "revolvepoint: ",self.resolvePoint

	
	def projectToTrackball(self, camera, newX, newY):
		""" Project the mouseposition onto a trackball to rotate the camera.
		
		Parameters:
			newX - new x position on the trackball
			newY - new y position on the trackball
		
		Return:
			vector - position on the trackball
		"""
		x = newX / (camera.getWindowWidth() / 2.0)
		y = newY / (camera.getWindowHeight() / 2.0)
		x = x -1
		y = 1-y
		z2 = 1 - (x * x + y * y)
		z = 0.0
		if z2 > 0 :
			z = math.sqrt(z2)
		#print " x, y, z on sphere: " , x, y, z
		p = Vec([x,y,z])
		p.normalize()
		return p
	
	def rotationFromMove(self, vFrom, vTo):
		rotAxis = vTo.cross(vFrom)
		d = Vec(vFrom - vTo)
		t = d.norm()/(2.0*1.0)
		phi = 2.0*math.asin(t)
		rotQuat = Quaternion()
		rotQuat.fromAxisAngle(rotAxis, phi)
		rotQuat.normalize()
		return rotQuat

	def mouseWheelEvent(self, event, camera):
		pass

	def mouseReleaseEvent(self, event, camera):
		pass

	def handleFit(self, camera):
		center = camera.getSceneCenter()
		radius = camera.getSceneRadius()
		distance = 0.0
		cameraType = camera.getCameraType()
		if cameraType == CameraType.PERSPECTIVE:
			yView = radius / math.sin(camera.getFieldOfView()/2.0)
			xView = radius / math.sin(camera.getHorizontalFov()/2.0)
			if xView >= yView:
				distance = xView
			else:
				distance = yView
		elif cameraType == CameraType.ORTHOGRAPHIC:
			distance = ((center - camera.getRevolveAroundPoint()) * camera.getViewDirection()) + (radius/camera.orthoCoef)
			
		position = Vec(center-distance * camera.getViewDirection())
		
		camera.setPosition(position)

	"""slot"""
	def setActiveMouseaction(self, action):
		self.activeMouseAction = action

	def translate(self, camera, translation):
		pos = camera.getPosition()
		trans = camera.getOrientation().rotate(translation)
		pos[0] += trans[0]
		pos[1] += trans[1]
		pos[2] += trans[2]

	def spin(self, camera):
		self.rotateAroundPoint(camera, self.spinningQuaternion, camera.getRevolveAroundPoint())

	def rotateAroundPoint(self, camera, spinQuat, point):
		cameraOrientation = camera.getOrientation()
		cameraOrientation *= spinQuat
  		cameraOrientation.normalize()
		
		
		tempQuat = Quaternion()
		tempQuat.fromAxisAngle(spinQuat.axis(), spinQuat.angle())
		#print "pos: ", camera.getPosition(), " point: ", point
  		translation = point + tempQuat.rotate(camera.getPosition()-point) - camera.getPosition()
		pos = camera.getPosition()
 		pos[0] += translation[0]
		pos[1] += translation[1]
		pos[2] += translation[2]

	def getMainWindow(self):
		""" Return the main window. """
		return self.glViewport.getMainWindow()
