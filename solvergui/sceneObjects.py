from includes import *
"""# no more nasty rounding with integer divisions
from __future__ import division

import sys, pdb
from PyQt4 import QtCore, QtGui, QtOpenGL
"""
try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except ImportError:
	app = QtGui.QApplication(sys.argv)
	QtGui.QMessageBox.critical(None, "OpenGL grabber","PyOpenGL must be installed to run this example.",
					QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)
	sys.exit(1)

class SceneObject:
	def __init__(self,viewport):
		self.quadratic = gluNewQuadric()
		#gluQuadricNormals(self.quadratic, GLU_SMOOTH)
		#gluQuadricDrawStyle(self.quadratic, GLU_LINE)
		self.activeViewport = viewport

	def drawCylinder(self, orientation, position, radiusBottom, radiusTop, height):
		glPushMatrix()
		glColor3fv([0.0,1.0,1.0])
		glTranslatef(position[0], position[1], position[2])
		glRotatef(orientation[0], orientation[1], orientation[2], orientation[3])
		gluCylinder(self.quadratic, radiusBottom, radiusTop, height, 10, 10)
		glPopMatrix()		

	def drawSphere(self, pos, radius, reflectance=0.0):
		glPushMatrix()
		glTranslatef(pos[0], pos[1], pos[2])
		gluSphere(self.quadratic, radius, 10, 10)
		glPopMatrix()

	def drawRectangle(self, geometry):
		glPushMatrix()
		#print "left: " , geometry.left(), " right: ", geometry.right(), " bottom ", geometry.bottom(), " top: ", geometry.top()
		#glTranslatef(0.0,0.0,-199.0)
		glDisable(GL_LIGHTING)
		
		glRecti(geometry.left(), geometry.top(), geometry.right(), geometry.bottom())
		glEnable(GL_LIGHTING)
		glPopMatrix()
	
	def drawSelection(self, x1, y1, x2, y2):
		glPushMatrix()
		glTranslatef(0.0,0.0,-50.0)
		glDisable(GL_LIGHTING)
		glBegin(GL_LINE_STRIP)
		glVertex2f(x1, y1)
		glVertex2f(x1, y2)		
		glVertex2f(x2, y2)
		glVertex2f(x2, y1)
		glVertex2f(x1, y1)
		glEnd()
		glEnable(GL_LIGHTING)
		glPopMatrix()
		
	def drawBackgroundgrid3D(self, gridWidth, gridHeight, rectWidth, rectHeight, gridColor, filled=False):
		if rectWidth > 0 and rectHeight > 0:
			glPushMatrix()
			cameraPos = self.activeViewport.getCamera().getPosition()
			glDisable(GL_LIGHTING)
			#glEnable(GL_LINE_SMOOTH)
			leftRest = (-gridWidth/2) % rectWidth
			bottomRest = (-gridHeight/2) % rectHeight
			
			posX1Start = int((-gridWidth/2) - leftRest)
			posZ1Start = int((-gridHeight/2) - bottomRest)
			posX1 = posX1Start
	
			rangeX =  int(gridWidth / rectWidth) + 1
			rangeZ =  int(gridHeight / rectHeight) + 1
			
			glLineWidth(1.0)
			if filled:
				glRotatef(90.0, 1.0, 0.0, 0.0)
			for x in range (0, rangeX):
				if x != 0 and not filled:
					glEnd()
				if not filled:
					glBegin(GL_LINE_STRIP)
				posZ1 = posZ1Start
				for z in range(0, rangeZ):
					glColor3f(gridColor.redF(), gridColor.greenF(), gridColor.blueF())
					if(filled):
						if (x + z) % 2 == 0:
							glColor3f(1, 1, 1)
						else:
							glColor3f(0, 0, 1)
						glRectf(posX1, posZ1, posX1+rectWidth, posZ1+rectHeight)
					else:
						glVertex3f(posX1+rectWidth, 0, posZ1)
						glVertex3f(posX1, 0, posZ1)
						glVertex3f(posX1, 0, posZ1+rectHeight)
						glVertex3f(posX1+rectWidth, 0, posZ1+rectHeight)
						glVertex3f(posX1+rectWidth, 0, posZ1)					
					posZ1 += rectHeight
				posX1 += rectWidth
				
			if not filled:
				glEnd()	
			else:
				glRotatef(-90, 1.0, 0.0, 0.0)
			
			self.drawThickAxis(posX1Start, posX1Start+gridWidth+rectWidth, 0.0, 0.0, posZ1Start, posZ1Start+gridHeight+rectHeight, 2.0)
			#glDisable(GL_LINE_SMOOTH)
			glEnable(GL_LIGHTING)
			glPopMatrix()

	def drawBackgroundgrid2D(self, rectWidth, rectHeight, gridColor, filled=False):
		if rectWidth > 0 and rectHeight > 0:
			glPushMatrix()
			vpType = self.activeViewport.getViewportType()	
			camera = self.activeViewport.getCamera()
			cameraPos = camera.getPosition()
	
			leftPlaneSub = 0.0	
			bottomPlaneSub = 0.0
			if  vpType == ViewportType.FRONT:
				leftPlaneSub = cameraPos[0]
				bottomPlaneSub = cameraPos[1]
				inBack = camera.getFarPlane() - cameraPos[2]
				glTranslatef(0,0, -inBack)
			elif vpType == ViewportType.SIDE:
				leftPlaneSub = -cameraPos[2] 
				bottomPlaneSub = cameraPos[1]
				inBack = camera.getFarPlane() - cameraPos[0]
				glTranslatef(-inBack,0,0)
			elif vpType == ViewportType.TOP:
				leftPlaneSub = cameraPos[0]
				bottomPlaneSub = cameraPos[2]
				inBack = camera.getFarPlane() - cameraPos[1]
				glTranslatef(0,-inBack,0)
		
			glDisable(GL_LIGHTING)
	
			width = camera.getWindowWidth()
			height = camera.getWindowHeight()
			
			viewWidth = 0.0
			viewHeight = 0.0
			ratio = camera.getAspectRatio()
			
			if width >= height:
				viewWidth = 2*camera.getOrthoWidth()*ratio #rightplane -leftplane
				viewHeight = 2*camera.getOrthoHeight() # topplane - bottomplane
				leftPlane = -camera.getOrthoWidth()*ratio + leftPlaneSub # leftplane
				bottomPlane =  -camera.getOrthoHeight() + bottomPlaneSub # topplane
			else:
				viewWidth = 2*camera.getOrthoWidth()
				viewHeight = 2*camera.getOrthoHeight()*ratio
				leftPlane = -camera.getOrthoWidth() - leftPlaneSub
				bottomPlane =  -camera.getOrthoHeight()*ratio + bottomPlaneSub
			
			leftRest = leftPlane % rectWidth
			posLeft = (leftPlane - leftRest)
			bottomRest = bottomPlane % rectHeight
			posBottom = (bottomPlane - bottomRest)
			
			#print "width: ", viewWidth, " heihgt: ", viewHeight
			#rectWidthAdjustment = int(viewWidth/3000) + 1
			#rectHeightAdjustment = int(viewHeight/3000) + 1
			#rectWidth *= rectWidthAdjustment
			#rectHeight *= rectHeightAdjustment
			widthRange =  int(viewWidth / rectWidth) + 2
			heightRange =  int(viewHeight / rectHeight) + 2
			#print widthRange, heightRange
			if  vpType == ViewportType.FRONT:
				if filled:
					self.drawFilledGrid(posLeft, posBottom, widthRange, heightRange, rectWidth, rectHeight)
				else:
					self.drawOpenGrid(posLeft, posBottom, widthRange, heightRange, rectWidth, rectHeight, gridColor)
				self.drawThickAxis(posLeft, posLeft+viewWidth+rectWidth, posBottom, posBottom+viewHeight+rectHeight, 
									0.0, 0.0, 2.0)
			elif vpType == ViewportType.SIDE:
				glPushMatrix()
				glRotatef(90.0, 0.0 , 1.0, 0.0)
				
				if filled:
					self.drawFilledGrid(posLeft, posBottom, widthRange, heightRange, rectWidth, rectHeight)
				else:
					self.drawOpenGrid(posLeft, posBottom, widthRange, heightRange, rectWidth, rectHeight, gridColor)
				glPopMatrix() 
				self.drawThickAxis(0.0, 0.0, posBottom, posBottom+viewHeight+rectHeight, 
									-posLeft, -(posLeft+viewWidth+rectWidth), 2.0)
			elif vpType == ViewportType.TOP:
				glPushMatrix()
				glRotatef(90.0, 1.0 , 0.0, 0.0)
				if filled:	
					self.drawFilledGrid(posLeft, posBottom, widthRange, heightRange, rectWidth, rectHeight)
				else:
					self.drawOpenGrid(posLeft, posBottom, widthRange, heightRange, rectWidth, rectHeight, gridColor)
				glPopMatrix()
				self.drawThickAxis(posLeft, posLeft+viewWidth+rectWidth, 0.0, 0.0, 
									posBottom, (posBottom+viewHeight+rectHeight), 2.0)
			
			glEnable(GL_LIGHTING)
			glPopMatrix()
		
	def drawFilledGrid(self, startPosX, startPosY, rangeX, rangeY, rectWidth, rectHeight):
		posX = startPosX
		for x in range (0, rangeX):
			posY =  startPosY
			for y in range(0, rangeY):
				glColor3f(0, 0, 1)
				if (posX + posY) % 100 == 0:
					glColor3f(1, 1, 1)
				else:
					glColor3f(0, 0, 1)
				glRectf(posX, posY, posX+rectWidth, posY+rectHeight)
				posY += rectHeight
			posX += rectWidth

	def drawOpenGrid(self, startPosX, startPosY, rangeX, rangeY, rectWidth, rectHeight, gridColor):
		glLineWidth(0.5)
		posX = startPosX
		glColor3f(gridColor.redF(),gridColor.greenF(),gridColor.blueF())
		for x in range (0, rangeX):
			if x != 0:
				glEnd()
			glBegin(GL_LINE_STRIP)
			posY =  startPosY
			for y in range(0, rangeY):
				glVertex2f(posX+rectWidth, posY)
				glVertex2f(posX, posY)
				glVertex2f(posX, posY+rectHeight)
				glVertex2f(posX+rectWidth, posY+rectHeight)
					
				posY += rectHeight
			posX += rectWidth
		glEnd()	
	
	
	def drawThickAxis(self, beginX, endX, beginY, endY, beginZ, endZ, thickness):
		glLineWidth(thickness)
		glColor3f(0.25,0.5,0.25)
		# draw thick x axis
		glBegin(GL_LINES)
		glVertex3f(beginX, 0,0)
		glVertex3f(endX, 0,0)
		glEnd()
		
		# draw thick y axis
		glBegin(GL_LINES)
		glVertex3f(0, beginY,0)
		glVertex3f(0, endY,0)
		glEnd()

		# draw thick z axis
		glBegin(GL_LINES)
		glVertex3f(0, 0, beginZ)
		glVertex3f(0, 0, endZ)
		glEnd()
		glLineWidth(1.0)

	def testDraw(self, size):
		direction = 20.0
		glColor3f(0.5,0.5,0.5)
		position = [-direction, 0.0, -direction]
		self.drawSphere(position, size)
		position = [direction, 0.0, -direction]
		self.drawSphere(position, size)
		position = [direction, 0.0, direction]
		self.drawSphere(position, size)
		position = [-direction, 0.0, direction]
		self.drawSphere(position, size)
		glColor3f(0.7,0.0,0.5)
		position = [-direction*2, -10.0, direction]
		self.drawSphere(position, size)
		
		glColor3f(0.0,0.7,0.5)
		position = [-direction, direction*2, -direction]
		self.drawSphere(position, size)
		position = [direction, direction*2, -direction]
		self.drawSphere(position, size)
		position = [direction, direction*2, direction]
		self.drawSphere(position, size)
		position = [-direction, direction*2, direction]
		self.drawSphere(position, size)
		
		height = 40.0
		radius1 = size/4
		radius2 = size/4
		position = [-direction, 0.0, -direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [direction, 0.0, -direction]
		orientation = [90.0, 0.0, 0.0, 1.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [-direction, 0.0, -direction]
		orientation = [0.0, 0.0, 0.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [-direction, 0.0, direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)

		position = [-direction, direction*2, -direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [direction, direction*2, -direction]
		orientation = [90.0, 0.0, 0.0, 1.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [-direction, direction*2, -direction]
		orientation = [0.0, 0.0, 0.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [-direction, direction*2, direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)

		position = [-direction, direction*2, -direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [direction, direction*2, -direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		
		position = [-direction, direction*2, direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)
		position = [direction, direction*2, direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		self.drawCylinder(orientation,position,radius1, radius2, height)

	def testDrawWithNames(self, size):
		i = 0
		direction = 20.0
		glColor3f(0.5,0.5,0.5)
		position = [-direction, 0.0, -direction]
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		position = [direction, 0.0, -direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		position = [direction, 0.0, direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		position = [-direction, 0.0, direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		glColor3f(0.7,0.0,0.5)
		position = [-direction*2, -10.0, direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		
		glColor3f(0.0,0.7,0.5)
		position = [-direction, direction*2, -direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		position = [direction, direction*2, -direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		position = [direction, direction*2, direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		position = [-direction, direction*2, direction]
		i+=1
		glPushName(i)
		self.drawSphere(position, size)
		glPopName()
		
		height = 40.0
		radius1 = size/4
		radius2 = size/4
		position = [-direction, 0.0, -direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [direction, 0.0, -direction]
		orientation = [90.0, 0.0, 0.0, 1.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [-direction, 0.0, -direction]
		orientation = [0.0, 0.0, 0.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [-direction, 0.0, direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()

		position = [-direction, direction*2, -direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [direction, direction*2, -direction]
		orientation = [90.0, 0.0, 0.0, 1.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [-direction, direction*2, -direction]
		orientation = [0.0, 0.0, 0.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [-direction, direction*2, direction]
		orientation = [90.0, 0.0, 1.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()

		position = [-direction, direction*2, -direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [direction, direction*2, -direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		
		position = [-direction, direction*2, direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()
		position = [direction, direction*2, direction]
		orientation = [90.0, 1.0, 0.0, 0.0]
		i+=1
		glPushName(i)
		self.drawCylinder(orientation,position,radius1, radius2, height)
		glPopName()

	def testDraw2(self):
		glTranslatef(0.0, 0.0, -100.0)
		glColor3f(0.0,0.0,1.0)
		self.drawRectangle(QtCore.QRect(0.0, 0.0, 50.0, 50.0))	
		glColor3f(1.0,0.0,0.0)
		
		glTranslatef(0.0, 0.0, -100.0)
		#glRotatef(-90.0, 0.0,1.0,0.0)

		gluDisk(self.quadratic, 0.0, 10.0,10, 10)
		
		#gluCylinder(self.quadratic, 0.0, 25.0, 50.0, 10, 10)

	def drawXAxis(self, width=2.0, height=20.0):
		# x axis	
		glPushMatrix()
		glColor3fv([1.0,0.0,0.0])
		glTranslate(-1.0, 0.0, 0.0)
		glRotate(90, 0.0, 1.0 ,0.0)
		#glRotate(180, 1.0, 0.0, 0.0)
		gluCylinder(self.quadratic, width, width, height, 10, 10)
		glPushMatrix()
		glTranslatef(0.0,0.0,height)
		gluCylinder(self.quadratic, width*2.5, 0.0, height/5, 10, 10)
		#newFont = QtGui.QFont()
		#newFont.setStyleStrategy(QtGui.QFont.OpenGLCompatible) 
		#self.activeViewport.renderText(-4.0, 4.0, 6.0, 'X', newFont)
		glPopMatrix()
		glPopMatrix()

	def drawYAxis(self, width=2.0, height=20.0):
		# y axis
		glPushMatrix()
		glColor3fv([0.0,1.0,0.0])
		glRotate(90, 1.0, 0.0 ,0.0)
		gluCylinder(self.quadratic, width, width, height, 10, 10)
		glPushMatrix()
		glTranslatef(0.0,0.0,height)
		gluCylinder(self.quadratic, width*2.5, 0.0, height/5, 10, 10)
		
		#newFont = QtGui.QFont()
		#newFont.setStyleStrategy(QtGui.QFont.OpenGLCompatible) 
		#self.activeViewport.renderText(5.0, 10.0, 1.0, 'Y', newFont)
		#glEnable(GL_LIGHTING)
		glPopMatrix()
		glPopMatrix()

	def drawZAxis(self, width=2.0, height=20.0):
		# z axis
		glPushMatrix()
		glColor3fv([0.0,0.0,1.0])
		glRotate(180, 0.0, 1.0 ,0.0)
		gluCylinder(self.quadratic, width, width, height, 10, 10)
		glPushMatrix()
		glTranslatef(0.0,0.0,height)
		gluCylinder(self.quadratic, width*2.5, 0.0, height/5, 10, 10)
		#newFont = QtGui.QFont()
		#newFont.setStyleStrategy(QtGui.QFont.OpenGLCompatible) 
		#self.activeViewport.renderText(-4.0, 4.0, 6.0, 'Z', newFont)
		glPopMatrix()
		glPopMatrix()
	
