#!/usr/bin/env python
"""This module provides some tests for the GeoSolver. 
These tests are concerned with geometric primitives.
The tests are also simple examples of how to use of the GeomSolver API"""

import random
from test_generic import test
from geosolver.geometric import GeometricProblem, GeometricSolver, DistanceConstraint, AngleConstraint, FixConstraint
from geosolver.geometric import Point, Line, CoincidenceConstraint
from geosolver.vector import vector 
from geosolver.diagnostic import diag_select, diag_print

# ---------- 3d ----------

def line_problem_3d_0():
    """A problem with a Line (and no CoincicentConstraints)"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    return problem 


def line_problem_3d_1():
    """A problem with a Line and 1 CoincicentConstraint"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Point('p1'),vector([3.0, 2.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    return problem 


def line_problem_3d_2():
    """A problem with a Line and 2 CoincicentConstraints"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Point('p1'),vector([3.0, 2.0, 1.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    return problem 

def line_problem_3d_3():
    """A problem with a Line and a 3 CoincicentConstraints"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Point('p1'),vector([3.0, 2.0, 1.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    problem.add_variable(Point('p3'),vector([0.0, 0.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p3'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p3'), 8.0))
    return problem 

def line_problem_3d_4():
    """A problem with a Line and a 4 CoincicentConstraints"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Point('p1'),vector([3.0, 2.0, 1.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    problem.add_variable(Point('p3'),vector([0.0, 0.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p3'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p3'), 8.0))
    problem.add_variable(Point('p4'),vector([1.0, 0.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p4'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p4'), 0.1))
    return problem 

# ------------2d

def line_problem_2d_0():
    """A problem with a Line (and no CoincicentConstraints)"""
    problem = GeometricProblem(dimension=2)
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 1.0, 1.0]))
    return problem 


def line_problem_2d_1():
    """A problem with a Line and 1 CoincicentConstraint"""
    problem = GeometricProblem(dimension=2)
    problem.add_variable(Point('p1'),vector([3.0, 2.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    return problem 


def line_problem_2d_2():
    """A problem with a Line and 2 CoincicentConstraints"""
    problem = GeometricProblem(dimension=2)
    problem.add_variable(Point('p1'),vector([3.0, 2.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    return problem 

def line_problem_2d_3a():
    """A problem with a Line and a 3 CoincicentConstraints"""
    problem = GeometricProblem(dimension=2)
    problem.add_variable(Point('p1'),vector([3.0, 2.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    problem.add_variable(Point('p3'),vector([1.0, 0.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p3'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p3'), Point('p2'), 8.0))
    return problem 

def line_problem_2d_3b():
    """A problem with a Line and a 3 CoincicentConstraints"""
    problem = GeometricProblem(dimension=2)
    problem.add_variable(Point('p1'),vector([3.0, 2.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    problem.add_variable(Point('p3'),vector([1.0, 0.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p3'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p3'), 8.0))
    return problem 


def line_problem_2d_4():
    """A problem with a Line and a 4 CoincicentConstraints"""
    problem = GeometricProblem(dimension=2)
    problem.add_variable(Point('p1'),vector([3.0, 2.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    problem.add_variable(Point('p3'),vector([0.0, 0.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p3'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p3'), 8.0))
    problem.add_variable(Point('p4'),vector([1.0, 0.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p4'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p4'), 0.1))
    return problem 


def test_line():
    diag_select("(GeometricSolver)|(CoincidenceConstraint)")
    #test(line_problem_2d_0())
    #test(line_problem_2d_1())
    #test(line_problem_2d_2())
    test(line_problem_2d_3a())
    #test(line_problem_2d_3b())
    #test(line_problem_2d_4())

    #test(line_problem_3d_0())
    #test(line_problem_3d_1())
    #test(line_problem_3d_2())
    #test(line_problem_3d_3())
    #test(line_problem_3d_4())

if __name__ == "__main__": 
    test_line()
