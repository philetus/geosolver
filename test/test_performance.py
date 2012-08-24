#!/usr/bin/env python
"""This module provides some tests for the GeoSolver. 
These test are concerned with the performance of the solver
The tests are also simple examples of how to use of the GeomSolver API"""

import random
import math
from test_generic import test
from geosolver.geometric import GeometricProblem, GeometricSolver, DistanceConstraint,AngleConstraint, FixConstraint,RightHandedConstraint
from geosolver.vector import vector 
from geosolver.randomproblem import random_triangular_problem_3D, random_distance_problem_3D
from geosolver.diagnostic import diag_select, diag_print
from geosolver.intersections import distance_2p, angle_3p
from time import time

# create statistics for solving time
def stats_solving(minsize, maxsize, repeats):
    print "times for solving problems from scratch"
    print "size \t # \t time \t result"
    for size in range(minsize,maxsize+1):
        for i in range(1,repeats+1):
            problem = random_triangular_problem_3D(size,10.0,0.0,0.0)
            t1 = time()
            solver = GeometricSolver(problem)
            result = solver.get_status()
            t2 = time()
            t = t2-t1
            print size,"\t",i,"\t",t,"\t",result

# create statistics for incremental solving time
def stats_incremental(minsize, maxsize, repeats):
    #diag_select("clsolver.remove")
    print "times for incremental re-solving (one constraint removed and re-added)"
    print "size \t # \t time \t result"
    for size in range(minsize,maxsize+1):
        for i in range(1,repeats+1):
            problem = random_triangular_problem_3D(size,10.0,0.0,0.0)
            solver = GeometricSolver(problem)
            t1 = time()
            constraint = random.choice(problem.cg.constraints())
            problem.rem_constraint(constraint)
            problem.add_constraint(constraint)
            result = solver.get_status()
            t2 = time()
            t = t2-t1
            print size,"\t",i,"\t",t,"\t",result

# create statistics for parametric change
def stats_parametric(minsize, maxsize, repeats):
    #diag_select("clsolver.remove")
    print "times for parameteric updates (one constraint parameter)"
    print "size \t # \t time \t result"
    for size in range(minsize,maxsize+1):
        for i in range(1,repeats+1):
            problem = random_triangular_problem_3D(size,10.0,0.0,0.0)
            solver = GeometricSolver(problem)
            constraint = random.choice(problem.cg.constraints())
            t1 = time()
            constraint.set_parameter(constraint.get_parameter())
            result = solver.get_status()
            t2 = time()
            t = t2-t1
            print size,"\t",i,"\t",t,"\t",result

def runstats():
    minsize = 4
    maxsize = 10
    repeats = 1
    stats_solving(minsize, maxsize, repeats) 
    stats_incremental(minsize, maxsize, repeats) 
    stats_parametric(minsize, maxsize, repeats) 

if __name__ == "__main__": 
    runstats()
