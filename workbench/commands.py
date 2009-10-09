from includes import *
from geosolver.matfunc import Vec
from LinearAlgebra import *
from camera import CameraType
from prototypeObjects import PrototypeManager

class Command:
	""" Commands that are general to the whole scene can be subclassed from this class. """
	def __init__(self):
		""" initialize """
		pass
		
	def execute(self):
		""" execute the command """
		raise NotImplementedError(caller + ' must be implemented in subclass')

class UpdateTaskbarCommand(Command):
	""" Update the taskbar whena mouse move event occurs in on of the many views/viewports. """
	def __init__(self, glViewport, mainWindow):
		Command.__init__(self)
		self.mainWindow = mainWindow
		self.glViewport = glViewport

	def execute(self, mouseEvent):
		""" Process the mouse move event and update the text in the taskbar 
		
		Parameters:
			mouseEvent: new position of the mouse in 2D
		"""
		camera = self.glViewport.getCamera()
		""" convert the 2D viewport coordinates into 3D projected on a Y-plane in 3D and
		for the other viewports to the orthogonal plane. """
		translation = Vec(camera.unprojectedCoordinatesOf([mouseEvent.x(), mouseEvent.y(), 1.0]))
		if camera.getCameraType() == CameraType.PERSPECTIVE:
			position = camera.getPositionOnYPlane(translation)	
		else:
			position = translation
		
		self.glViewport.mousePosition[0] = position[0]
		if self.glViewport.viewportType == ViewportType.SIDE:
			position[0] = 0.0
		self.glViewport.mousePosition[1] = position[1]
		if self.glViewport.viewportType == ViewportType.TOP:
			position[1] = 0.0
		self.glViewport.mousePosition[2] = position[2]
		if self.glViewport.viewportType == ViewportType.FRONT:
			position[2] = 0.0
			
		""" Update the text of the statusbar """
		translation[0] = "%.4f" % position[0]
		translation[1] = "%.4f" % position[1]
		translation[2] = "%.4f" % position[2]
		text = QtCore.QString("x:%1, y:%2, z:%3").arg(position[0]).arg(position[1]).arg(position[2])
		self.mainWindow.statusBar().showMessage(text)

class UpdateTextInTaskbarCommand(Command):
	def __init__(self, prototypeManager, mainWindow):
		Command.__init__(self)
		self.mainWindow = mainWindow
		self.prototypeManager = prototypeManager
		
	def execute(self):
		constraintInfo = ""
		constraintInfo = self.prototypeManager.getConstraintInfoAsText()
		print constraintInfo
		self.mainWindow.statusSolveInfo.setText(constraintInfo)

class UpdateToolCommand(Command):
	""" Update the tools which can be used in any of the viewports, the tool is set for the all
	the viewports. """
	def __init__(self, viewportManager):
		Command.__init__(self)
		self.viewportManager = viewportManager
		
	def execute(self, tool):
		""" Update a tool to a new tool
		
		Parameters:
			tool = new tool which the user has selected
		"""
		if self.viewportManager.displayViewport == DisplayViewport.ALL:
			for viewport in self.viewportManager.viewportList:
				viewport.glViewport.currentTool = tool
				for action in viewport.editGroup.actions():
					action.setChecked(False)
		else:
			self.viewportManager.viewport.glViewport.currentTool = tool
			for action in self.viewportManager.viewport.editGroup.actions():
					action.setChecked(False)
		PrototypeManager().deselectObject()
		self.viewportManager.updateViewports()
			
class UpdateActionCommand(Command):
	""" If an action for one of the viewports is set, disable all the tools for all of the windows. """
	def __init__(self, mainWindow):
		Command.__init__(self)
		self.mainWindow = mainWindow
		
	def execute(self, glViewport):
		actions = self.mainWindow.editGroup.actions()
		for action in actions:
			action.setChecked(False)
		
		if self.mainWindow.viewportManager.displayViewport == DisplayViewport.ALL:
			for viewport in self.mainWindow.viewportManager.viewportList:
				viewport.glViewport.currentTool = None
		else:
			glViewport.currentTool = None

class SaveCommand(Command):
	""" Save the file for all the objects in the scene. """		
	def __init__(self, mainWindow):
		Command.__init__(self)
		self.mainWindow = mainWindow
		self.prototypeManager = PrototypeManager()
		
	def execute(self, filename):
		doc = QtXml.QDomDocument( "Geometric Constraints" )
		root = doc.createElement( "Objects" )
		doc.appendChild( root );

		for prtObject in self.prototypeManager.prtObjects:
			if not prtObject.ghost:
				root.appendChild(prtObject.save(doc))
		root.appendChild(self.prototypeManager.save(doc))
		
		file = QtCore.QFile(filename)
		if file.open(QtCore.QIODevice.WriteOnly): 
			ts = QtCore.QTextStream(file)
			ts << doc.toString()
			file.close()

class LoadCommand(Command):
	""" Load the objects from a file. """
	def __init__(self, mainWindow):
		Command.__init__(self)
		self.mainWindow = mainWindow
		self.prototypeManager = PrototypeManager()
		
	def execute(self, filename):
		doc = QtXml.QDomDocument( "Geometric Constraints" )
		file = QtCore.QFile(filename)

		if not file.open(QtCore.QIODevice.ReadOnly):
			raise StandardError, "File could not be opened"
			return
		
		""" Skip the first line, because we need the root of the objects not the document. """
		file.readLine()
		
		if not doc.setContent(file, False):
			file.close()
			raise StandardError, "Could not initialize the file"
			return
		file.close()
		
		root = doc.documentElement()

		if root.tagName() != "Objects":
			raise StandardError, "Invalid document"
			return

		self.prototypeManager.load(root)
		self.mainWindow.viewportManager.updateViewports()

class ImportCommand(Command):
	""" Import the objects from a file into the scene. """
	def __init__(self, mainWindow):
		Command.__init__(self)
		self.mainWindow = mainWindow
		self.prototypeManager = PrototypeManager()
		
	def execute(self, filename):
		doc = QtXml.QDomDocument( "Geometric Constraints" )
		file = QtCore.QFile(filename)

		if not file.open(QtCore.QIODevice.ReadOnly):
			raise StandardError, "File could not be opened"
			return
		
		""" Skip the first line, because we need the root of the objects not the document. """
		file.readLine()
		
		if not doc.setContent(file, False):
			file.close()
			raise StandardError, "Could not initialize the file"
			return
		file.close()
		
		root = doc.documentElement()

		if root.tagName() != "Objects":
			raise StandardError, "Invalid document"
			return

		self.prototypeManager.importScene(root)
		self.mainWindow.viewportManager.updateViewports()
		
class ClearSceneCommand(Command):
	""" Clear the whole scene of all the objects. """		
	def __init__(self, mainWindow):
		Command.__init__(self)
		self.mainWindow = mainWindow
		self.prototypeManager = PrototypeManager()
		
	def execute(self):
		self.prototypeManager.removeAllObjects()
		self.mainWindow.viewportManager.resetScene()
		self.mainWindow.viewportManager.updateViewports()
		self.mainWindow.saveFileName = QtCore.QString("")

