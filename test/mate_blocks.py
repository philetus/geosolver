#!/usr/bin/env python
"""This module provides some tests for the GeoSolver. 
The tests are also simple examples of how to use of the GeoSolver API"""

from geosolver.geometric import *
from geosolver.vector import vector, norm 
from geosolver.randomproblem import *
from geosolver.diagnostic import diag_select, diag_print
import geosolver.tolerance as tolerance
from time import time
from geosolver.graph import Graph
from geosolver.intersections import translate_3D, rotate_3D_x, rotate_3D_y, rotate_3D_z,scale_3D, id_transform_3D

# ------- generic test -------

def test(problem):
    """Test solver on a given problem"""
    #diag_select(".*")
    print "problem:"
    print problem
    solver = GeometricSolver(problem, use_prototype=True)
    #print "drplan:"
    #print solver.dr
    #print "number of top-level rigids:",len(solver.dr.top_level())
    result = solver.get_result()
    print "result:"
    print result
    print "result is",result.flag, "with", len(result.solutions),"solutions"
    check = True
    if len(result.solutions) == 0:
        check = False
    for sol in result.solutions:
        print "solution:",sol
        check = check and problem.verify(sol)
    if check: 
        print "all solutions valid"
    else:
        print "INVALID"
        for sol in result.solutions:
            print sol
            for constraint in problem.cg.constraints():
                print constraint, constraint.satisfied(sol)
  

# ------------- creating and manupulating blocks ---------

def block_var(block, index):
    return str(block)+"#"+str(index)

def add_block(problem,name,x,y,z):
    """A block with variables name+#1...8 and dimensions x,y,z"""
    problem.add_point(block_var(name,'left-bot-front'), vector([-1.0, -1.0, -1.0]))
    problem.add_point(block_var(name,'left-bot-back'), vector([-1.0, -1.0, 1.0]))
    problem.add_point(block_var(name,'left-top-front'), vector([-1.0, 1.0, -1.0]))
    problem.add_point(block_var(name,'left-top-back'), vector([-1.0, 1.0, 1.0]))
    problem.add_point(block_var(name,'right-bot-front'), vector([1.0, -1.0, -1.0]))
    problem.add_point(block_var(name,'right-bot-back'), vector([1.0, -1.0, 0.0]))
    problem.add_point(block_var(name,'right-top-front'), vector([1.0, 1.0, -1.0]))
    problem.add_point(block_var(name,'right-top-back'), vector([1.0, 1.0, 1.0]))
    conf = Configuration({
        block_var(name,'left-bot-front'):vector([-x/2, -y/2, -z/2]),
        block_var(name,'left-bot-back'):vector([-x/2, -y/2, +z/2]),
        block_var(name,'left-top-front'):vector([-x/2, +y/2, -z/2]),
        block_var(name,'left-top-back'):vector([-x/2, +y/2, +z/2]),
        block_var(name,'right-bot-front'):vector([+x/2, -y/2, -z/2]),
        block_var(name,'right-bot-back'):vector([+x/2, -y/2, +z/2]),
        block_var(name,'right-top-front'):vector([+x/2, +y/2, -z/2]),
        block_var(name,'right-top-back'):vector([+x/2, +y/2, +z/2])
    })
    problem.add_constraint(RigidConstraint(conf))
    return problem

def mate_blocks(problem, block1, o1, x1, y1, block2, o2, x2, y2, dx, dy):
    """Mate two blocks.
       block1 and block2 are the names of the blocks. 
       o1, x1 and x2 are vertices of the blocks.
       o1-x1 identifies the so-called x-edge in block1. 
       o1-y1 identifies the y-edge in block1. 
       --- no longer needed -- The x-edge and y-edge must be actual egdes in block1, or an error will be generated. 
       The same for block2.
       dx is the relative position of the x-edges of the two blocks. 
       dy is the relative position of the y-edges of the two blocks. 
       Note that if the blocks are not actually block-shaped, the axis will not be properly 
       aligned and the faces will not be properly mated.
    """
    # determine variable names of the points
    vo1 = block_var(block1,o1)
    vx1 = block_var(block1,x1)
    vy1 = block_var(block1,y1)
    vo2 = block_var(block2,o2)
    vx2 = block_var(block2,x2)
    vy2 = block_var(block2,y2)
    # ---- no longer needed --- determine points opposite to given origin and plane
    # vz1 = block_var(block1,get_block_opposite(o1, x1, y1))
    # vz2 = block_var(block2,get_block_opposite(o2, x2, y2))
    # determine transformation
    trans = translate_3D(dx, dy,0.0)
    # add constraint
    problem.add_constraint(MateConstraint(vo1,vx1,vy1,vo2,vx2,vy2,trans))


# ----- no longer used, but maybe in the future? -- ----

# create a graph of the edges in a block 
blockgraph = Graph()
edges = [('left-bot-front','left-bot-back'), 
         ('left-bot-front','left-top-front'), 
         ('left-bot-front','right-bot-front'), 
         ('left-bot-back','left-top-back'),
         ('left-bot-back','right-bot-back'),
         ('left-top-front','left-top-back'), 
         ('left-top-front','right-top-front'), 
         ('left-top-back','right-top-back'), 
         ('right-bot-front','right-bot-back'), 
         ('right-bot-front','right-top-front'), 
         ('right-bot-back','right-top-back'), 
         ('right-top-font','right-top-back')]

for edge in edges:
    # add bi-directional edge to graoh
    blockgraph.add_bi(edge[0], edge[1])

def get_block_opposite(o, x, y):
    """return the index of the vertex connected to o but not connected to x and y""" 
    if not blockgraph.has_vertex(o):
        raise Exception, "vertex %s is not a block vertex"%(str(o))
    # determine vertices connected to 
    connected = list(blockgraph.outgoing_vertices(o))
    if x not in connected:
        raise Exception, "edge (%s,%s) is not a block edge"%(str(o),str(x))
    if y not in connected:
        raise Exception, "edge (%s,%s) is not a block edge"%(str(o),str(y))
    connected.remove(x) 
    connected.remove(y)
    if len(connected) != 1:
        raise Exception, "could not find opposite edge, because I am an idiot."
    return connected[0]

# ----------- test mate constraint

def test_mate():
    problem = GeometricProblem(dimension=3)
    
    # create and  mate two blocks
    add_block(problem, "A", 4.0, 2.0, 6.0)
    add_block(problem, "B", 4.0, 2.0, 6.0)
    mate_blocks(problem, "A", 'right-bot-front','right-bot-back','right-top-front',
                         "B", 'left-bot-front','left-bot-back','left-top-front', 
                0.5, 0.0)
    # add global coordinate system
    problem.add_point("origin",vector([0.0,0.0,0.0]))
    problem.add_point("x-axis",vector([1.0,0.0,0.0]))
    problem.add_point("y-axis",vector([0.0,1.0,0.0]))
    problem.add_constraint(FixConstraint("origin",vector([0.0,0.0,0.0])))
    problem.add_constraint(FixConstraint("x-axis",vector([1.0,0.0,0.0])))
    problem.add_constraint(FixConstraint("y-axis",vector([0.0,1.0,0.0])))
    
    # fix block1 to cs
    problem.add_constraint(MateConstraint("origin","x-axis","y-axis",
        block_var("A", "left-bot-front"),block_var("A", "right-bot-front"),block_var("A", "left-top-front"),
        id_transform_3D()))
   
    test(problem)
    

if __name__ == "__main__": 
    #test_twoblocks()
    #test_z_index()
    test_mate()
   
