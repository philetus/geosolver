"""A generic 3D geometric constraint solver"""

from clsolver import *
from sets import Set
from diagnostic import diag_print, diag_select
from selconstr import *
from intersections import *
from configuration import Configuration
from cluster import *
from map import Map
from gmatch import gmatch
from method import OrMethod

def pattern2graph(pattern):
    """convert pattern to pattern graph"""
    pgraph = Graph()
    pgraph.add_vertex("point")
    pgraph.add_vertex("distance")
    pgraph.add_vertex("rigid")
    pgraph.add_vertex("balloon")
    pgraph.add_vertex("hedgehog")
    for clpattern in pattern:
        (pattype, patname, patvars) = clpattern
        pgraph.add_edge(pattype, patname)
        for var in patvars:
            pgraph.add_edge(patname, var)
        if pattype == "hedgehog":
            pgraph.add_edge("cvar"+"#"+patname, patvars[0])
            pgraph.add_edge(patname, "cvar"+"#"+patname)
    #diag_print("pattern graph:"+str(pgraph),"match");
    return pgraph

def reference2graph(nlet):
    """convert nlet to reference graph"""
    rgraph = Graph()
    rgraph.add_vertex("point")
    rgraph.add_vertex("distance")
    rgraph.add_vertex("rigid")
    rgraph.add_vertex("balloon")
    rgraph.add_vertex("hedgehog")
    for cluster in nlet:
        for var in cluster.vars:
            rgraph.add_edge(cluster, var)
        if isinstance(cluster, Rigid):
            rgraph.add_edge("rigid", cluster)
            if len(cluster.vars) == 1:
                rgraph.add_edge("point", cluster)
            elif len(cluster.vars) == 2:
                rgraph.add_edge("distance", cluster)
        if isinstance(cluster, Balloon):
            rgraph.add_edge("balloon", cluster)
        if isinstance(cluster, Hedgehog):
            rgraph.add_edge("hedgehog", cluster)
            rgraph.add_edge("cvar"+"#"+str(id(cluster)), cluster.cvar)
            rgraph.add_edge(cluster, "cvar"+"#"+str(id(cluster)))
    #diag_print("reference graph:"+str(rgraph),"match");
    return rgraph

def rootname(cluster):
    return "root#"+str(id(cluster))


class ClusterSolver3D(ClusterSolver):
    """A generic 3D geometric constraint solver. 
    
    Finds a generic solution for problems formulated by cluster-constraints.

    Constraints are Clusers: Rigids, Hedgehogs and Balloons. 
    Cluster are added and removed using the add and remove methods. 
    After adding each Cluster, the solver tries to merge it with
    other clusters, resulting in new Clusters and Methods.

    The generic solution is a directed acyclic graph of Clusters and Methods. 
    Particilar problems and solutions are represented by a Configuration 
    for each cluster. 

    For each Cluster a set of Configurations can be set using the
    set method. Configurations are propagated via Methods and can
    be retrieved with the get method (also returning a set). 
    """

    # ------- PUBLIC METHODS --------

    def __init__(self):
        """Instantiate a ClusterSolver3D"""
        ClusterSolver.__init__(self, dimension=3)
        self.rootcluster = None

    # overriding ClusterSolver.set_root
    def set_root(self, cluster):
        diag_print("set root "+str(self.rootcluster), "clsolver3D")
        if self.rootcluster != None:
            oldrootvar = rootname(self.rootcluster)
            self._mg.set(oldrootvar, False)
        newrootvar = rootname(cluster)
        self._mg.set(newrootvar, True)
        self.rootcluster = cluster


    # ------------ INTERNALLY USED METHODS --------

    def _all_sources_constraint_in_cluster(self, constraint, cluster):
        if not self._contains_constraint(cluster, constraint):
            return Set()
        elif self._is_atomic(cluster):
            return Set([cluster])
        else:
            method = self._determining_method(cluster)
            sources = Set()
            for inp in method.input_clusters():
                sources.union_update(self._all_sources_constraint_in_cluster(constraint, inp))
            return sources
     
    # --------------
    # search methods
    # --------------
    
    def _search(self, newcluster):
        diag_print("search from: "+str(newcluster),"clsolver3D")
        # find all toplevel clusters connected to newcluster via one or more variables
        connected = Set()
        for var in newcluster.vars:
            dependend = self.find_dependend(var)
            dependend = filter(lambda x: self.is_top_level(x), dependend)
            connected.union_update(dependend)
        diag_print("search: connected clusters="+str(connected),"clsolver3D")
        # try applying methods
        if self._try_method(connected):
            return True 
        return False

    def _try_method(self, nlet):
        """finds a possible rewrite rule applications on given set of clusters, applies it 
           and returns True iff successfull
        """
        refgraph = reference2graph(nlet)
        for methodclass in [MergePR, MergeDR, MergeRR, MergeSR, DeriveTTD, DeriveDDD, DeriveADD, DeriveDAD, DeriveAA]:
            matches = gmatch(methodclass.patterngraph, refgraph)
            if len(matches) > 0:
                diag_print("number of matches = "+str(len(matches)), "clsolver3D")
            for s in matches:
                # diag_print("try match: "+str(s),"clsolver3D")
                method = apply(methodclass, [s])
                succes = self._add_method_complete(method)
                if succes:
                   #raw_input()
                   #print "press key"
                   return True
            # end for match
        # end for method
        return False
    
    def _add_method_complete(self, merge):
        # diag_print("add_method_complete "+str(merge), "clsolver3D")
        # check that method has one output
        if len(merge.outputs()) != 1:
            raise StandardError, "merge number of outputs != 1"
        output = merge.outputs()[0]
        
        # check that the method is information increasing (infinc)
        infinc = True
        connected = Set()
        for var in output.vars:
            dependend = self.find_dependend(var)
            dependend = filter(lambda x: self.is_top_level(x), dependend)
            connected.union_update(dependend)
        #for cluster in merge.input_clusters():
        #    if cluster in connected:
        #        connected.remove(cluster)

        # NOTE 07-11-2007 (while writing the paper): this  implementation of information increasing may not be correct. We may need to check that the total sum of the information in the overlapping clusters is equal to the information in the output.

        for cluster in connected:
            if num_constraints(cluster.intersection(output)) >= num_constraints(output):
                infinc = False
                break
        diag_print("information increasing:"+str(infinc),"clsolver3D")

        # check if method reduces number of clusters (reduc)
        nremove = 0
        for cluster in merge.input_clusters():
            if num_constraints(cluster.intersection(output)) >= num_constraints(cluster): 
               # will be removed from toplevel
               nremove += 1
        reduc = (nremove > 1)
        diag_print("reduce # clusters:"+str(reduc),"clsolver3D")
        
        # check if the method is redundant
        if not infinc and not reduc:
            diag_print("method is redundant","clsolver3D")
            return False

        # check consistency and local/global overconstrained
        consistent = True
        local_oc = False
        for i1 in range(0, len(merge.input_clusters())):
            for i2 in range(i1+1, len(merge.input_clusters())):
                c1 = merge.input_clusters()[i1] 
                c2 = merge.input_clusters()[i2] 
                if num_constraints(c1.intersection(c2)) != 0:
                    local_oc = True
                consistent = consistent and self._is_consistent_pair(c1, c2)
        merge.consistent = consistent
        merge.overconstrained = local_oc
        # global overconstrained? (store in output cluster)
        overconstrained = not consistent
        for cluster in merge.input_clusters():
            overconstrained = overconstrained or cluster.overconstrained
        output.overconstrained = overconstrained
        # add to graph
        self._add_cluster(output)
        self._add_method(merge)
        # remove input clusters from top_level
        if not (hasattr(merge,"noremove") and merge.noremove == True):
            merge.restore_toplevel = []    # make restore list in method
            for cluster in merge.input_clusters():
                if num_constraints(cluster.intersection(output)) >= num_constraints(cluster): 
                    diag_print("remove from top-level: "+str(cluster),"clsolver3D")
                    self._rem_top_level(cluster) 
                    merge.restore_toplevel.append(cluster)
                else:
                    diag_print("keep top-level: "+str(cluster),"clsolver3D")
        # endif
        # add prototype selection method
        self._add_prototype_selector(merge)
        # add solution selection method
        self._add_solution_selector(merge)
        # add method to determine root-variable
        self._add_root_method(merge.input_clusters(),merge.outputs()[0])
        # pause
        return True

    def _add_root_method(self,inclusters,outcluster):
        inroots = []
        for cluster in inclusters:
            inroots.append(rootname(cluster))
        outroot = rootname(outcluster)
        method = OrMethod(inroots, outroot)
        # add method
        self._add_method(method)
        # make sure its deleted when cluster is deleted
        self._add_dependency(outcluster, method) 

    # overriding superclass function
    def _add_cluster(self, cluster):
        # call superclass function
        ClusterSolver._add_cluster(self, cluster)
        # add root-variable if needed with default value False
        root = rootname(cluster)
        if not self._mg.contains(root):
            self._mg.add_variable(root, False)
            self._mg.set(root, False)
            # add root-variable to dependency graph
            self._add_dependency(cluster, root)

# class ClusterSolver3D

# ----------------------------------------------
# ---------- Methods for 3D solving -------------
# ----------------------------------------------

# Merge<X> methods take root-cluster in considerations   
# Derive<X> methods do not take root cluster in consideration

class MergePR(ClusterMethod):
    """Represents a merging of a one-point cluster with any other rigid."""
    def __init__(self, map):
        # check inputs
        in1 = map["$p"]
        in2 = map["$r"]
        # create ouput
        outvars = Set(in1.vars).union(in2.vars)
        out = Rigid(outvars)
        # set method properties
        in1root = rootname(in1)
        in2root = rootname(in2)
        self._inputs = [in1, in2, in1root, in2root]
        self._outputs = [out]
        ClusterMethod.__init__(self)

    def _pattern():
        pattern = [["point","$p",["$a"]], ["rigid", "$r", ["$a"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

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
        else: # cheapest
            res = conf2.merge(conf1)
        return [res]

class MergeDR(ClusterMethod):
    """Represents a merging of a distance (two-point cluster) with a rigid."""
    def __init__(self, map):
        # check inputs
        in1 = map["$d"]
        in2 = map["$r"]
        # create ouput
        outvars = Set(in1.vars).union(in2.vars)
        out = Rigid(outvars)
        # set method properties
        in1root = rootname(in1)
        in2root = rootname(in2)
        self._inputs = [in1, in2, in1root, in2root]
        self._outputs = [out]
        ClusterMethod.__init__(self)

    def _pattern():
        pattern = [["distance","$d",["$a","$b"]], ["rigid", "$r",["$a", "$b"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

    def __str__(self):
        s =  "MergeDR("+str(self._inputs[0])+"+"+str(self._inputs[1])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("MergeDR.multi_execute called","clmethods")
        c1 = self._inputs[0]
        c2 = self._inputs[1]
        conf1 = inmap[c1]
        conf2 = inmap[c2]
        isroot1 = inmap[self._inputs[2]]
        isroot2 = inmap[self._inputs[3]]
        if isroot1:
            res = conf1.merge(conf2)
        elif isroot2:
            res = conf2.merge(conf1)
        else: # cheapest
            res = conf2.merge(conf1)
        return [res]
   
class MergeRR(ClusterMethod):
    """Represents a merging of two rigids sharing three points."""
    def __init__(self, map):
        # check inputs
        in1 = map["$r1"]
        in2 = map["$r2"]
        # create output
        out = Rigid(Set(in1.vars).union(in2.vars))
        # set method parameters
        in1root = rootname(in1)
        in2root = rootname(in2)
        self._inputs = [in1, in2, in1root, in2root]
        self._outputs = [out]
        ClusterMethod.__init__(self)

    def _pattern():
        pattern = [["rigid","$r1",["$a","$b","$c"]], ["rigid", "$r2", ["$a", "$b", "$c"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

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
        elif len(c1.vars) < len(c2.vars):  # cheapest
            res = conf2.merge(conf1)
        else:
            res = conf1.merge(conf2)
        return [res]

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
        # set method parameters
        self._inputs = [self.d_ab, self.d_ac, self.d_bc]
        self._outputs = [out]
        ClusterMethod.__init__(self)
        # do not remove input clusters (because root not considered here)
        self.noremove = True

    def _pattern():
        pattern = [["rigid","$d_ab",["$a", "$b"]], 
            ["rigid", "$d_ac",["$a", "$c"]], 
            ["rigid", "$d_bc",["$b","$c"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()


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
        solutions = solve_ddd_3D(v1,v2,v3,d12,d23,d31)
        return solutions

class DeriveTTD(ClusterMethod):
    """Represents a derive of a tetra from six distances"""
    def __init__(self, map):
        # check inputs
        self.t_abc = map["$t_abc"]
        self.t_abd = map["$t_abd"]
        self.d_cd = map["$d_cd"]
        self.a = map["$a"]
        self.b = map["$b"]
        self.c = map["$c"]
        self.d = map["$d"]
        # create output
        out = Rigid([self.a,self.b,self.c,self.d])
        # set method parameters
        self._inputs = [self.t_abc, self.t_abd, self.d_cd]
        self._outputs = [out]
        ClusterMethod.__init__(self)
        # do not remove input clusters (because root not considered here)
        self.noremove = True

    def __str__(self):
        s =  "DeriveTTD("+str(self._inputs[0])+\
                        str(self._inputs[1])+\
                        str(self._inputs[2])+\
                        ", ... -> "+\
                        str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def _pattern():
        pattern  = [["rigid","$t_abc",["$a", "$b", "$c"]]]
        pattern += [["rigid","$t_abd",["$a", "$b", "$d"]]]
        pattern += [["rigid","$d_cd",["$c", "$d"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

    def multi_execute(self, inmap):
        diag_print("DeriveTTD.multi_execute called","clmethods")
        c123 = inmap[self.t_abc]
        c124 = inmap[self.t_abd]
        c34 = inmap[self.d_cd]
        v1 = self.a
        v2 = self.b
        v3 = self.c
        v4 = self.d
        p1 = c123.get(v1)
        p2 = c123.get(v2)
        p3 = c123.get(v3)
        d14 = distance_2p(c124.get(v1),c124.get(v4))
        d24 = distance_2p(c124.get(v2),c124.get(v4))
        d34 = distance_2p(c34.get(v3),c34.get(v4))
        return solve_3p3d(v1,v2,v3,v4,p1,p2,p3,d14,d24,d34)

    def prototype_constraints(self):
        constraints = []
        constraints.append(FunctionConstraint(fnot(is_left_handed),[self.a,self.b,self.c,self.d]))
        constraints.append(FunctionConstraint(fnot(is_right_handed),[self.a,self.b,self.c,self.d]))
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

    def _pattern():
        pattern = [["rigid","$d_ab",["$a", "$b"]], 
            ["hedgehog", "$a_abc",["$b", "$a", "$c"]], 
            ["rigid", "$d_bc",["$b","$c"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

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
        solutions = solve_dad_3D(v1,v2,v3,d12,a123,d23)
        return solutions

class DeriveADD(ClusterMethod):
    """Represents a merging of one distance and to distances"""
    def __init__(self, map):
        # check inputs
        self.a_cab = map["$a_cab"]
        self.d_ab = map["$d_ab"]
        self.d_bc = map["$d_bc"]
        self.a = map["$a"]
        self.b = map["$b"]
        self.c = map["$c"]
        # create output
        out = Rigid([self.a,self.b,self.c])
        # set method parameters
        self._inputs = [self.a_cab, self.d_ab, self.d_bc]
        self._outputs = [out]
        ClusterMethod.__init__(self)
        # do not remove input clusters (because root not considered here)
        self.noremove = True


    def _pattern():
        pattern = [["hedgehog","$a_cab",["$a", "$c", "$b"]], 
            ["rigid", "$d_ab",["$a", "$b"]], 
            ["rigid", "$d_bc",["$b","$c"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

    def __str__(self):
        s =  "DeriveADD("+str(self._inputs[0])+"+"+str(self._inputs[1])+"+"+str(self._inputs[2])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("DeriveADD.multi_execute called","clmethods")
        c312 = inmap[self.a_cab]
        c12 = inmap[self.d_ab]
        c23 = inmap[self.d_bc]
        v1 = self.a
        v2 = self.b
        v3 = self.c
        a312 = angle_3p(c312.get(v3),c312.get(v1),c312.get(v2))
        d12 = distance_2p(c12.get(v1),c12.get(v2))
        d23 = distance_2p(c23.get(v2),c23.get(v3))
        solutions = solve_add_3D(v1,v2,v3,a312,d12,d23)
        return solutions

class DeriveAA(ClusterMethod):
    """Derive a scalable from two angles"""
    def __init__(self, map):
        # check inputs
        self.a_cab = map["$a_cab"]
        self.a_abc = map["$a_abc"]
        self.a = map["$a"]
        self.b = map["$b"]
        self.c = map["$c"]
        # create output
        out = Balloon([self.a,self.b,self.c])
        # set method parameters
        self._inputs = [self.a_cab, self.a_abc]
        self._outputs = [out]
        ClusterMethod.__init__(self)
        # do not remove input clusters (because root not considered here)
        self.noremove = True



    def _pattern():
        pattern = [["hedgehog","$a_cab",["$a", "$c", "$b"]], 
            ["hedgehog", "$a_abc",["$b", "$a","$c"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

    def __str__(self):
        s =  "DeriveAA("+str(self._inputs[0])+"+"+str(self._inputs[1])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("DeriveAA.multi_execute called","clmethods")
        c312 = inmap[self.a_cab]
        c123 = inmap[self.a_abc]
        v1 = self.a
        v2 = self.b
        v3 = self.c
        a312 = angle_3p(c312.get(v3),c312.get(v1),c312.get(v2))
        d12 = 1.0
        a123 = angle_3p(c123.get(v1),c123.get(v2),c123.get(v3))
        solutions = solve_ada_3D(v1,v2,v3,a312,d12,a123)
        return solutions

class MergeSR(ClusterMethod):
    """Merge a Rigid from a Scalabe and a Rigid sharing two points"""
    def __init__(self, map):
        # check inputs
        in1 = map["$r"]
        in2 = map["$s"]
        # create output
        out = Rigid(Set(in2.vars))
        # set method parameters
        self._inputs = [in1, in2]
        self._outputs = [out]
        ClusterMethod.__init__(self)

    def _pattern():
        pattern = [["rigid","$r",["$a","$b"]], ["balloon", "$s", ["$a", "$b"]]]
        return pattern2graph(pattern)
    pattern = staticmethod(_pattern)
    patterngraph = _pattern()

    def __str__(self):
        s =  "MergeSR("+str(self._inputs[0])+"+"+str(self._inputs[1])+"->"+str(self._outputs[0])+")"
        s += "[" + self.status_str()+"]"
        return s

    def multi_execute(self, inmap):
        diag_print("MergeSR.multi_execute called","clmethods")
        c1 = self._inputs[0]
        c2 = self._inputs[1]
        conf1 = inmap[c1]
        conf2 = inmap[c2]
        return [conf1.merge_scale(conf2)]

# ---------------------------------------------------------
# ------- functions to determine configurations  ----------
# ---------------------------------------------------------

def solve_ddd_3D(v1,v2,v3,d12,d23,d31):
    """returns a list of Configurations of v1,v2,v3 such that distance v1-v2=d12 etc.
        v<x>: name of point variables
        d<xy>: numeric distance values
        a<xyz>: numeric angle in radians
    """
    diag_print("solve_ddd: %s %s %s %f %f %f"%(v1,v2,v3,d12,d23,d31),"clmethods")
    # solve in 2D
    p1 = vector.vector([0.0,0.0])
    p2 = vector.vector([d12,0.0])
    p3s = cc_int(p1,d31,p2,d23)
    solutions = []
    # extend coords to 3D!
    p1.append(0.0)
    p2.append(0.0)
    for p3 in p3s:
        p3.append(0.0)
        solution = Configuration({v1:p1, v2:p2, v3:p3})
        solutions.append(solution)
    # return only one solution (if any)
    if len(solutions) > 0:
        solutions = [solutions[0]]
    diag_print("solve_ddd solutions"+str(solutions),"clmethods")
    return solutions

def solve_dad_3D(v1,v2,v3,d12,a123,d23):
    """returns a list of Configurations of v1,v2,v3 such that distance v1-v2=d12 etc.
        v<x>: name of point variables
        d<xy>: numeric distance values
        a<xyz>: numeric angle in radians
    """
    diag_print("solve_dad: %s %s %s %f %f %f"%(v1,v2,v3,d12,a123,d23),"clmethods")
    p2 = vector.vector([0.0, 0.0])
    p1 = vector.vector([d12, 0.0])
    p3s = [ vector.vector([d23*math.cos(a123), d23*math.sin(a123)]) ]
    # extend coords to 3D!
    p1.append(0.0)
    p2.append(0.0)
    solutions = []
    for p3 in p3s:
        p3.append(0.0)
        solution = Configuration({v1:p1, v2:p2, v3:p3})
        solutions.append(solution)
    return solutions

def solve_add_3D(a,b,c, a_cab, d_ab, d_bc):
    """returns a list of Configurations of v1,v2,v3 such that distance v1-v2=d12 etc.
        v<x>: name of point variables
        d<xy>: numeric distance values
        a<xyz>: numeric angle in radians
    """

    diag_print("solve_dad: %s %s %s %f %f %f"%(a,b,c,a_cab,d_ab,d_bc),"clmethods")
    p_a = vector.vector([0.0,0.0])
    p_b = vector.vector([d_ab,0.0])
    dir = vector.vector([math.cos(-a_cab),math.sin(-a_cab)])
    solutions = cr_int(p_b, d_bc, p_a, dir)
    rval = []
    p_a.append(0.0)
    p_b.append(0.0)
    for p_c in solutions:
        p_c.append(0.0)
        map = {a:p_a, b:p_b, c:p_c}
        rval.append(Configuration(map))
    return rval

def solve_ada_3D(a, b, c, a_cab, d_ab, a_abc):
    """returns a list of Configurations of v1,v2,v3 such that distance v1-v2=d12 etc.
        v<x>: name of point variables
        d<xy>: numeric distance values
        a<xyz>: numeric angle in radians
    """
    diag_print("solve_ada: %s %s %s %f %f %f"%(a,b,c,a_cab,d_ab,a_abc),"clmethods")
    p_a = vector.vector([0.0,0.0])
    p_b = vector.vector([d_ab, 0.0])
    dir_ac = vector.vector([math.cos(-a_cab),math.sin(-a_cab)])
    dir_bc = vector.vector([math.cos(math.pi-a_abc),math.sin(math.pi-a_abc)])
    dir_ac[1] = math.fabs(dir_ac[1]) 
    dir_bc[1] = math.fabs(dir_bc[1]) 
    if tol_eq(math.sin(a_cab), 0.0) and tol_eq(math.sin(a_abc),0.0):
                m = d_ab/2 + math.cos(-a_cab)*d_ab - math.cos(-a_abc)*d_ab
                p_c = vector.vector([m,0.0]) 
                # p_c = (p_a + p_b) / 2
                p_a.append(0.0)
                p_b.append(0.0)        
                p_c.append(0.0)
                map = {a:p_a, b:p_b, c:p_c}
                cluster = _Configuration(map)
                cluster.underconstrained = True
                rval = [cluster]
    else:
                solutions = rr_int(p_a,dir_ac,p_b,dir_bc)
                p_a.append(0.0)
                p_b.append(0.0)
                rval = []
                for p_c in solutions:
                        p_c.append(0.0)
                        map = {a:p_a, b:p_b, c:p_c}
                        rval.append(Configuration(map))
    return rval

def solve_3p3d(v1,v2,v3,v4,p1,p2,p3,d14,d24,d34):
    """returns a list of Configurations of v1,v2,v3 such that distance v1-v2=d12 etc.
        v<x>: name of point variable
        p<x>: numeric point position (vector)
        d<xy>: numeric distance value
        a<xyz>: numeric angle in radians
    """
    diag_print("solve_3p3d: %s %s %s %s "%(v1,v2,v3,v4),"clmethods")
    diag_print("p1="+str(p1),"clsolver3D")
    diag_print("p2="+str(p2),"clsolver3D")
    diag_print("p3="+str(p3),"clsolver3D")
    diag_print("d14="+str(d14),"clsolver3D")
    diag_print("d24="+str(d24),"clsolver3D")
    diag_print("d34="+str(d34),"clsolver3D")
    p4s = sss_int(p1,d14,p2,d24,p3,d34)
    solutions = []
    for p4 in p4s:
        solution = Configuration({v1:p1, v2:p2, v3:p3, v4:p4})
        solutions.append(solution)
    return solutions


