"""A generic 2D geometric constraint solver."""

from clsolver import *
from diagnostic import diag_print, diag_select
from selconstr import *
from intersections import *
from configuration import Configuration
from cluster import *
from map import Map
import incremental


class ClusterSolver2D(ClusterSolver):
    """A 2D geometric constraint solver. See ClusterSolver for details."""  
       # ------- PUBLIC METHODS --------

    def __init__(self):
        """Instantiate a ClusterSolver2D"""
        ClusterSolver.__init__(self, [CheckAR, MergePR, MergeRR, DeriveDDD, DeriveDAD])
        

# ----------------------------------------------
# ---------- Methods for 2D solving -------------
# ----------------------------------------------

# Merge<X> methods take root cluster in considerations   
# Derive<X> methods do not take root cluster in consideration

class MergePR(ClusterMethod):
    """Represents a merging of a one-point cluster with any other rigid."""
    def __init__(self, map):
        # check inputs
        in1 = map["$p"]
        in2 = map["$r"]
        # create ouput
        outvars = set(in1.vars).union(in2.vars)
        out = Rigid(outvars)
        # set method properties
        in1root = rootname(in1)
        in2root = rootname(in2)
        self._inputs = [in1, in2, in1root, in2root]
        self._outputs = [out]
        ClusterMethod.__init__(self)

    def _incremental_matcher(solver):
        toplevel = solver.top_level()
        rigids = Rigids(solver)
        points = Points(solver)
        connectedpairs = ConnectedPairs2(solver, points, rigids)
        matcher = incremental.Map(lambda (p,r): MergePR({"$p":p, "$r":r}), connectedpairs)
        return matcher
    
    incremental_matcher = staticmethod(_incremental_matcher)
    
    def __str__(self):
        s =  "MergePR("+str(self._inputs[0])+"+"+str(self._inputs[1])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("MergePR.multi_execute called","clmethods")
        #c1 = self._inputs[0]
        #c2 = self._inputs[1]
        conf1 = inmap[self._inputs[0]]
        conf2 = inmap[self._inputs[1]]
        isroot1 = inmap[self._inputs[2]]
        isroot2 = inmap[self._inputs[3]]
        if isroot1:
            res = conf1.merge(conf2)
        elif isroot2:
            res = conf2.merge(conf1)
        else: # cheapest - just copy reference
            res = conf2
        return [res]

class MergeRR(ClusterMethod):
    """Represents a merging of two rigids sharing two points."""
    def __init__(self, map):
        # check inputs
        in1 = map["$r1"]
        in2 = map["$r2"]
        # create output
        out = Rigid(set(in1.vars).union(in2.vars))
        # set method parameters
        in1root = rootname(in1)
        in2root = rootname(in2)
        self._inputs = [in1, in2, in1root, in2root]
        self._outputs = [out]
        ClusterMethod.__init__(self)

    #def _pattern():
    #    pattern = [["rigid","$r1",["$a","$b"]], ["rigid", "$r2", ["$a", "$b"]]]
    #    return pattern2graph(pattern)
    #pattern = staticmethod(_pattern)
    #patterngraph = _pattern()

    def _incremental_matcher(solver):
        toplevel = solver.top_level()
        rigids = Rigids(solver)
        connectedpairs = ConnectedPairs1(solver, rigids)
        twoconnectedpairs = incremental.Filter(lambda (r1,r2): len(r1.vars.intersection(r2.vars))==2, connectedpairs);
        matcher = incremental.Map(lambda (r1,r2): MergeRR({"$r1":r1, "$r2":r2}), twoconnectedpairs)
        return matcher
    
    incremental_matcher = staticmethod(_incremental_matcher)


    def __str__(self):
        s =  "MergeRR("+str(self._inputs[0])+"+"+str(self._inputs[1])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("MergeRR.multi_execute called","clmethods")
        c1 = self._inputs[0]
        c2 = self._inputs[1]
        conf1 = inmap[c1]
        conf2 = inmap[c2]
        isroot1 = inmap[self._inputs[2]]
        isroot2 = inmap[self._inputs[3]]
        if isroot1 and not isroot2:
            res = conf1.merge(conf2)
        elif isroot2 and not isroot1:
            res = conf2.merge(conf1)
        elif len(c1.vars) < len(c2.vars):  # cheapest - transform smallest config
            res = conf2.merge(conf1)
        else:
            res = conf1.merge(conf2)
        return [res]


def triplet2ddd(triplet):
    (d_ab,d_ac,d_bc) = triplet
    a = list(d_ab.vars.intersection(d_ac.vars))[0]
    b = list(d_ab.vars.intersection(d_bc.vars))[0]
    c = list(d_ac.vars.intersection(d_bc.vars))[0]
    return DeriveDDD({"$d_ab":d_ab, "$d_ac":d_ac, "$d_bc":d_bc, "$a": a, "$b":b, "$c":c})


class DeriveDDD(ClusterMethod):
    """Represents a merging of three distances"""
    def __init__(self, map):
        # check inputs
        self.d_ab = map["$d_ab"]
        self.d_ac = map["$d_ac"]
        self.d_bc = map["$d_bc"]
        self.a = map["$a"]
        self.b = map["$b"]
        self.c = map["$c"]
        # create output
        out = Rigid([self.a,self.b,self.c])
        # get roots        
        self.root_ab = rootname(self.d_ab)
        self.root_ac = rootname(self.d_ac)
        self.root_bc = rootname(self.d_bc)
        # set method parameters
        self._inputs = [self.d_ab, self.d_ac, self.d_bc, self.root_ab, self.root_ac, self.root_bc]
        self._outputs = [out]
        ClusterMethod.__init__(self)
        # do not remove input clusters (because root not considered here)
        # self.noremove = True

    #def _pattern():
    #    pattern = [["rigid","$d_ab",["$a", "$b"]], 
    #        ["rigid", "$d_ac",["$a", "$c"]], 
    #        ["rigid", "$d_bc",["$b","$c"]]]
    #    return pattern2graph(pattern)
    #pattern = staticmethod(_pattern)
    #patterngraph = _pattern()

    def _incremental_matcher(solver):
        triplets = Triplets(solver, Rigids(solver))
        matcher = incremental.Map(triplet2ddd, triplets)
        return matcher
    
    incremental_matcher = staticmethod(_incremental_matcher)

    def __str__(self):
        s =  "DeriveDDD("+str(self._inputs[0])+"+"+str(self._inputs[1])+"+"+str(self._inputs[2])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("DeriveDDD.multi_execute called","clmethods")
        c12 = inmap[self.d_ab]
        c13 = inmap[self.d_ac]
        c23 = inmap[self.d_bc]
        v1 = self.a
        v2 = self.b
        v3 = self.c
        d12 = distance_2p(c12.get(v1),c12.get(v2))
        d31 = distance_2p(c13.get(v1),c13.get(v3))
        d23 = distance_2p(c23.get(v2),c23.get(v3))
        solutions = solve_ddd(v1,v2,v3,d12,d23,d31)

        # transform solutions to align with root input cluster
        isroot_ab = inmap[self.root_ab]
        isroot_ac = inmap[self.root_ac]
        isroot_bc = inmap[self.root_bc]
        for i in range(len(solutions)):
            if isroot_ab:
                solutions[i] = c12.merge(solutions[i])
            elif isroot_ac:
                solutions[i] = c13.merge(solutions[i])
            elif isroot_bc:
                solutions[i] = c23.merge(solutions[i])
        return solutions

    def prototype_constraints(self):
        constraints = []
        constraints.append(SelectionConstraint(fnot(is_clockwise),[self.a,self.b,self.c]))
        constraints.append(SelectionConstraint(fnot(is_counterclockwise),[self.a,self.b,self.c]))
        return constraints


class DeriveDAD(ClusterMethod):
    """Represents a merging of two distances and an angle"""
    def __init__(self, map):
        # check inputs
        self.d_ab = map["$d_ab"]
        self.a_abc = map["$a_abc"]
        self.d_bc = map["$d_bc"]
        self.a = map["$a"]
        self.b = map["$b"]
        self.c = map["$c"]
        # create output
        out = Rigid([self.a,self.b,self.c])
        # set method parameters
        self._inputs = [self.d_ab, self.a_abc, self.d_bc]
        self._outputs = [out]
        ClusterMethod.__init__(self)
        # do not remove input clusters (because root not considered here)
        self.noremove = True

    #def _pattern():
    #    pattern = [["rigid","$d_ab",["$a", "$b"]], 
    #        ["hedgehog", "$a_abc",["$b", "$a", "$c"]], 
    #        ["rigid", "$d_bc",["$b","$c"]]]
    #    return pattern2graph(pattern)
    #pattern = staticmethod(_pattern)
    #patterngraph = _pattern()

    def _incremental_matcher(solver):
        
        def isdad(triplet):
            dad = triplet2dad(triplet)
            return isinstance(DeriveDAD, dad)
    
        def triplet2dad(triplet):
            print "triplet2dad: start"
            hogs = filter(lambda c: isinstance(Hog, c), triplet)
            rigids= filter(lambda c: isinstance(Rigid, c), triplet)
            if not(len(hogs)==1 and len(rigids)==2): return None
            hog = hogs[0]
            r1 = rigids[0]
            r2 = rigids[2]
            b = hog.apex;
            print "triplet2dad: b = ", b    
            if not(b in r1.vars): return None
            if not(b in r2.vars): return None
            print "triplet2dad: b in rigids"
            p1s = r1.vars.intersection(hog.vars) 
            p2s = r2.vars.intersection(hog.vars)
            if not(len(p1s) == 1): return None
            if not(len(p2s) == 1): return None
            a = p1s[0]
            b = p1s[1]
            print "triplet2dad: a =  ", a
            print "triplet2dad: c =  ", c
            return DeriveDAD( {"$d_ab":r1, "$a_abc":hog, "$d_bc":r2, "$a":a, "$b":b, "$c":c })
        # end def
        triplets = Triplets(solver, solver.top_level())
        matchtriplets = incremental.Filter(lambda triplet: isdad(triplet), triplets)
        matcher = incremental.Map(triplet2dad, matchtriplets)
        return matcher
    
    incremental_matcher = staticmethod(_incremental_matcher)


    def __str__(self):
        s =  "DeriveDAD("+str(self._inputs[0])+"+"+str(self._inputs[1])+"+"+str(self._inputs[2])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("DeriveDAD.multi_execute called","clmethods")
        c12 = inmap[self.d_ab]
        c123 = inmap[self.a_abc]
        c23 = inmap[self.d_bc]
        v1 = self.a
        v2 = self.b
        v3 = self.c
        d12 = distance_2p(c12.get(v1),c12.get(v2))
        a123 = angle_3p(c123.get(v1),c123.get(v2),c123.get(v3))
        d23 = distance_2p(c23.get(v2),c23.get(v3))
        solutions = solve_dad(v1,v2,v3,d12,a123,d23)
        return solutions

class CheckAR(ClusterMethod):
    """Represents the overconstrained merging a hedgehog and a rigid that completely overlaps it."""
    def __init__(self, map):
        # get input clusters
        self.hog = map["$h"]
        self.rigid = map["$r"]
        self.sharedx = self.hog.xvars.intersection(self.rigid.vars)
        # create ouptut cluster
        outvars = set(self.rigid.vars)
        self.out = Rigid(outvars)
        # set method properties
        self._inputs = [self.hog, self.rigid]
        self._outputs = [self.out]
        ClusterMethod.__init__(self)

    def _handcoded_match(problem, newcluster, connected):
        matches = [];
        if isinstance(newcluster, Rigid) and len(newcluster.vars)>=3:
            rigids = [newcluster]
            hogs = filter(lambda hog: isinstance(hog, Hedgehog) and hog.vars.intersection(newcluster.vars) == hog.vars, connected)
        elif isinstance(newcluster, Hedgehog):
            hogs = [newcluster]
            rigids = filter(lambda rigid: isinstance(rigid, Rigid) and newcluster.vars.intersection(rigid.vars) == newcluster.vars, connected)
        else:
            return []
        for h in hogs: 
            for r in rigids: 
                m = Map({
                    "$h": h, 
                    "$r": r,
                })
                matches.append(m)
        return matches;
    handcoded_match = staticmethod(_handcoded_match)

    def __str__(self):
        s =  "CheckAR("+str(self._inputs[0])+"+"+str(self._inputs[1])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("CheckAR.multi_execute called","clmethods")
        # get configurations
        hog = inmap[self.hog]
        rigid = inmap[self.rigid]
        xvars = list(self.hog.xvars)
        # test if all angles match
        for i in range(len(self.sharedx)-1):
            hangle = angle_3p(hog.get(xvars[i]), hog.get(self.hog.cvar), hog.get(xvars[i+1]))
            rangle = angle_3p(rigid.get(xvars[i]), rigid.get(self.hog.cvar), rigid.get(xvars[i+1]))
            # angle check failed, return no configuration
            if not tol_eq(hangle,rangle):
                return []
        # all checks passed, return rigid configuration 
        return [rigid]
    

# ---------------------------------------------------------
# ------- functions to determine configurations  ----------
# ---------------------------------------------------------

def solve_ddd(v1,v2,v3,d12,d23,d31):
    diag_print("solve_ddd: %s %s %s %f %f %f"%(v1,v2,v3,d12,d23,d31),"clmethods")
    p1 = vector.vector([0.0,0.0])
    p2 = vector.vector([d12,0.0])
    p3s = cc_int(p1,d31,p2,d23)
    solutions = []
    for p3 in p3s:
        solution = Configuration({v1:p1, v2:p2, v3:p3})
        solutions.append(solution)
    diag_print("solve_ddd solutions"+str(solutions),"clmethods")
    return solutions

def solve_dad(v1,v2,v3,d12,a123,d23):
    """returns a list of Configurations of v1,v2,v3 such that distance v1-v2=d12 etc.
        v<x>: name of point variables
        d<xy>: numeric distance values
        a<xyz>: numeric angle in radians
    """
    diag_print("solve_dad: %s %s %s %f %f %f"%(v1,v2,v3,d12,a123,d23),"clmethods")
    p2 = vector.vector([0.0, 0.0])
    p1 = vector.vector([d12, 0.0])
    p3s = [ vector.vector([d23*math.cos(a123), d23*math.sin(a123)]) ]
    solutions = []
    for p3 in p3s:
        solution = Configuration({v1:p1, v2:p2, v3:p3})
        solutions.append(solution)
    return solutions


# -------------------------------------
# --------- incremental sets ----------
# -------------------------------------

class ConnectedPairs1(incremental.IncrementalSet):
    """Incremental set of all pairs of connected clusters in 1 incremental set"""
    
    def __init__(self, solver, incrset):
        """Creates an incremental set of all pairs of connected clusters in incrset, according to solver"""
        self._solver = solver
        self._incrset = incrset
        incremental.IncrementalSet.__init__(self, [incrset])
        return 

    def _receive_add(self,source, obj):
        connected = set()
        for var in obj.vars:
            dependend = self._solver.find_dependend(var)
            dependend = filter(lambda x: x in self._incrset, dependend)
            connected.update(dependend)
        if obj in connected:
            connected.remove(obj)
        for obj2 in connected:
            self._add(frozenset((obj, obj2)))

    def _receive_remove(self,source, obj):
        for frozen in list(self):
            if obj in frozen:
                self._remove(frozen)

    def __eq__(self, other):
        if isinstance(other, ConnectedPairs1):
            return self._solver == other._solver and self._incrset == other._incrset
        else:
            return False

    def __hash__(self):
        return hash((self._solver, self._incrset))

class ConnectedPairs2(incremental.IncrementalSet):
    """Iincremental set of all pairs of connected clusters in 2 incremental sets."""
 
    def __init__(self, solver, incrset1, incrset2):
        """Creates an incremental set of all pairs (c1, c2) from incrset1 and incrset2 respectively, that are connected according to solver"""
        self._solver = solver
        self._incrset1 = incrset1
        self._incrset2 = incrset2
        incremental.IncrementalSet.__init__(self, [incrset1, incrset2])
        return 

    def _receive_add(self,source, obj):
        connected = set()
        for var in obj.vars:
            dependend = self._solver.find_dependend(var)
            if source == self._incrset1:
                dependend = filter(lambda x: x in self._incrset2, dependend)
            elif source == self._incrset2:
                dependend = filter(lambda x: x in self._incrset1, dependend)
            connected.update(dependend)
        if obj in connected:
            connected.remove(obj)
        for obj2 in connected:
            if source == self._incrset1:
                self._add((obj, obj2))
            elif source == self._incrset2:
                self._add((obj2, obj))

    def _receive_remove(self,source, obj):
        for (c1,c2) in list(self):
            if c1==obj or c2==obj:
                self._remove((c1,c2))

    def __eq__(self, other):
        if isinstance(other, ConnectedPairs2):
            return self._solver == other._solver and self._incrset1 == other._incrset1 and self._incrset2 == other._incrset2
        else:
            return False

    def __hash__(self):
        return hash((self._solver, self._incrset1, self._incrset2))


class Rigids(incremental.Filter):
    
    def __init__(self, solver): 
        self._solver = solver
        incremental.Filter.__init__(self, lambda c: isinstance(c, Rigid), self._solver.top_level())

    def __hash__(self):
        return hash((self.__class__, self._solver))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._solver == other._solver
        else:
            return False

    def __repr__(self):
        return "Rigids("+repr(self._solver)+")"



class Points(incremental.Filter):
    
    def __init__(self, solver): 
        self._solver = solver
        rigids = Rigids(solver)
        incremental.Filter.__init__(self, lambda c: len(c.vars)==1, rigids)

    def __hash__(self):
        return hash((self.__class__, self._solver))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._solver == other._solver
        else:
            return False

    def __repr__(self):
        return "Points("+repr(self._solver)+")"

class Distances(incremental.Filter):
    
    def __init__(self, solver): 
        self._solver = solver
        rigids = Rigids(solver)
        incremental.Filter.__init__(self, lambda c: len(c.vars)==2, rigids)

    def __hash__(self):
        return hash((self.__class__, self._solver))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._solver == other._solver
        else:
            return False

    def __repr__(self):
        return "Distances("+repr(self._solver)+")"

class Triplets(incremental.IncrementalSet):
    
    def __init__(self, solver, incrset):
        """Creates an incremental set of all tripltes of connected clusters in incrset, according to solver"""
        self._solver = solver
        self._incrset = incrset
        incremental.IncrementalSet.__init__(self, [incrset])
        return 

    def _receive_add(self,source, obj):
        connected = set()
        for var in obj.vars:
            dependend = self._solver.find_dependend(var)
            dependend = filter(lambda x: x in self._incrset, dependend)
            dependend = filter(lambda x: len(x.vars.intersection(obj.vars))==1, dependend)
            connected.update(dependend)
        if obj in connected:
            connected.remove(obj)
        obj1 = obj
        if len(connected) >= 2:
            l = list(connected)
            for i in range(len(l)):
                obj2 = l[i]
                shared12 = obj1.vars.intersection(obj2.vars)
                for j in range(i):
                    obj3 = l[j]
                    if len(obj2.vars.intersection(obj3.vars))==1:
                        shared23 = obj2.vars.intersection(obj3.vars)
                        shared13 = obj1.vars.intersection(obj3.vars)
                        shared = shared12.union(shared23).union(shared13)
                        if len(shared)==3: 
                            self._add(frozenset((obj1,obj2,obj3)))

    def _receive_remove(self,source, obj):
        for frozen in list(self):
            if obj in frozen:
                self._remove(frozen)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._solver == other._solver and self._incrset == other._incrset
        else:
            return False

    def __hash__(self):
        return hash((self.__class__, self._solver, self._incrset))

    def __repr__(self):
        return "Triplets("+repr(self._solver)+","+repr(self._incset)+")"

       
