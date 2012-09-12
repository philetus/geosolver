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

def line_problem1():
    """A problem with a Point, a Line and a CoincicentConstraint"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    return problem 


def line_problem2():
    """A problem with a Point, a Line and a CoincicentConstraint"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Point('p1'),vector([3.0, 2.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    return problem 


def line_problem3():
    """A problem with a Point, a Line and a CoincicentConstraint"""
    problem = GeometricProblem(dimension=3)
    problem.add_variable(Point('p1'),vector([3.0, 2.0, 1.0]))
    problem.add_variable(Point('p2'),vector([1.0, 1.0, 1.0]))
    problem.add_variable(Line('l1'),vector([0.0, 0.0, 0.0, 1.0, 1.0, 1.0]))
    problem.add_constraint(CoincidenceConstraint(Point('p1'), Line('l1')))
    problem.add_constraint(CoincidenceConstraint(Point('p2'), Line('l1')))
    problem.add_constraint(DistanceConstraint(Point('p1'), Point('p2'), 5.0))
    return problem 

def test_line():
    test(line_problem3())

if __name__ == "__main__": 
    test_line()
