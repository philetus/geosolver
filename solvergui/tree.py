from includes import *
from parameters import Settings

class Tree:
	def __init__(self, root):
		self.settings = Settings()
		self.orientation = self.settings.dvData.treeAlignment
		self.maxDepth = 100
		self.siblingSeperation = 5
		self.subtreeSeperation = 5
		self.levelSeperation = 40
		self.maxLevelHeight = []
		self.maxLevelWidth = []
		self.previousLevelNode = []
		self.root = None
		self.topXAdjustment = 0
		self.topYAdjustment = 0
		self.rootOffset = QtCore.QPoint()
		
	def firstWalk(self, tree, node, level):
		leftSibbling = None
		node.position.setX(0.0)
		node.position.setY(0.0)
		node.leftNeighbour = None
		node.rightNeighbour = None
		tree.setLevelHeight(node, level)
		tree.setLevelWidth(node, level)
		tree.setNeighbours(node, level)
		
		if (node.getChildrenCount() == 0) or (level == tree.maxDepth):
			leftSibling = node.getLeftSibling()
			if leftSibling != None:
				node.prelim = leftSibling.prelim + tree.getNodeSize(leftSibling) + tree.siblingSeperation
			else:
				node.prelim = 0.0
		else:
			for chldNode in node.children:
				self.firstWalk(tree, chldNode, level+1)
		
		midPoint = node.getChildrenCenter(tree)
		midPoint -= tree.getNodeSize(node)/2.0
		leftSibling = node.getLeftSibling()
		if leftSibling != None:
			node.prelim = leftSibling.prelim + tree.getNodeSize(leftSibling) + tree.siblingSeperation
			node.modifier = node.prelim - midPoint
			self.apportion(tree, node, level)
		else:
			node.prelim = midPoint
		
	def apportion(self, tree, node, level):
		k = tree.maxDepth - level
		j = 1
		
		if node.getChildrenCount() != 0: 
			firstChild = node.children[0]
			firstChildLeftNeighbour = node.children[0].leftNeighbour
		else:
			firstChild = None
			firstChildLeftNeighbour = None
		
		while firstChild != None and firstChildLeftNeighbour != None and j <= k:
			modifierSumRight = 0.0
			modifierSumLeft = 0.0
			rightAncestor = firstChild
			leftAncestor = firstChildLeftNeighbour
			
			for i in range(j):
				rightAncestor = rightAncestor.parentNode
				leftAncestor = leftAncestor.parentNode
				modifierSumRight += rightAncestor.modifier
				modifierSumLeft += leftAncestor.modifier
			
			totalGap = (firstChildLeftNeighbour.prelim + modifierSumLeft + tree.getNodeSize(firstChildLeftNeighbour) + tree.subtreeSeperation) - (firstChild.prelim + modifierSumRight)  
			if totalGap > 0:
				subtreeAux = node
				numSubtrees = 0
				while subtreeAux != None and subtreeAux != leftAncestor:
					numSubtrees +=1
					subtreeAux = subtreeAux.getLeftSibling()
					
				if subtreeAux != None:
					subtreeMoveAux = node
					singleGap = totalGap / numSubtrees

					while subtreeMoveAux != None and subtreeMoveAux != leftAncestor:
						subtreeMoveAux.prelim += totalGap
						subtreeMoveAux.modifier += totalGap
						totalGap -= singleGap
						subtreeMoveAux = subtreeMoveAux.getLeftSibling()
							
			j += 1
			if firstChild.getChildrenCount() == 0:
				firstChild = tree.getLeftMost(node, 0, j)
			else:
				firstChild = firstChild.children[0]
			if firstChild != None:
				firstChildLeftNeighbour = firstChild.leftNeighbour
				
	def secondWalk(self, tree, node, level, posX, posY):
		if level <= tree.maxDepth:
			xTmp = tree.rootOffset.x() + node.prelim + posX
			yTmp = tree.rootOffset.y() + posY
			maxSizeTmp = 0
			nodeSizeTmp = 0
			flag = False
			
			if self.orientation == TreeOrientation.TOP or self.orientation == TreeOrientation.BOTTOM:
				maxSizeTmp = tree.maxLevelHeight[level]
				nodeSizeTmp = node.height
			elif self.orientation == TreeOrientation.LEFT or self.orientation == TreeOrientation.RIGHT: 
				maxSizeTmp = tree.maxLevelWidth[level]
				nodeSizeTmp = node.width
				flag = True
			
			node.position.setX(xTmp)
			node.position.setY(yTmp)
							
			if flag:
				swapTmp = node.position.x()
				node.position.setX(node.position.y())
				node.position.setY(swapTmp)
			
			if self.orientation == TreeOrientation.BOTTOM:
				node.position.setY(-node.position.y() - nodeSizeTmp)
			elif self.orientation == TreeOrientation.RIGHT:
				 node.position.setX(-node.position.x() - nodeSizeTmp)
			
			if node.getChildrenCount() != 0:
				self.secondWalk(tree, node.children[0], level+1, posX + node.modifier, posY + maxSizeTmp + tree.levelSeperation)
			
			rightSibling = node.getRightSibling()
			
			if rightSibling != None:
				self.secondWalk(tree, rightSibling, level, posX, posY)
	
	def positionTree(self):
		self.maxLevelWidth = []
		self.maxLevelHeight = []
		self.previousLevelNode = []
		self.firstWalk(self, self.root, 0)
		
		self.rootOffset.setX( self.topXAdjustment + self.root.position.x())
		self.rootOffset.setY( self.topYAdjustment + self.root.position.y())
		self.secondWalk(self, self.root, 0, 0, 0)		
	
	def updateTree(self):
		self.positionTree()
	
	def setLevelHeight(self, node, level):
		if len(self.maxLevelHeight) <= level:
			for i in range(level-len(self.maxLevelHeight)+1):
				self.maxLevelHeight += [None]
		if self.maxLevelHeight[level]< node.height:
			self.maxLevelHeight[level] = node.height
	
	def setLevelWidth(self, node, level):
		if len(self.maxLevelWidth) <= level:
			for i in range(level-len(self.maxLevelWidth)+1):
				self.maxLevelWidth += [None]
		if self.maxLevelWidth[level]< node.width:
			self.maxLevelWidth[level] = node.width
	
	def setNeighbours(self, node, level):
		if len(self.previousLevelNode) > level:
			node.leftNeighbour = self.previousLevelNode[level]
		else:
			for i in range(level - len(self.previousLevelNode)+1):
				self.previousLevelNode += [None]
			
		if node.leftNeighbour != None:
			node.leftNeighbour.rightNeighbour = node
		self.previousLevelNode[level] = node
	
	def getLeftMost(self, node, level, maxLevel):
		if level >= maxLevel:
			return node
		if node.getChildrenCount() == 0:
			return None
		
		for chldNode in node.children:
			leftMostDescendant = self.getLeftMost(chldNode, level+1, maxLevel)
			if leftMostDescendant != None:
				return leftMostDescendant
	
	def getNodeSize(self, node):
		if self.orientation == TreeOrientation.TOP or self.orientation == TreeOrientation.BOTTOM:
			return node.width
		elif self.orientation == TreeOrientation.LEFT or self.orientation == TreeOrientation.RIGHT: 
			return node.height
	
	def clear(self, node):
		node.clear()
		for childNode in node.children:
			self.clear(childNode)
	
	def __str__(self):
		pass
		
	def __str_recursive_(self):
		pass
	
class Node:
	def __init__(self, parentNode):
		self.prelim = 0
		self.position = QtCore.QPointF()		
		self.modifier = 0.0
		self.width = 50.0
		self.height = 40.0
		self.isCollapsed = False
		self.canCollapse = True
		
		self.parentNode = parentNode
		self.leftNeighbour = None
		self.rightNeighbour = None
		self.children = []
		self.variables = []
		
	def collapse(self):
		pass
	
	def expand(self):
		pass
	
	def getLeftSibling(self):
		if self.leftNeighbour != None and self.leftNeighbour.parentNode == self.parentNode:
			return self.leftNeighbour
		else:
			return None
	
	def getRightSibling(self):
		if self.rightNeighbour != None and self.rightNeighbour.parentNode == self.parentNode:
			return self.rightNeighbour
		else:
			return None
	
	def getChildrenCenter(self, tree):
		if len(self.children) > 0:
			return self.children[0].prelim + ((self.children[-1].prelim - self.children[0].prelim) + tree.getNodeSize(self.children[-1]))/2.0
		else:
			return 0.0
	
	def getChildrenCount(self):
		if self.isCollapsed:
			return 0
		else:
			return len(self.children)
	
	def clear(self):
		self.position.setX(0.0)
		self.position.setY(0.0)
		self.prelim = 0.0
		self.modifier = 0.0
	