from constraint import Constraint
from tolerance import tol_eq
from intersections import *


class SelectionConstraint(Constraint):
    """select solutions where function returns true when applied to given variables."""

    def __init__(self,function, vars):
        """init constraint with function and a sequence of variables"""
        self._variables = vars
        self._function = function
        
    def satisfied(self, map):
        """return True iff given solution (map) for given variables applied to function gives True""" 
        values = []
        for var in self._variables:
            values.append(map[var])
        return apply(self._function, values)==True
 
    def __str__(self):
         return "SelectionConstraint("+self._function.__name__+","+str(map(str, self._variables))+")"

def fnot(function):
    notf = lambda *args: not apply(function,args)
    notf.__name__ = "fnot("+function.__name__+")"
    return notf

def test():
    print SelectionConstraint(is_right_handed, ['a','b','c','d'])
    print SelectionConstraint(fnot(is_right_handed), ['a','b','c','d'])

if __name__ == "__main__": test()
