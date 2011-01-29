"""This module provides various incrementally updated set-like containers.""" 

import notify
import weakref

class IncrementalSet(notify.Notifier, notify.Listener):
    """This is the base class for various incrementally updated set-like containers. 
       The represented set can change when it is notified of changes in other IncementalSets,
       and it can notify other IncrementalSets when objects are added or removed.
       Its contents can be iterated using 'iter', and it supports the 'in' and 'len queries.
       
       All objects in the set are unique, and objects must implement __hash__ and __eq__.
       
       Note that this class does not provide public methods for adding and removing objects.
       See MutableSet for a user-modifiable subclass.

       Subclasses should implement the _receive_add and _receive_remove methods, which are
       called when an incset is notified by another incset. If your subclass uses the
       Listerner/Notifier scheme for notification from other objects, your receive_notify
       function should call IncrementalSet.receive_notify. 

       IncrementalSets are unqiue. Multiple instances of equivalent incsets refer to the 
       first of its kind. So update operations are executed only once, even if multiple 
       instances of equivalent incset exist. IncrementalSets must also define the __eq__ and
       __hash__ methods. 
    """ 

    # keep track of all IncrementalSets, so we can re-use identical IncrementalSets
    # _all[x] maps to a tuple (wr, cnt) 
    # where wr is a weak refererence to the original, first instantiated nest equal to x
    # and cnt is the total number of instantiations (past and present) of x (never decreases)
    _all = weakref.WeakKeyDictionary()

    def __init__(self, inputs=[]):
        """Instantiate a new incset, that listens for changes from given incsets. 
           If an equivalent incset allready exists, this object stores only a
           reference, and all IncrementalSet methods will use this reference.
        """
        if self in self._all:
            # set self._ref and update self._all
            (self._ref, count) = self._all[self]
            count += 1
            self._all[self] = (self._ref, count)

            self.listeners = self._ref().listeners
            self.notifiers = self._ref().notifiers
        else:
            # set self._ref and update self._all
            self._ref = None
            count = 1
            self._all[self] = (weakref.ref(self), count)
       
            # initialise instance variables
            self._objects = set()
            self._inputs = set(inputs)
            notify.Notifier.__init__(self)
            notify.Listener.__init__(self)
             # add incsets
            for incset in self._inputs:
                self._add_input(incset)
            # update from initial state of all incsets 
            for incset in self._inputs:
                for obj in incset:
                    self._receive_add(incset, obj)
                   
    def _add_input(self, incset):
        """Add an incset, listen for notifications from it"""
        if self._ref:
            # add object to ref if given
            self._ref()._add_input(incset)
        else:
            self.add_notifier(incset)

    def receive_notify(self, source, message):
        if source in self.notifiers:
            (action, object) = message
            if action == "add":
                self._receive_add(source, object)        
            elif action == "remove":
                self._receive_remove(source, object)        
            else:
                print "Warning:",self,"reveiced unknown message"
        else:
            print "Warning:", self, "reveiced notification from unknown source"
 
    def _receive_add(self,source, object):
        raise Exception("This method is abstract. Subclasses should implement it")

    def _receive_remove(self,source, object):
        raise Exception("This method is abstract. Subclasses should implement it")

    def _add(self, object):
        """Add an object and send notification to listeners"""
        if self._ref:
            # add object to ref if given
            self._ref()._add(object)
        else:
            # else add object to self
            if object not in self._objects:
                self._objects.add(object)
                self.send_notify(("add", object))

    def _remove(self, object):
        """Remove an object and send notification to listeners"""
        if self._ref:
            # remove object from ref, if given
            self._ref()._remove(object)
        else:
            # else add object to self
            if object not in self._objects:
                self._objects.add(object)
                self.send_notify(("add", object))
        if object in self._objects:
            self._objects.remove(object)
            self.send_notify(("remove", object))

    def __iter__(self):
        """Returns an iterator for the objects contained here. 
           Note that the iterator will become invalid when objects are added or removed, which
           may be a side-effect of changing other IncrementalSets. 
        """
        if self._ref:
            # remove object from ref, if given
            return iter(self._ref())
        else:
            return iter(self._objects)

    def __contains__(self, obj):
        if self._ref:
            # remove object from ref, if given
            return obj in self._ref()
        else:
            return obj in self._objects

    def __len__(self):
        if self._ref:
            # remove object from ref, if given
            return len(self._ref())
        else:
            return len(self._objects)


class MutableSet(IncrementalSet):
    """A set-like container that can notify other objects of changes, when objects are added or removed"""  

    def __init__(self, seq=[]):
        IncrementalSet.__init__(self)
        for obj in seq:
            self._add(obj)
     
    def add(self, object):
        self._add(object)

    def remove(self, object):
        self._remove(object)

    def __repr__(self):
        return "MutableSet#%s"%str(id(self))

class Union(IncrementalSet):
    def __init__(self, *args):
        IncrementalSet.__init__(self, args)

    def _receive_add(self, source, obj):
        self._add(obj)

    def _receive_remove(self, source, obj):
        count = 0
        for incset in self._inputs:
            if obj in incset:
                count += 1
        if count == 0:
            self._remove(obj)

class Intersection(IncrementalSet):
    def __init__(self, *args):
        IncrementalSet.__init__(self, args)

    def _receive_add(self, source, obj):
        for incset in self._inputs:
            if obj not in incset:
                return
        self._add(obj)

    def _receive_remove(self, source, obj):
        self._remove(obj)


class Difference(IncrementalSet):
    def __init__(self, pos, neg):
        self._pos = pos
        self._neg = neg
        IncrementalSet.__init__(self, [pos, neg])

    def _receive_add(self, source, obj):
        if source == self._pos and obj not in self._neg:
            self._add(obj)
        elif source == self._neg:  # and obj in self:
            self._remove(obj)

    def _receive_remove(self, source, obj):
        if source == self._pos:
            self._remove(obj)
        elif source == self._neg and obj in self._pos:
            self._add(obj)

class Filter(IncrementalSet):
    """A set-like container that incrementally filters its input (MutableSet or other IncrementalSet)"""

    def __init__(self, testfunction, incrset):
        self._incrset = incrset
        self._testfunction = testfunction
        IncrementalSet.__init__(self,[incrset])

    def _receive_add(self, source, object):
        if self._testfunction(object):
            self._add(object)        
                
    def _receive_remove(self, source, object):        
        if self._testfunction(object):
            self._remove(object)        
    
    def __eq__(self, other):
        if isinstance(other, Filter):
            return (self._incrset, self._testfunction)==(other._incrset,other._testfunction)
        else:
            return False 

    def __hash__(self):
        return hash((self._incrset, self._testfunction))

    def __repr__(self):
        return "Filter(%s,%s)"%(str(self._incrset),str(self._testfunction))


class Map(IncrementalSet):
    """A set-like container that incrementally maps its input through a function. 
       Note that the mapping function must always return the same output for the same input."""

    def __init__(self, mapfunction, incrset):
        self._incrset = incrset
        self._mapfunction = mapfunction
        IncrementalSet.__init__(self, [incrset])

    def _receive_add(self, source, object):
        self._add(self._mapfunction(object))        

    def _receive_remove(self, source, object):
        self._remove(self._mapfunction(object))        

    def __eq__(self, other):
        if isinstance(other, Map):
            return (self._incrset, self._mapfunction)==(other._incrset,other._mapfunction)
        else:
            return False 

    def __hash__(self):
        return hash((self._incrset, self._mapfunction))

    def __repr__(self):
        return "Map(%s,%s)"%(str(self._incrset),str(self._mapfunction))


class Permutations(IncrementalSet):
    """A set-like container that incrementally determines all permutations of its inputs (IncrementalSets)"""

    def __init__(self, partmatchers):
        self._partmatchers = list(partmatchers)
        IncrementalSet.__init__(self, partmatchers)

    def _receive_add(self, source, obj):
        index = self._partmatchers.index(source)
        if index == -1:
            raise Exception("Unknown source")
        parts = []
        for i in range(len(self._partmatchers)):
            if i == index:
                parts.append([obj])
            else:
                parts.append(iter(self._partmatchers[i]))
        newmatches = permutations(parts)
        for match in newmatches:
            self._add(match)

    def _receive_remove(self, source, obj):
        index = self._partmatchers.index(source)
        if index == -1:
            raise Exception("Unknown source")
        toremove = []
        for match in iter(self):
            if match[index] == obj:
                toremove.append(match)
        for match in toremove:
            self._remove(match)

    def __eq__(self, other):
        if isinstance(other, Permutations):
            return self._partmatchers == other.partmathers
        else:
            return False 

    def __hash__(self):
        return hash(tuple(self._partmatchers))

    def __repr__(self):
        return "Permutations(%s)"%str(self._partmatchers)

def permutations(listofiters):
    """All permuations of the objects in each iter, returned as a list of tuples"""
    if len(listofiters)==0:
        return []
    elif len(listofiters)==1:
        return map(lambda element: tuple([element]), listofiters[0])
    else:
        l = list(listofiters[0])
        p = permutations(listofiters[1:])
        z = []
        for e in l:
            for y in p:
                z.append(tuple([e])+y)
        return z

class Combinations(IncrementalSet):
    """A set-like container that incrementally determines all combinations of its inputs (IncrementalSets)"""
    def __init__(self, partmatchers):
        self._partmatchers = list(partmatchers)
        IncrementalSet.__init__(self, partmatchers)
        
    def _receive_add(self, source, obj):
        index = self._partmatchers.index(source)
        if index == -1:
            raise Exception("Unknown source")
        parts = []
        for i in range(len(self._partmatchers)):
            if i == index:
                parts.append([obj])
            else:
                parts.append(iter(self._partmatchers[i]))
        newmatches = combinations(parts)
        for match in newmatches:
            self._add(match)

    def _receive_remove(self, source, obj):
        index = self._partmatchers.index(source)
        if index == -1:
            raise Exception("Unknown source")
        toremove = []
        for match in iter(self):
            if obj in match:
                toremove.append(match)
        for match in toremove:
            self._remove(match)

    def __eq__(self, other):
        if isinstance(other, Combinations):
            return self._partmatchers == other.partmathers
        else:
            return False 

    def __hash__(self):
        return hash(tuple(self._partmatchers))

    def __repr__(self):
        return "Combinations(%s)"%str(self._partmatchers)


def combinations(listofiters):
    """All combinations of the objects in each iter, returned as a set of tuples"""
    #Note: this implementation could be faster; now as expensive as permutations
    if len(listofiters)==0:
        return []
    elif len(listofiters)==1:
        return map(lambda element: frozenset([element]), listofiters[0])
    else:
        l = list(listofiters[0])
        p = combinations(listofiters[1:])
        z = set()
        for e in l:
            for y in p:
                if e not in y:
                    z.add(tuple(frozenset([e]).union(y)))
        return z

class Debugger(IncrementalSet):
    """A set-like container that incrementally determines all combinations of its inputs (IncrementalSets)"""
    def __init__(self, watch_iset):
        self._watch = watch_iset
        IncrementalSet.__init__(self, [self._watch])
 
    def _receive_add(self, source, obj):
        print "add", obj, "to", source         

    def _receive_remove(self, source, obj):
        print "remove", obj, "to", source         

    def __eq__(self, other):
        if isinstance(other, Debugger):
            return self._watch == other.watch
        else:
            return False 

    def __hash__(self):
        return hash((self.__class__, self._watch))

    def __repr__(self):
        return "Debugger(%s)"%str(self._watch)




def test1():
    s = MutableSet([5,-3])
    s.add(1)
    s.add(2)
    print list(s)
    t = Filter(lambda x: x > 1,s)
    print list(t)
    s.remove(2)
    s.add(3)
    print list(t)

    p = MutableSet([1,2])
    q = MutableSet(['x', 'y'])
    r = Permutations((p,q))
    print list(r)
    p.add(3)
    print list(r)
    q.remove('x')
    print list(r)

    u = MutableSet(['a', 'b', 'c'])
    w = Combinations((u,u))
    print list(w)
    u.add('d')
    print list(w)
    u.remove('a')
    print list(w)

    print list(IncrementalSet._all)

def test2():
    integers = MutableSet([1,2,3,4,5,6,7,8,9,10])
    odd = lambda x: x%2 == 1
    square = lambda x: x**2
    odds1 = Filter(odd,integers)
    odds2 = Filter(odd,integers)
    sq1 = Map(square,odds1)
    sq2 = Map(square,odds2)
    print set(sq1), set(sq2)
    print list(IncrementalSet._all)

def test3():
    integers5 = MutableSet([1,2,3,4,5])
    integers10 = MutableSet([1,2,3,4,5,6,7,8,9,10])
    union = Union(integers5, integers10)
    intersection = Intersection(integers5, integers10)
    difference = Difference(integers10, integers5)
    integers5.remove(1)
    integers5.remove(2)
    integers10.remove(1)
    integers10.remove(10)
    print set(union)
    print set(intersection)
    print set(difference)


if __name__ == '__main__': 
    test1()
    test2()
    test3()
