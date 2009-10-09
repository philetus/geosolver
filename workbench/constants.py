""" The module provide some constants to make use of some different types """

class ViewportType:
	FRONT, SIDE, TOP, PERSPECTIVE, DECOMPOSITION, SOLUTION = range(6)

class MouseAction:
	ZOOM, ROTATE, TRANSLATE, FIT = range(4)

class DisplayViewport:
	ALL, SINGLE = range(2)
	
class ToolType:
	SELECT, MOVE, PLACE_POINT, PLACE_DISTANCE_CONSTRAINT, PLACE_ANGLE_CONSTRAINT, PLACE_DISTANCE, PLACE_FIXEDCONSTRAINT, CONNECT, DISCONNECT = range(9)
	
class ObjectType:
	POINT, DISTANCE_CONSTRAINT, ANGLE_CONSTRAINT, FIXED_POINT, DISTANCE_HELPER, CLUSTER = range(6)
	
class TreeOrientation:
	TOP, BOTTOM, LEFT, RIGHT = range(4)
	
class ConnectionType:
	LINES, BEZIER = range(2)
	