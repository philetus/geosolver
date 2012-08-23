#!/usr/bin/env python
"""This module provides some generic tests routines for the GeoSolver. 
These can be used by other specific test modules, i.e. 2d, 3d, etc.
The tests are also simple examples of how to use of the GeomSolver API"""

from geosolver.geometric import GeometricProblem, GeometricSolver
from geosolver.vector import vector 
from geosolver.diagnostic import diag_select, diag_print
import geosolver.tolerance as tolerance

# ------- generic test -------

def test(problem):
    """Test solver on a given problem"""
    #diag_select(".*")
    print "problem:"
    print problem
    print "Solving..."
    solver = GeometricSolver(problem)
    print "...done"
    print "drplan:"
    print solver.dr
    print "top-level rigids:",list(solver.dr.top_level())
    result = solver.get_result()
    print "result:"
    print result
    print "result is",result.flag, "with", len(result.solutions),"solutions"
    check = True
    if len(result.solutions) == 0:
        check = False
    diag_select("(GeometricProblem.verify)|(satisfied)")
    for sol in result.solutions:
        print "solution:",sol
        check = check and problem.verify(sol)
    if check: 
        print "all solutions valid"
    else:
        print "INVALID"
  

