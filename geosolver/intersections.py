import vector
import math
import random
from matfunc import Mat,Vec,eye
from tolerance import *
from diagnostic import *

# ------ misc fucntions ----------

def sign(x):
    """Returns 1 if x>0, return -1 if x<0 and 0 if x=0"""
    if tol_gt(x,0.0):
        return 1.0
    elif tol_lt(x,0.0):
        return -1.0
    else:
        return 0.0

def sign2(x):
    """Returns 1 if x>0, else -1 (even if x=0)"""
    if tol_gt(x,0.0):
        return 1.0
    else:
        return -1.0


# -------- 3D intersections ---------------


def sss_int(p1, r1, p2, r2, p3, r3):
    """Intersect three spheres, centered in p1, p2, p3 with radius r1,r2,r3 respectively. 
       Returns a list of zero, one or two solution points.
    """
    solutions = []
    # intersect circles in plane
    cp1 = vector.vector([0.0,0.0]) 
    cp2 = vector.vector([vector.norm(p2-p1), 0.0])
    cpxs = cc_int(cp1, r1, cp2, r2)
    if len(cpxs) == 0:
        return []
    # determine normal of plane though p1, p2, p3
    n = vector.cross(p2-p1, p3-p1)
    if not tol_eq(vector.norm(n),0.0):  
        n = n / vector.norm(n)
    else:
        # traingle p1, p2, p3 is degenerate
        # check for 2d solutions
        if len(cpxs) == 0:
            return []
        # project cpxs back to 3d and check radius r3 
        cp4 = cpxs[0]
        u = normalised(p2-p1)
        v,w = perp_3d(u)
        p4 = p1 + cp4[0] * u + cp4[1] * v
        if tol_eq(vector.norm(p4-p3), r3):
            return [p4]
        else:
            return []
    # px, rx, nx is circle 
    px = p1 + (p2-p1) * cpxs[0][0] / vector.norm(p2-p1)
    rx = abs(cpxs[0][1])
    nx = p2-p1
    nx = nx / vector.norm(nx)
    # py is projection of p3 on px,nx
    dy3 = vector.dot(p3-px, nx)
    py = p3 - (nx * dy3)
    if tol_gt(dy3, r3):
        return []
    # ry is radius of circle in py
    if tol_eq(r3,0.0):
        ry = 0.0 
    else:   
        ry = math.sin(math.acos(min(1.0,abs(dy3/r3))))*r3
    # determine intersection of circle px, rx and circle py, ry, projected relative to line py-px 
    cpx = vector.vector([0.0,0.0]) 
    cpy = vector.vector([vector.norm(py-px), 0.0])
    cp4s = cc_int(cpx, rx, cpy, ry)
    for cp4 in cp4s:
        p4 = px + (py-px) * cp4[0] / vector.norm(py-px) + n * cp4[1] 
        solutions.append(p4)  
    return solutions

# ------- 2D intersections ----------------

def cc_int(p1, r1, p2, r2):
    """
    Intersect circle (p1,r1) circle (p2,r2)
    where p1 and p2 are 2-vectors and r1 and r2 are scalars
    Returns a list of zero, one or two solution points.
    """
    d = vector.norm(p2-p1)
    if not tol_gt(d, 0):
        return []
    u = ((r1*r1 - r2*r2)/d + d)/2
    if tol_lt(r1*r1, u*u):
        return []
    elif r1*r1 < u*u:
        v = 0.0
    else:
        v = math.sqrt(r1*r1 - u*u)
    s = (p2-p1) * u / d
    if tol_eq(vector.norm(s),0):
        p3a = p1+vector.vector([p2[1]-p1[1],p1[0]-p2[0]])*r1/d
        if tol_eq(r1/d,0):
            return [p3a]
        else:
            p3b = p1+vector.vector([p1[1]-p2[1],p2[0]-p1[0]])*r1/d
            return [p3a,p3b]
    else:
        p3a = p1 + s + vector.vector([s[1], -s[0]]) * v / vector.norm(s) 
        if tol_eq(v / vector.norm(s),0):
            return [p3a]
        else:
            p3b = p1 + s + vector.vector([-s[1], s[0]]) * v / vector.norm(s)
            return [p3a,p3b]


def cl_int(p1,r,p2,v):
    """
    Intersect a circle (p1,r) with line (p2,v)
    where p1, p2 and v are 2-vectors, r is a scalar
    Returns a list of zero, one or two solution points
    """
    p = p2 - p1
    d2 = v[0]*v[0] + v[1]*v[1]
    D = p[0]*v[1] - v[0]*p[1]
    E = r*r*d2 - D*D
    if tol_gt(d2, 0) and tol_gt(E, 0):
        sE = math.sqrt(E) 
        x1 = p1[0] + (D * v[1] + sign2(v[1])*v[0]*sE) / d2
        x2 = p1[0] + (D * v[1] - sign2(v[1])*v[0]*sE) / d2
        y1 = p1[1] + (-D * v[0] + abs(v[1])*sE) / d2
        y2 = p1[1] + (-D * v[0] - abs(v[1])*sE) / d2
        return [vector.vector([x1,y1]), vector.vector([x2,y2])]
    elif tol_eq(E, 0):
        x1 = p1[0] + D * v[1] / d2
        y1 = p1[1] + -D * v[0] / d2
        return [vector.vector([x1,y1])]
    else:
        return []

def cr_int(p1,r,p2,v):
    """
    Intersect a circle (p1,r) with ray (p2,v) (a half-line)
    where p1, p2 and v are 2-vectors, r is a scalar
    Returns a list of zero, one or two solutions.
    """
    sols = []
    all = cl_int(p1,r,p2,v)
    for s in all: 
        if tol_gte(vector.dot(s-p2,v), 0):          
            sols.append(s)
    return sols

def ll_int(p1, v1, p2, v2):
    """Intersect line though p1 direction v1 with line through p2 direction v2.
       Returns a list of zero or one solutions
    """
    diag_print("ll_int "+str(p1)+str(v1)+str(p2)+str(v2),"intersections")
    if tol_eq((v1[0]*v2[1])-(v1[1]*v2[0]),0):
        return []
    elif not tol_eq(v2[1],0.0):
        d = p2-p1
        r2 = -v2[0]/v2[1]
        f = v1[0] + v1[1]*r2
        t1 = (d[0] + d[1]*r2) / f
    else:
        d = p2-p1
        t1 = d[1]/v1[1]
    return [p1 + v1*t1]
    
def lr_int(p1, v1, p2, v2):
    """Intersect line though p1 direction v1 with ray through p2 direction v2.
       Returns a list of zero or one solutions
    """
    diag_print("lr_int "+str(p1)+str(v1)+str(p2)+str(v2),"intersections")
    s = ll_int(p1,v1,p2,v2)
    if len(s) > 0 and tol_gte(vector.dot(s[0]-p2,v2), 0):
        return s
    else:
        return []
 
def rr_int(p1, v1, p2, v2):
    """Intersect ray though p1 direction v1 with ray through p2 direction v2.
       Returns a list of zero or one solutions
    """
    diag_print("rr_int "+str(p1)+str(v1)+str(p2)+str(v2),"intersections")
    s = ll_int(p1,v1,p2,v2)
    if len(s) > 0 and tol_gte(vector.dot(s[0]-p2,v2), 0) and tol_gte(vector.dot(s[0]-p1,v1),0):
        return s
    else:
        return []

# ----- Geometric properties ------- 

def angle_3p(p1, p2, p3):
    """Returns the angle, in radians, rotating vector p2p1 to vector p2p3.
       arg keywords:
          p1 - a vector
          p2 - a vector
          p3 - a vector
       returns: a number
       In 2D, the angle is a signed angle, range [-pi,pi], corresponding
       to a clockwise rotation. If p1-p2-p3 is clockwise, then angle > 0.
       In 3D, the angle is unsigned, range [0,pi]
    """
    d21 = vector.norm(p2-p1)
    d23 = vector.norm(p3-p2)
    if tol_eq(d21,0) or tol_eq(d23,0):
        # degenerate, indeterminate angle
        return None
    v21 = (p1-p2) / d21
    v23 = (p3-p2) / d23
    t = vector.dot(v21,v23) # / (d21 * d23)
    if t > 1.0:             # check for floating point error
        t = 1.0
    elif t < -1.0:
        t = -1.0
    angle = math.acos(t)
    if len(p1) == 2:        # 2D case
        if is_counterclockwise(p1,p2,p3):
            angle = -angle
    return angle

def distance_2p(p1, p2):
    """Returns the euclidean distance between two points
       arg keywords:
          p1 - a vector
          p2 - a vector
       returns: a number
    """
    return vector.norm(p2 - p1)

def distance_point_line(p,l1,l2):
    """distance from point p to line l1-l2"""
    # v,w is p, l2 relative to l1
    v = p-l1
    w = l2-l1
    # x = projection v on w
    lw = vector.norm(w)
    if tol_eq(lw,0):
        x = 0*w
    else:
        x = w * vector.dot(v,w) / lw
    # result is distance x,v
    return vector.norm(x-v)

# ------ 2D

def is_clockwise(p1,p2,p3):
    """ returns True iff triangle p1,p2,p3 is clockwise oriented"""
    assert len(p1)==2
    assert len(p1)==len(p2)
    assert len(p2)==len(p3)   
    u = p2 - p1
    v = p3 - p2
    perp_u = vector.vector([-u[1], u[0]])
    return tol_lt(vector.dot(perp_u,v),0)

def is_counterclockwise(p1,p2,p3):
    """ returns True iff triangle p1,p2,p3 is counterclockwise oriented"""
    assert len(p1)==2
    assert len(p1)==len(p2)
    assert len(p2)==len(p3)   
    u = p2 - p1
    v = p3 - p2;
    perp_u = vector.vector([-u[1], u[0]])
    return tol_gt(vector.dot(perp_u,v), 0)

def is_colinear(p1,p2,p3):
    """ returns True iff triangle p1,p2,p3 is colinear (neither clockwise of counterclockwise oriented)"""
    assert len(p1)==2
    assert len(p1)==len(p2)
    assert len(p2)==len(p3)   
 
    u = p2 - p1
    v = p3 - p2;
    perp_u = vector.vector([-u[1], u[0]])
    return tol_eq(vector.dot(perp_u,v), 0)

# ------ 2D or 3D ----

def is_acute(p1,p2,p3):
    """returns True iff angle p1,p2,p3 is acute, i.e. less than pi/2"""
    angle = angle_3p(p1, p2, p3)
    if angle == None:
        return None
    else:
        return tol_gt(abs(angle), math.pi / 2)


def is_obtuse(p1,p2,p3):
    """returns True iff angle p1,p2,p3 is obtuse, i.e. greater than pi/2"""
    angle = angle_3p(p1, p2, p3)
    if angle == None:
        return None
    else:
        return tol_gt(abs(angle), math.pi / 2)

# -------- 3D ------------

def is_left_handed(p1,p2,p3,p4):
    """return True if tetrahedron p1 p2 p3 p4 is left handed"""
    u = p2-p1
    v = p3-p1
    uv = vector.cross(u,v)
    w = p4-p1
    #return vector.dot(uv,w) < 0 
    return tol_lt(vector.dot(uv,w), 0) 

def is_right_handed(p1,p2,p3,p4):
    """return True if tetrahedron p1 p2 p3 p4 is right handed"""
    u = p2-p1
    v = p3-p1
    uv = vector.cross(u,v)
    w = p4-p1
    #return vector.dot(uv,w) > 0 
    return tol_gt(vector.dot(uv,w), 0) 

def is_coplanar(p1,p2,p3,p4):
    """return True if tetrahedron p1 p2 p3 p4 is co-planar (not left- or right-handed)"""
    u = p2-p1
    v = p3-p1
    uv = vector.cross(u,v)
    w = p4-p1
    #return vector.dot(uv,w) == 0 
    return tol_eq(vector.dot(uv,w), 0) 


# --------- coordinate tranformations -------

def make_hcs_3d (a, b, c, righthanded=True):
    """build a 3D homogeneous coordiate system from three points. The origin is point a. The x-axis is
    b-a, the y axis is c-a, or as close as possible after orthogonormalisation."""
    # create orthonormal basis 
    u = normalised(b-a)
    v = normalised(c-a)
    nu = vector.norm(u)
    nv = vector.norm(v)
    if tol_eq(nu,0.0) and tol_eq(nv,0.0):
        # all points equal, no rotation
        u = vector.vector([1.0,0.0,0.0])
        v = vector.vector([0.0,1.0,0.0])
    elif tol_eq(nu, 0.0):
        # determine u perpendicular from v
        u,dummy = perp_3d(v)[0]
    elif tol_eq(nv, 0.0):
        # determine v perpendicular from u
        dummy,v = perp_3d(u)[0]
    # ensure that u and v are different
    if tol_eq(vector.norm(u-v),0.0):
        dummy,v = perp_3d(u)[0]
    # make the basis vectors orthogonal
    w = vector.cross(u,v)
    v = vector.cross(w,u)
    # flip basis if lefthanded desired
    if righthanded==False:
        w = -w
    # create matix with basis vectors + translation as columns
    hcs = Mat([ 
        [u[0],v[0], w[0], a[0]], 
        [u[1],v[1], w[1], a[1]],
        [u[2],v[2], w[2], a[2]], 
        [0.0, 0.0, 0.0, 1.0]    ])
    return hcs 

def make_hcs_3d_scaled (a, b, c):
    """build a 3D homogeneus coordiate system from three points, and derive scale from distance between points"""
     # create orthonormal basis 
    u = normalised(b-a)
    v = normalised(c-a)
    nu = vector.norm(u)
    nv = vector.norm(v)
    if tol_eq(nu,0) and tol_eq(nv,0):
        # all points equal, no rotation
        u = vector.vector([1.0,0.0,0.0])
        v = vector.vector([0.0,1.0,0.0])
    elif tol_eq(nu, 0):
        # determine u perpendicular from v
        u,dummy = perp_3d(v)[0]
    elif tol_eq(nv, 0):
        # determine v perpendicular from u
        dummy,v = perp_3d(u)[0]
    # make the basis vectors orthogonal
    w = vector.cross(u,v)
    v = vector.cross(w,u)
    # scale again
    if not tol_eq(vector.norm(b-a),0.0):
        u = u / vector.norm(b-a)
    if not tol_eq(vector.norm(c-a),0.0):
        v = v / vector.norm(c-a)
    # note: w is not scaled
    # create matix with basis vectors + translation as columns
    hcs = Mat([ 
        [u[0],v[0], w[0], a[0]], 
        [u[1],v[1], w[1], a[1]],
        [u[2],v[2], w[2], a[2]], 
        [0.0, 0.0, 0.0, 1.0]    ])
    return hcs 

def make_hcs_2d (a, b):
    """build a 2D homogeneus coordiate system from two points"""
    u = b-a
    if tol_eq(vector.norm(u), 0.0):
        u = vector.vector([0.0,0.0])
    else:
        u = u / vector.norm(u)
    v = vector.vector([-u[1], u[0]])
    hcs = Mat([ [u[0],v[0],a[0]] , [u[1],v[1],a[1]] , [0.0, 0.0, 1.0] ] )
    return hcs 

def make_hcs_2d_scaled (a, b):
    """build a 2D homogeneus coordiate system from two points, but scale with distance between input point"""
    u = b-a
    if tol_eq(vector.norm(u), 0.0):     
        u = vector.vector([1.0,0.0])
    #else:
    #    u = u / vector.norm(u)
    v = vector.vector([-u[1], u[0]])
    hcs = Mat([ [u[0],v[0],a[0]] , [u[1],v[1],a[1]] , [0.0, 0.0, 1.0] ] )
    return hcs 

def cs_transform_matrix(from_cs, to_cs):
    """returns a transform matrix from from_cs to to_cs"""
    try:
        transform = to_cs.mmul(from_cs.inverse())
    except Exception, e:
        print "from_cs=",from_cs
        raise Exception, "from_cs is not a valid coodinate system."
    return transform

# ------- rigid transformations ----------

#--- 2D

def id_transform_2D():
    return eye(3)

def translate_2D(dx,dy):
    mat = Mat([ 
        [1.0, 0.0, dx] , 
        [0.0, 1.0, dy] , 
        [0.0, 0.0, 1.0] ] )
    return mat

def rotate_2D(angle):
    """rotation matrix for rotation in 2d with homogeneous coordinates"""
    cosa = math.cos(angle)
    sina = math.sin(angle)
    mat = Mat([ 
        [cosa,-sina,0.0], 
        [sina,cosa,0.0], 
        [0.0, 0.0, 1.0] ])
    return mat

# --- 3D

def id_transform_3D():
    return eye(4)

def rotate_3D_z(angle):
    """rotation matrix for rotation in 3d over z-axis with homogeneous coordinates"""
    cosa = math.cos(angle)
    sina = math.sin(angle)
    mat = Mat([ 
        [cosa,-sina,0.0, 0.0], 
        [sina,cosa, 0.0, 0.0],   
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0] ] )
    return mat

def rotate_3D_y(angle):
    """rotation matrix for rotation in 3d over y-axis with homogeneous coordinates"""
    cosa = math.cos(angle)
    sina = math.sin(angle)
    mat = Mat([ 
        [cosa,0.0,sina, 0.0], 
        [0.0, 1.0, 0.0, 0.0],
        [-sina,0.0,cosa, 0.0], 
        [0.0, 0.0, 0.0, 1.0] ] )
    return mat

def rotate_3D_x(angle):
    """rotation matrix for rotation in 3d over x-axis with homogeneous coordinates"""
    cosa = math.cos(angle)
    sina = math.sin(angle)
    mat = Mat([ 
        [1.0, 0.0,0.0, 0.0], 
        [0.0, cosa, -sina, 0.0],
        [0.0, sina, cosa, 0.0], 
        [0.0, 0.0, 0.0, 1.0] ] )
    return mat

def translate_3D(dx,dy,dz):
    mat = Mat([ 
    [1.0, 0.0, 0.0, dx] , 
    [0.0, 1.0, 0.0, dy] , 
    [0.0, 0.0, 1.0, dz] , 
    [0.0, 0.0, 0.0, 1.0] ] )
    return mat

def scale_3D(sx, sy, sz):
    mat = Mat([ 
    [sx, 0.0, 0.0, 0.0] , 
    [0.0, sy, 0.0, 0.0] , 
    [0.0, 0.0, sz, 0.0] , 
    [0.0, 0.0, 0.0, 1.0] ] )
    return mat

def uniform_scale_3D(scale):
    mat = Mat([ 
    [scale, 0.0, 0.0, 0.0] , 
    [0.0, scale, 0.0, 0.0] , 
    [0.0, 0.0, scale, 0.0] , 
    [0.0, 0.0, 0.0, 1.0] ] )
    return mat

def pivot_scale_3D(pivot,scale):
    x = pivot[0]
    y = pivot[1]
    z = pivot[2]
    return translate_3D(x, y, z).mmul(
            uniform_scale_3D(scale).mmul(
                translate_3D(-x, -y, -z)))


# ---- applyign transformations

def transform_point(point, transform):
    """transform a point"""
    hpoint = Vec(point)
    hpoint.append(1.0)
    hres = transform.mmul(hpoint)
    res = vector.vector(hres[0:-1]) / hres[-1]
    return res

# -------- perpendicular vectors ---------

def perp_2d(v):
    """returns the orthonormal vector."""
    return normalised(vector.vector([-v[1], v[0]]))


perp_matrix = rotate_3D_x(math.pi/2).mmul(rotate_3D_z(math.pi/2).mmul(rotate_3D_y(math.pi)))

def perp_3d(u):
    """Returns 2 orthonormal vectors."""
    t = transform_point(u, perp_matrix)
    v = normalised(vector.cross(u,t))
    w = normalised(vector.cross(u,v))
    return (v,w)

def normalised(v):
    n = vector.norm(v)
    if tol_eq(n, 0.0):
        return v
    else:
        return v / n

# -------------------------test code -----------------

def test_ll_int():
    """test random line-line intersection. returns True iff succesful"""
    # generate tree points A,B,C an two lines AC, BC. 
    # then calculate the intersection of the two lines
    # and check that it equals C
    p_a = vector.randvec(2, 0.0, 10.0,1.0)
    p_b = vector.randvec(2, 0.0, 10.0,1.0)
    p_c = vector.randvec(2, 0.0, 10.0,1.0)
    # print p_a, p_b, p_c
    if tol_eq(vector.norm(p_c - p_a),0) or tol_eq(vector.norm(p_c - p_b),0): 
        return True # ignore this case
    v_ac = (p_c - p_a) / vector.norm(p_c - p_a)
    v_bc = (p_c - p_b) / vector.norm(p_c - p_b)
    s = ll_int(p_a, v_ac, p_b, v_bc)
    if tol_eq(math.fabs(vector.dot(v_ac, v_bc)),1.0): 
        return len(s) == 0
    else:
        if len(s) > 0:
            p_s = s[0]
            return tol_eq(p_s[0],p_c[0]) and tol_eq(p_s[1],p_c[1])
        else:
            return False

def test_rr_int():
    """test random ray-ray intersection. returns True iff succesful"""
    # generate tree points A,B,C an two rays AC, BC. 
    # then calculate the intersection of the two rays
    # and check that it equals C
    p_a = vector.randvec(2, 0.0, 10.0,1.0)
    p_b = vector.randvec(2, 0.0, 10.0,1.0)
    p_c = vector.randvec(2, 0.0, 10.0,1.0)
    # print p_a, p_b, p_c
    if tol_eq(vector.norm(p_c - p_a),0) or tol_eq(vector.norm(p_c - p_b),0): 
        return True # ignore this case
    v_ac = (p_c - p_a) / vector.norm(p_c - p_a)
    v_bc = (p_c - p_b) / vector.norm(p_c - p_b)
    s = rr_int(p_a, v_ac, p_b, v_bc)
    if tol_eq(math.fabs(vector.dot(v_ac, v_bc)),1.0): 
        return len(s) == 0
    else:
        if len(s) > 0:
            p_s = s[0]
            return tol_eq(p_s[0],p_c[0]) and tol_eq(p_s[1],p_c[1])
        else:
            return False

def test_sss_int():
    p1 = vector.randvec(3, 0.0, 10.0,1.0)
    p2 = vector.randvec(3, 0.0, 10.0,1.0)
    p3 = vector.randvec(3, 0.0, 10.0,1.0)
    p4 = vector.randvec(3, 0.0, 10.0,1.0)
    #p1 = vector.vector([0.0,0.0,0.0])
    #p2 = vector.vector([1.0,0.0,0.0])
    #p3 = vector.vector([0.0,1.0,0.0])
    #p4 = vector.vector([1.0,1.0,1.0])
    d14 = vector.norm(p4-p1)
    d24 = vector.norm(p4-p2)
    d34 = vector.norm(p4-p3)
    sols = sss_int(p1,d14,p2,d24,p3,d34)
    sat = True
    for sol in sols:
        # print sol
        d1s = vector.norm(sol-p1)
        d2s = vector.norm(sol-p2)
        d3s = vector.norm(sol-p3)
        sat = sat and tol_eq(d1s,d14)
        sat = sat and tol_eq(d2s,d24)
        sat = sat and tol_eq(d3s,d34)
        # print sat
    return sat

def test_cc_int():
    """Generates two random circles, computes the intersection,
       and verifies that the number of intersections and the 
       positions of the intersections are correct. 
       Returns True or False"""
    # gen two random circles p1,r2 and p2, r2
    p1 = vector.randvec(2, 0.0, 10.0,1.0)
    r1 = random.uniform(0, 10.0)
    p2 = vector.randvec(2, 0.0, 10.0,1.0)
    r2 = random.uniform(0, 10.0)
    # 33% change that r2=abs(r1-|p1-p2|)
    if random.random() < 0.33:
        r2 = abs(r1-vector.norm(p1-p2))
    # do interesection 
    diag_print("problem:"+str(p1)+","+str(r1)+","+str(p2)+","+str(r2),"test_cc_int")
    sols = cc_int(p1, r1, p2, r2)
    diag_print("solutions:"+str(map(str, sols)),"test_cc_int")
    # test number of intersections
    if len(sols) == 0:
        if not tol_gt(vector.norm(p2-p1),r1 + r2) and not tol_lt(vector.norm(p2-p1),abs(r1 - r2)) and not tol_eq(vector.norm(p1-p2),0):
            diag_print("number of solutions 0 is wrong","test_cc_int")
            return False
    elif len(sols) == 1: 
        if not tol_eq(vector.norm(p2-p1),r1 + r2) and not tol_eq(vector.norm(p2-p1),abs(r1-r2)):
            diag_print("number of solutions 1 is wrong","test_cc_int")
            return False
    elif len(sols) == 2:
        if not tol_lt(vector.norm(p2-p1),r1 + r2) and not tol_gt(vector.norm(p2-p1),abs(r1 - r2)):
            diag_prin("number of solutions 2 is wrong")
            return False
    else:
        diag_print("number of solutions > 2 is wrong","test_cc_int")
        return False

    # test intersection coords
    for p3 in sols:
        if not tol_eq(vector.norm(p3-p1), r1):
            diag_print("solution not on circle 1","test_cc_int")
            return False
        if not tol_eq(vector.norm(p3-p2), r2):
            diag_print("solution not on circle 2","test_cc_int")
            return False

    diag_print("OK","test_cc_int")
    return True

def test_cl_int():
    """Generates random circle and line, computes the intersection,
       and verifies that the number of intersections and the 
       positions of the intersections are correct. 
       Returns True or False"""
    # 3 random points
    p1 = vector.randvec(2, 0.0, 10.0,1.0)
    p2 = vector.randvec(2, 0.0, 10.0,1.0)
    p3 = vector.randvec(2, 0.0, 10.0,1.0)
    # prevent div by zero / no line direction
    if tol_eq(vector.norm(p1-p2),0):
        p2 = p1 + p3 * 0.1
    # line (o,v): origin p1, direction p1-p2
    o = p1
    v = (p2 - p1) / vector.norm(p2 - p1)
    # cirlce (c, r): centered in p3, radius p3-p2 + rx
    c = p3
    r0 = vector.norm(p3-p2)
    # cases rx = 0, rx > 0, rx < 0
    case = random.choice([1,2,3])
    if case==1:
        r = r0      #should have one intersection (unles r0 = 0)
    elif case==2:
        r = random.random() * r0   # should have no ints (unless r0=0)
    elif case==3:
        r = r0 + random.random() * r0 # should have 2 ints (unless r0=0) 
    # do interesection 
    diag_print("problem:"+str(c)+","+str(r)+","+str(o)+","+str(v),"test_cl_int")
    sols = cl_int(c,r,o,v)
    diag_print("solutions:"+str(map(str, sols)),"test_cl_int")
    # distance from point on line closest to circle center
    l = vector.dot(c-o, v) / vector.norm(v)
    p = o + v * l / vector.norm(v)  
    d = vector.norm(p-c)
    diag_print("distance center to line="+str(d),"test_cl_int")
    # test number of intersections 
    if len(sols) == 0:
        if not tol_gt(d, r):
            diag_print("wrong number of solutions: 0", "test_cl_int")
            return False
    elif len(sols) == 1:
        if not tol_eq(d, r):
            diag_print("wrong number of solutions: 1", "test_cl_int")
            return False
    elif len(sols) == 2:
        if not tol_lt(d, r):
            diag_print("wrong number of solutions: 2", "test_cl_int")
            return False
    else:
            diag_print("wrong number of solutions: >2", "test_cl_int")

    # test coordinates of intersection 
    for s in sols:
        # s on line (o,v)
        if not is_colinear(s, o, o+v):
            diag_print("solution not on line", "test_cl_int")
            return False
        # s on circle c, r
        if not tol_eq(vector.norm(s-c), r):
            diag_print("solution not on circle", "test_cl_int")
            return False

    return True


def test_intersections():
    sat = True
    for i in range(0,100):
        sat = sat and test_ll_int()
        if not sat: 
            print "ll_int() failed"
            return 
    if sat:
        print "ll_int() passed"
    else:
        print "ll_int() FAILED"

    sat = True
    for i in range(0,100):
        sat = sat and test_rr_int()
        if not sat: 
            print "rr_int() failed"
            return 
    if sat:
        print "rr_int() passed"
    else:
        print "rr_int() FAILED"

    sat = True
    for i in range(0,100):
        sat = sat and test_cc_int()
    if sat:
        print "cc_int() passed"
    else:
        print "cc_int() FAILED"

    sat = True
    for i in range(0,100):
        sat = sat and test_cl_int()
    if sat:
        print "cl_int() passed"
    else:
        print "cl_int() FAILED"

    sat = True
    for i in range(0,100):
        sat = sat and test_sss_int()
    if sat:
        print "sss_int() passed"
    else:
        print "sss_int() FAILED"
    print "Note: did not test degenerate cases for sss_int"

def test_angles():
    print "2D angles" 
    for i in xrange(9):
        a = i * 45 * math.pi / 180
        p1 = vector.vector([1.0,0.0])
        p2 = vector.vector([0.0,0.0])
        p3 = vector.vector([math.cos(a),math.sin(a)])
        print p3, angle_3p(p1,p2,p3) * 180 / math.pi, "flip", angle_3p(p3,p2,p1) * 180 / math.pi
    
    print "3D angles" 
    for i in xrange(9):
        a = i * 45 * math.pi / 180    
        p1 = vector.vector([1.0,0.0,0.0])
        p2 = vector.vector([0.0,0.0,0.0])
        p3 = vector.vector([math.cos(a),math.sin(a),0.0])
        print p3, angle_3p(p1,p2,p3) * 180 / math.pi, "flip", angle_3p(p3,p2,p1) * 180 / math.pi
    

def test_perp_3d():
    for i in range(10):
        u = normalised(vector.randvec(3))
        v,w = perp_3d(u)
        print u, vector.norm(u)
        print v, vector.norm(v)
        print w, vector.norm(w)
        print tol_eq(vector.dot(u,v),0.0) 
        print tol_eq(vector.dot(v,w),0.0) 
        print tol_eq(vector.dot(w,u),0.0) 

def test_sss_degen():
    p1 = vector.vector([0.0, 0.0, 0.0])
    p2 = vector.vector([2.0, 0.0, 0.0])
    p3 = vector.vector([1.0, 0.0, 0.0])
    r1 = 2.0
    r2 = 2.0
    r3 = math.sqrt(3)
    print sss_int(p1,r1,p2,r2,p3,r3)

def test_hcs_degen():
    p1 = vector.vector([0.0, 0.0, 0.0])
    p2 = vector.vector([1.0, 0.0, 0.0])
    p3 = vector.vector([1.0, 0.0, 0.0])
    print make_hcs_3d(p1,p2,p3)
        
if __name__ == '__main__': 
    #diag_select("test_cc_int")
    #diag_select("test_cl_int")
    #diag_select(".*")
    test_intersections()
    #test_angles()
    #test_perp_3d()
    #test_sss_degen()
    #test_hcs_degen()
