from includes import *
import numpy.numarray as Numeric
from geosolver.matfunc import Vec

class Quaternion:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        #self.quaternion = Numeric.array([x, y, z, w])
        self.quaternion = Vec([x, y, z, w])
        # self.matrix = Numeric.zeros([4,4])   $ ununsed! - Rick

    def __str__(self):
        return "Quaternion "+str(self.quaternion)

    def __repr__(self):
        return "Quaternion("+str(repr(self.quaternion))+")"

    def __mul__(self, quat2):
        return Quaternion(self.quaternion[3]*quat2.quaternion[0] + quat2.quaternion[3]*self.quaternion[0] + 
                          self.quaternion[1]*quat2.quaternion[2] - self.quaternion[2]*quat2.quaternion[1],
                          self.quaternion[3]*quat2.quaternion[1] + quat2.quaternion[3]*self.quaternion[1] +
                          self.quaternion[2]*quat2.quaternion[0] - self.quaternion[0]*quat2.quaternion[2],
                          self.quaternion[3]*quat2.quaternion[2] + quat2.quaternion[3]*self.quaternion[2] +
                          self.quaternion[0]*quat2.quaternion[1] - self.quaternion[1] * quat2.quaternion[0],
                          self.quaternion[3]*quat2.quaternion[3] - quat2.quaternion[0]*self.quaternion[0] -
                          self.quaternion[1]*quat2.quaternion[1] - self.quaternion[2]*quat2.quaternion[2])

    def getQuaternion(self):
        return self.quaternion

    def fromDirection(self, vFrom, vTo):
        vFrom = Vec(vFrom)
        vTo = Vec(vTo)
        epsilon = 1E-10
        fromLengthSq = vFrom.normSquared()
        toLengthSq = vTo.normSquared()
        
        if (fromLengthSq < epsilon) or (toLengthSq < epsilon):
            self.quaternion[0] = self.quaternion[1] = self.quaternion[2] = 0.0
            self.quaternion[3] = 1.0
        else:
            axis = vTo.cross(vFrom)
            axisLengthSq = axis.normSquared()

            if axisLengthSq < epsilon:
                if (math.fabs(vFrom[1]) >= math.fabs(vFrom[0])) and (math.fabs(vFrom[2]) >= math.fabs(vFrom[0])):
                    axis[0] = 0.0
                    axis[1] = -vFrom[2]
                    axis[2] = vFrom[0]
                elif (math.fabs(vFrom[0]) >= math.fabs(vFrom[1])) and (math.fabs(vFrom[2]) >= math.fabs(vFrom[1])):
                    axis[0] = -vFrom[2]
                    axis[1] = 0.0
                    axis[2] = vFrom[0]
                else:
                    axis[0] = -vFrom[1]
                    axis[1] = vFrom[0]
                    axis[2] = 0.0
            
            squareroot = math.sqrt(axisLengthSq / (fromLengthSq * toLengthSq))

            if squareroot > 1.0:
                squareroot = 1.0
            elif squareroot < -1.0:
                squareroot = -1.0
            
            angle = math.asin(squareroot)

            if vFrom.dot(vTo) < 0.0:
                angle = math.pi - angle

            self.fromAxisAngle(axis, angle)
    
    def angleBetween(self, vFrom, vTo):
        d = vFrom.dot(vTo)
        axis = vFrom.cross(vTo)
        qw = math.sqrt(vFrom.normSquared()*vTo.normSquared()) + d

        if qw < 0.0001:
            self.quaternion[0] = -vFrom[2]
            self.quaternion[1] = vFrom[1]
            self.quaternion[2] = vFrom[0]
            self.quaternion[3] = 1.0
            self.normalize()
        else:
            self.quaternion[0] = axis[0]
            self.quaternion[1] = axis[1]
            self.quaternion[2] = axis[2]
            self.quaternion[3] = qw
            self.normalize()
                
    def fromAxisAngle(self, axis, angle):
        axisLength = axis.norm()
        if axisLength < 1E-8:
            self.quaternion[0] = 0.0
            self.quaternion[1] = 0.0
            self.quaternion[2] = 0.0
            self.quaternion[3] = 1.0
        else:
            sinHalfAngle = math.sin(angle/2.0)
            self.quaternion[0] = sinHalfAngle * axis[0]/axisLength
            self.quaternion[1] = sinHalfAngle * axis[1]/axisLength
            self.quaternion[2] = sinHalfAngle * axis[2]/axisLength
            self.quaternion[3] = math.cos(angle/2.0)

    def fromEulerToQuaternion(self, heading, attitude, bank):
        c1 = math.cos(heading/2.0)
        s1 = math.sin(heading/2.0)
        c2 = math.cos(attitude/2.0)
        s2 = math.sin(attitude/2.0)
        c3 = math.cos(bank/2.0)
        s3 = math.sin(bank/2.0)
        c1c2 = c1*c2
        s1s2 = s1*s2
        tempQuat = Quaternion()
        tempQuat.quaternion[3] = c1c2*c3 - s1s2*s3
        tempQuat.quaternion[0] = c1c2*s3 + s1s2*c3
        tempQuat.quaternion[1] = s1*c2*c3 + c1*s2*s3
        tempQuat.quaternion[2] = c1*s2*c3 - s1*c2*s3
        return tempQuat
        
    def getAxisAngle(self, quat, axis):
        realQuat = quat.getQuaternion()
        angle = 2.0*math.acos(realQuat[3])
        axis[0] = realQuat[0]
        axis[1] = realQuat[1]
        axis[2] = realQuat[2]
        
        sinus = axis.norm()
        if sinus > 1E-8:
            axis[0] /= sinus
            axis[1] /= sinus
            axis[2] /= sinus

        if angle > math.pi:
            angle = 2.0*math.pi - angle;
            axis = -axis;
        
        return math.degrees(angle)
    
    def getMatrix(self, matrix):
        quat00 = 2.0 * self.quaternion[0] * self.quaternion[0]
        quat11 = 2.0 * self.quaternion[1] * self.quaternion[1]
        quat22 = 2.0 * self.quaternion[2] * self.quaternion[2]
        
        quat01 = 2.0 * self.quaternion[0] * self.quaternion[1]
        quat02 = 2.0 * self.quaternion[0] * self.quaternion[2]
        quat03 = 2.0 * self.quaternion[0] * self.quaternion[3]

        quat12 = 2.0 * self.quaternion[1] * self.quaternion[2]
        quat13 = 2.0 * self.quaternion[1] * self.quaternion[3]

        quat23 = 2.0 * self.quaternion[2] * self.quaternion[3]

        matrix[0][0] = 1.0 - quat11 - quat22
        matrix[1][0] =      quat01 - quat23
        matrix[2][0] =         quat02 + quat13
        
        matrix[0][1] =         quat01 + quat23
        matrix[1][1] = 1.0 - quat22 - quat00
        matrix[2][1] =         quat12 - quat03
        
        matrix[0][2] =         quat02 - quat13
        matrix[1][2] =         quat12 + quat03
        matrix[2][2] = 1.0 - quat11 - quat00

        matrix[0][3] = 0.0
        matrix[1][3] = 0.0
        matrix[2][3] = 0.0
        matrix[3][0] = 0.0
        matrix[3][1] = 0.0
        matrix[3][2] = 0.0
        matrix[3][3] = 1.0

    # Not used - Rick
    #def getMatrixSingle(self, matrix):
    #    mat = Numeric.zeros([4,4])
    #    self.getMatrix(mat)
    #    count = 0
    #    for i in range(4):
    #        for j in range(4):
    #            matrix[count] = mat[i][j]
    #            count += 1
    #    #print "between:"
    #    #print matrix
    
    def getRotationMatrix(self, matrix):
        mat = Numeric.identity(4)
        self.getMatrix(mat)
        
        for i in range(4):
            for j in range(4):
                matrix[i][j] = mat[j][i]

    def axis(self):
        result = Vec([self.quaternion[0], self.quaternion[1], self.quaternion[2]])
        sinus = result.norm()
        if sinus > 1E-8:
            result /= sinus
        if math.acos(self.quaternion[3]) <= (math.pi/2.0):
            return result
        else:
            return -result
        
    def angle(self):
        angle = 2.0 * math.acos(self.quaternion[3])
        if angle <= math.pi:
            return angle
        else:
            return 2.0*math.pi - angle

    def rotate(self, vec):
        quat00 = 2.0 * self.quaternion[0] * self.quaternion[0]
        quat11 = 2.0 * self.quaternion[1] * self.quaternion[1]
        quat22 = 2.0 * self.quaternion[2] * self.quaternion[2]
        
        quat01 = 2.0 * self.quaternion[0] * self.quaternion[1]
        quat02 = 2.0 * self.quaternion[0] * self.quaternion[2]
        quat03 = 2.0 * self.quaternion[0] * self.quaternion[3]

        quat12 = 2.0 * self.quaternion[1] * self.quaternion[2]
        quat13 = 2.0 * self.quaternion[1] * self.quaternion[3]

        quat23 = 2.0 * self.quaternion[2] * self.quaternion[3]

        rotation = Vec([0.0, 0.0, 0.0])
        rotation[0] = (1.0 - quat11 - quat22)*vec[0] + (      quat01 - quat23)*vec[1] + (quat02 + quat13)*vec[2]
        rotation[1] = (         quat01 + quat23)*vec[0] + (1.0 - quat22 - quat00)*vec[1] + (quat12 - quat03)*vec[2]
        rotation[2] = (         quat02 - quat13)*vec[0] + (      quat12 + quat03)*vec[1] + (1.0 - quat11 - quat00)*vec[2]

        #print "rot: ", rotation
        return rotation

    def inverseRotate(self, vec):
        return self.inverse().rotate(vec)
        
    def normalize(self):
        magnitude = Numeric.sqrt(self.quaternion[0]*self.quaternion[0] + self.quaternion[1]*self.quaternion[1] + self.quaternion[2]*self.quaternion[2] + self.quaternion[3]*self.quaternion[3])
        for i in range(4):
              self.quaternion[i] /= magnitude
        return magnitude

    def normalized(self):
        quat = Quaternion()
        magnitude = sqrt(self.quaternion[0]*self.quaternion[0] + self.quaternion[1]*self.quaternion[1] + self.quaternion[2]*self.quaternion[2] + self.quaternion[3]*self.quaternion[3])
        for i in range(4):
              self.quat = self.quaternion[i] / magnitude
        return quat

    def invert(self):
        self.quaternion[0] = -self.quaternion[0] 
        self.quaternion[1] = -self.quaternion[1]
        self.quaternion[2] = -self.quaternion[2]

    def inverse(self):
        return Quaternion(-self.quaternion[0], -self.quaternion[1], -self.quaternion[2], self.quaternion[3])

    def dot(self, qA, qB):
        quatA = qA.getQuaternion()
        quatB = qB.getQuaternion()
        return quatA[0] * quatB[0] + quatA[1] * quatB[1] + quatA[2] * quatB[2] + quatA[3] * quatB[3]

    def slerp(self, qStart, qEnd, alpha, allowFlip=True):
        cosAngle = self.dot(qStart, qEnd)
        c1 = c2 = 0.0

        if (1.0 - math.fabs(cosAngle)) < 0.01:
            c1 = 1.0 - alpha
            c2 = alpha
        else:
            angle = math.acos(math.fabs(cosAngle))
            sinAngle = math.sin(angle)
            c1 = math.sin(angle * (1.0 - alpha)) / sinAngle
            c2 = math.sin(angle * alpha) / sinAngle

        if allowFlip and (cosAngle < 0.0):
            c1 = -c1
        
        qStartQuat = qStart.getQuaternion()
        qEndQuat = qEnd.getQuaternion()
        return Quaternion(c1 * qStartQuat[0] + c2*qEndQuat[0], c1 * qStartQuat[1] + c2*qEndQuat[1], 
                          c1 * qStartQuat[2] + c2*qEndQuat[2], c1 * qStartQuat[3] + c2*qEndQuat[3])

    def setFromRotatedBasis(self, vecX, vecY, vecZ):
        #print "setFromRotatedBases: ",vecX,vecY,vecZ
        m = Numeric.zeros([3,3])
        normX = vecX.norm()
        normY = vecY.norm()
        normZ = vecZ.norm()
        #print "norms: ",normX, normY, normZ
        for i in range(3):
            m[i][0] = vecX[i] / normX
            m[i][1] = vecY[i] / normY
            m[i][2] = vecZ[i] / normZ
        self.setFromRotationMatrix(m)

    def setFromRotationMatrix(self, matrix):
        #print "setFromRotationMatix: ",matrix
        onePlusTrace = 1.0 + matrix[0][0] + matrix[1][1] + matrix[2][2]
        
        if onePlusTrace > 1E-5:
            s = 0.5/math.sqrt(onePlusTrace)
            self.quaternion[0] = (matrix[2][1] - matrix[1][2]) * s
            self.quaternion[1] = (matrix[0][2] - matrix[2][0]) * s
            self.quaternion[2] = (matrix[1][0] - matrix[0][1]) * s
            self.quaternion[3] = 0.25 / s

        elif (matrix[0][0] > matrix[1][1]) and (matrix[0][0] > matrix[2][2]):
            s = math.sqrt(1.0 + matrix[0][0] - matrix[1][1] - matrix[2][2]) * 2.0
            self.quaternion[0] = 0.25 * s
            self.quaternion[1] = (matrix[0][1] + matrix[1][0]) / s
            self.quaternion[2] = (matrix[0][2] + matrix[2][0]) / s
            self.quaternion[3] = (matrix[1][2] - matrix[2][1]) / s

        elif matrix[1][1] > matrix[2][2]:
            s = math.sqrt(1.0 + matrix[1][1] - matrix[0][0] - matrix[2][2]) * 2.0
            self.quaternion[0] = (matrix[0][1] + matrix[1][0]) / s 
            self.quaternion[1] = 0.25 * s
            self.quaternion[2] = (matrix[1][2] + matrix[2][1]) / s
            self.quaternion[3] = (matrix[0][2] - matrix[2][0]) /s

        else:
            s = math.sqrt(1.0 + matrix[2][2] - matrix[0][0] - matrix[1][1]) * 2.0            
            self.quaternion[0] = (matrix[0][2] + matrix[2][0]) / s 
            self.quaternion[1] = (matrix[1][2] + matrix[2][1]) / s
            self.quaternion[2] = 0.25 * s
            self.quaternion[3] = (matrix[0][1] - matrix[1][0]) /s

        self.normalize()
        #print "quaternion: ", self.quaternion

if __name__ == "__main__":
    print "hallo"
    a = Quaternion(3.0, 3.0, 2.0, 1.0)
    #b = Quaternion()
    #c = a.slerp(a, b, 0.3)
    a.normalize()
    print a.getQuaternion()
    
        
