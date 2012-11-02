"""Incremental Cluster Pattern Matching"""

from clsolver import ClusterSolver
from diagnostic import diag_print
from cluster import Rigid, Hedgehog, Balloon
from incremental import IncrementalSet,MutableSet,Filter

class KindFilter(Filter):

    def __init__(self, kind, minpoints, incrset):
        kind2class = {}
        kind2class["rigid"]=Rigid
        kind2class["hog"]=Hedgehog
        kind2class["balloon"]=Balloon
        kind2class["distance"]=Rigid
        kind2class["point"]=Rigid
        kind2maxpoints = {}
        kind2maxpoints["rigid"]=0
        kind2maxpoints["hog"]=0
        kind2maxpoints["balloon"]=0
        kind2maxpoints["distance"]=2
        kind2maxpoints["point"]=1
        self._kind = kind
        self._classobj = kind2class[kind]
        self._maxpoints = kind2maxpoints[kind]
        self._input = incrset
        self._minpoints = minpoints
        IncrementalSet.__init__(self,[incrset])

    def _receive_add(self, source, object):
        if (isinstance(object,self._classobj) and 
            (len(object.vars) <= self._maxpoints or self._maxpoints == 0) and
            len(object.vars) >= self._minpoints):
            self._add(object)  
                
    def _receive_remove(self, source, object):        
        self._remove(object)       
    
    def __eq__(self, other):
        if isinstance(other, KindFilter):
            return (self._input, self._kind, self._minpoints)==(other._input,other._kind, self._minpoints)
        else:
            return False 

    def __hash__(self):
        return hash((self._input, self._kind, self._minpoints))

    def __repr__(self):
        return "KindFilter(%s,%s,%s)"%(str(self._kind),str(self._minpoints),str(self._input))
 

class NConnectedPairs(IncrementalSet):
    """Incremental set of all unordered pairs of N-connected clusters in 1 incremental sets."""
 
    def __init__(self, solver, n, incrset1, incrset2):
        """Creates an incremental set of all pairs frozetset([c1, c2]) from incrset1 and incrset2 respectively, 
            that are connected with N variables, according to solver"""
        # defining variables
        self._solver = solver
        self._incrset1 = incrset1
        self._incrset2 = incrset2
        self._n = n
        # map from objects to sets of pairs
        self._map = {}
        # super init
        IncrementalSet.__init__(self, [incrset1, incrset2])

    def _receive_add(self,source, obj):
        # determine 1-connected objects 
        connected = set()
        for var in obj.vars:
            dependend = self._solver.find_dependend(var)
            # check that connected objects in both sets
            if source == self._incrset1:
                dependend = filter(lambda x: x in self._incrset2, dependend)
            elif source == self._incrset2:
                dependend = filter(lambda x: x in self._incrset1, dependend)
            connected.update(dependend)
        # dont pair (obj,obj)
        if obj in connected:
            connected.remove(obj)
        # for each connected object, check that #shared vars == n
        for obj2 in connected:
            shared = obj.vars.intersection(obj2.vars)
            if len(shared) == self._n:
                # add new pair
                pair = frozenset([obj, obj2])
                self._add(pair)
                # add to mapping 
                if obj not in self._map: 
                    self._map[obj] = set()
                if obj2 not in self._map: 
                    self._map[obj2] = set()
                self._map[obj].add(pair)
                self._map[obj2].add(pair)

    def _receive_remove(self,source, obj):
        # remove all pairs that contain obj
        for pair in self._map[obj]:
            (obj1,obj2) = pair
            self._remove(pair)
            # remove pair from mapping
            self._map[obj1].remove(par)
            self._map[obj2].remove(pair)
            # clean up mapping 
            if len(self._map[obj1]) == 0: 
                del self._map[obj1]
            if len(self._map[obj2]) == 0: 
                del self._map[obj2]
 
    def __eq__(self, other):
        if isinstance(other, NConnectedPairs):
            return (self._solver == other._solver and 
                    self._incrset1 == other._incrset1 and 
                    self._incrset2 == other._incrset2 and 
                    self._n == other._n)
        else:
            return False

    def __hash__(self):
        return hash((self._solver, self._incrset1, self._incrset2, self._n))


class PatternMatches(IncrementalSet):
    """Incrementally matches patterns of clusters"""
    def __init__(self, pattern, solver):
        self._solver = solver
        # convert pattern to a set of tuples
        listoftuples = []
        for clusterpattern in pattern:
            (kind, clustername, pointnames) = clusterpattern
            listoftuples.append(tuple([kind, clustername, tuple(pointnames)]))
        setoftuples = frozenset(listoftuples)
        self._pattern = setoftuples
        # create sub-sets for correct type of input clusters
        self._subs = []
        # NOTE: we cannot use source like this to link it to a pattern, because sources may be equal!
        self._source2pattern = {}
        for clusterpattern in self._pattern:
            (kind, clustername, pointnames) = clusterpattern
            sub = KindFilter(kind, len(pointnames),self._solver.top_level())
            self._subs.append(sub)
            # NOTE: we cannot use source like this to link it to a pattern, because sources may be equal!
            self._source2pattern[sub]=[clusterpattern]
            print "creating",sub,"for",self._source2pattern[sub]
        #rof
        # create sub-sets for all pairs of clusters
        listoftuples = list(setoftuples)
        l = len(listoftuples) 
        for i in range(l):
            for j in range(i+1,l):
                cp1 = listoftuples[i]
                cp2 = listoftuples[j]
                (kind1, clustername1, pointnames1) = cp1
                (kind2, clustername2, pointnames2) = cp2
                shared = set(pointnames1).intersection(set(pointnames2))
                n = len(shared)
                if n > 0:
                    kindfilter1 = KindFilter(kind1, len(pointnames1),self._solver.top_level())
                    kindfilter2 = KindFilter(kind2, len(pointnames2),self._solver.top_level())
                    sub = NConnectedPairs(solver, n, kindfilter1,kindfilter2)
                    self._subs.append(sub)
                    # NOTE: we cannot use source like this to link it to a pattern, because sources may be equal!
                    self._source2pattern[sub]=[cp1,cp2]
                    print "creating",sub,"for",self._source2pattern[sub]

        IncrementalSet.__init__(self, self._subs)
            
    def _receive_add(self, source, object):
        # NOTE: we cannot use source like this to link it to a pattern, because sources may be equal!
        print "receive",object
        pattern = self._source2pattern[source]
        print "matching sub-pattern", pattern
        #raise NotImplementedError
                
    def _receive_remove(self, source, object):        
        raise NotImplementedError
 
    def __eq__(self, other):
        if isinstance(other, PatternMatches):
            return (self._solver, self._pattern)==(other._solver,other._pattern)
        else:
            return False 

    def __hash__(self):
        return hash((self._solver, self._pattern))

    def __repr__(self):
        return "PatternMatches(%s,%s)"%(str(self._pattern),str(self._solver))


def test_icpm():
    solver = ClusterSolver([])
    solver.add(Rigid(["p5"]))
    solver.add(Rigid(["p1","p2"]))
    solver.add(Rigid(["p2","p3"]))
    solver.add(Rigid(["p1","p3","p4","p5"]))
    pattern = [["rigid","$d_ab",["$a", "$b"]], 
            ["rigid", "$d_ac",["$a", "$c"]], 
            ["rigid", "$d_bc",["$b","$c"]]]
    matches = PatternMatches(pattern, solver)
    print list(matches)

if __name__ == "__main__":
    test_icpm()
