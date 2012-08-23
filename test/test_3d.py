#!/usr/bin/env python
"""This module provides some tests for the GeoSolver. 
These tests are concerned with 3D solving.
The tests are also simple examples of how to use of the GeomSolver API"""

import random
import math
from test_generic import test
from geosolver.geometric import GeometricProblem, GeometricSolver, DistanceConstraint,AngleConstraint, FixConstraint,RightHandedConstraint
from geosolver.vector import vector 
from geosolver.randomproblem import random_triangular_problem_3D, random_distance_problem_3D
from geosolver.diagnostic import diag_select, diag_print
from geosolver.intersections import distance_2p, angle_3p

# ---------- 3D problems -----

def fix3_problem_3d():
    """A problem with a fix constraint"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.0, 0.0, 1.0]))
    #problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    #problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    #problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(FixConstraint('v1', vector([0.0,0.0,0.0])))
    problem.add_constraint(FixConstraint('v2', vector([10.0,0.0,0.0])))
    problem.add_constraint(FixConstraint('v3', vector([5.0,5.0,0.0])))
    return problem

def fix2_problem_3d():
    """A problem with a fix constraint"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.0, 0.0, 1.0]))
    #problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(FixConstraint('v1', vector([0.0,0.0,0.0])))
    problem.add_constraint(FixConstraint('v2', vector([10.0,0.0,0.0])))
    return problem

def fix1_problem_3d():
    """A problem with a fix constraint"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.0, 0.0, 1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(FixConstraint('v1', vector([0.0,0.0,0.0])))
    return problem


    
def double_banana_problem():
    """The double banana problem"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_point('v5', vector([0.5, 0.5,-1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v5', 10.0))
    
    problem.add_point('w1', vector([0.0, 0.0, 0.0]))
    problem.add_point('w2', vector([1.0, 0.0, 0.0]))
    problem.add_point('w3', vector([0.0, 1.0, 0.0]))
    problem.add_constraint(DistanceConstraint('w1', 'w2', 10.0))
    problem.add_constraint(DistanceConstraint('w1', 'w3', 10.0))
    problem.add_constraint(DistanceConstraint('w2', 'w3', 10.0))
    problem.add_constraint(DistanceConstraint('w1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('w2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('w3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('w1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('w2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('w3', 'v5', 10.0))
    
    return problem

def double_banana_plus_one_problem():
    """The double banana problem, plus one constraint (well-constrained)"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_point('v5', vector([0.5, 0.5,-1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v5', 10.0))
    
    problem.add_point('w1', vector([0.0, 0.0, 0.0]))
    problem.add_point('w2', vector([1.0, 0.0, 0.0]))
    problem.add_point('w3', vector([0.0, 1.0, 0.0]))
    problem.add_constraint(DistanceConstraint('w1', 'w2', 10.0))
    problem.add_constraint(DistanceConstraint('w1', 'w3', 10.0))
    problem.add_constraint(DistanceConstraint('w2', 'w3', 10.0))
    problem.add_constraint(DistanceConstraint('w1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('w2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('w3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('w1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('w2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('w3', 'v5', 10.0))
   
    problem.add_constraint(DistanceConstraint('v1', 'w1', 10.0))
 
    return problem


def double_tetrahedron_problem():
    """The double tetrahedron problem"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_point('v5', vector([0.5, 0.5,-1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v5', 10.0))
    return problem


def dad_tetrahedron_problem():
    """The double tetrahedron problem with an angle"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_point('v5', vector([0.5, 0.5,-1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(AngleConstraint('v2', 'v1','v3', 60.0*math.pi/180.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v5', 10.0))
    return problem

def ada_tetrahedron_problem():
    """The double tetrahedron problem with an angle"""
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_point('v5', vector([0.5, 0.5,-1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(AngleConstraint('v3', 'v1','v2', 60.0*math.pi/180.0))
    problem.add_constraint(AngleConstraint('v1', 'v2','v3', 60.0*math.pi/180.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v5', 10.0))
    return problem

def ada_3d_problem():
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([random.random() for i in [1,2]]))
    problem.add_point('v2', vector([random.random() for i in [1,2]]))
    problem.add_point('v3', vector([random.random() for i in [1,2]]))
    problem.add_constraint(DistanceConstraint('v1','v2',distance_2p(problem.get_point('v1'), problem.get_point('v2'))))
    problem.add_constraint(AngleConstraint('v3', 'v1', 'v2', 
       angle_3p(problem.get_point('v3'), problem.get_point('v1'), problem.get_point('v2'))
    ))
    problem.add_constraint(AngleConstraint('v1', 'v2', 'v3',
       angle_3p(problem.get_point('v1'), problem.get_point('v2'), problem.get_point('v3'))
    ))
    return problem




def overconstrained_tetra():
    problem = GeometricProblem(dimension=3)
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    # overconstrain me!
    problem.add_constraint(AngleConstraint('v1', 'v2', 'v3', math.pi/3))
    #problem.add_constraint(AngleConstraint('v1', 'v2', 'v3', math.pi/4))
    return problem

def diamond_3d():
    """creates a diamond shape with point 'v1'...'v4' in 3D with one solution"""
    # Following should be well-constraint, gives underconstrained (need extra rule/pattern) 
    L=10.0
    problem = GeometricProblem(dimension=3, use_prototype=False)      # no prototype based selection
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([-5.0, 5.0, 0.0]))
    problem.add_point('v3', vector([5.0, 5.0, 0.0]))
    problem.add_point('v4', vector([0.0, 10.0, 0.0]))
    problem.add_constraint(DistanceConstraint('v1', 'v2', L))
    problem.add_constraint(DistanceConstraint('v1', 'v3', L))
    problem.add_constraint(DistanceConstraint('v2', 'v3', L))
    problem.add_constraint(DistanceConstraint('v2', 'v4', L))
    problem.add_constraint(DistanceConstraint('v3', 'v4', L))
    # this bit of code constrains the points v1...v4 in a plane with point p above it
    problem.add_point('p', vector([0.0, 0.0, 1.0]))
    problem.add_constraint(DistanceConstraint('v1', 'p', 1.0))
    problem.add_constraint(AngleConstraint('v2','v1','p', math.pi/2))
    problem.add_constraint(AngleConstraint('v3','v1','p', math.pi/2))
    problem.add_constraint(AngleConstraint('v4','v1','p', math.pi/2))
    return problem

# ----------- 3d tests ----------

def test_ada_3d():
    problem = ada_3d_problem()
    diag_select("nothing")
    print "problem:"
    print problem
    solver = GeometricSolver(problem)
    print "drplan:"
    print solver.dr
    print "number of top-level rigids:",len(solver.dr.top_level())
    result = solver.get_result()
    print "result:"
    print result
    print "result is",result.flag, "with", len(result.solutions),"solutions"
    check = True
    if len(result.solutions) == 0:
        check = False
    diag_select(".*")
    for sol in result.solutions:
        print "solution:",sol
        check = check and problem.verify(sol)
    diag_select("nothing")
    if check: 
        print "all solutions valid"
    else:
        print "INVALID"

def selection_test():
    problem = GeometricProblem(dimension=3,use_prototype=False)
    
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_point('v5', vector([0.5, 0.5,-1.0]))
    
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v5', 10.0))

    s1 = RightHandedConstraint('v1','v2','v4','v5')
    
    # add selection con
    problem.add_constraint(s1)
    
    # solve
    solver = GeometricSolver(problem)
    print len(solver.get_solutions()), "solutions"
    
    # remove and add constraint
    print "removing selection-constraint"
    problem.rem_constraint(s1)

    # solve again
    print len(solver.get_solutions()), "solutions"

    # remove and add constraint
    print "re-adding selection constraint"
    problem.add_constraint(s1)

    # solve again
    print len(solver.get_solutions()), "solutions"

    # remove distance
    print "removing and re-adding distance v1-v5"
    problem.rem_constraint(problem.get_distance("v1","v5"))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))

    # solve again
    print len(solver.get_solutions()), "solutions"

def selection_problem():
    """The double tetrahedron problem with selection constraints"""
    
    problem = GeometricProblem(dimension=3, use_prototype=False)  # no prototype based selection
    
    problem.add_point('v1', vector([0.0, 0.0, 0.0]))
    problem.add_point('v2', vector([1.0, 0.0, 0.0]))
    problem.add_point('v3', vector([0.0, 1.0, 0.0]))
    problem.add_point('v4', vector([0.5, 0.5, 1.0]))
    problem.add_point('v5', vector([0.5, 0.5,-1.0]))
    
    problem.add_constraint(DistanceConstraint('v1', 'v2', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v3', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v4', 10.0))
    problem.add_constraint(DistanceConstraint('v1', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v2', 'v5', 10.0))
    problem.add_constraint(DistanceConstraint('v3', 'v5', 10.0))

    #problem.add_constraint(SelectionConstraint(is_right_handed, ['v1','v2','v4','v5']))
    problem.add_constraint(RightHandedConstraint('v1','v2','v4','v5'))
    
    return problem


def test3d():
    #diag_select("clsolver")
    test(double_tetrahedron_problem())
    test(ada_tetrahedron_problem())
    test(double_banana_problem())
    test(double_banana_plus_one_problem())
    test(random_triangular_problem_3D(10,10.0,0.0,0.5))
    test(random_distance_problem_3D(10,1.0,0.0))
    test(fix1_problem_3d())
    test(fix2_problem_3d())
    test(fix3_problem_3d())
    test(selection_problem())
    selection_test()
    test(overconstrained_tetra())
    test(diamond_3d())

if __name__ == "__main__": 
    test3d()
