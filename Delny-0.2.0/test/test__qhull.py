#!/usr/bin/env python

# test_qhull.py - test of _qhull module
#
# Copyright 2004, 2006 Floris Bruynooghe
#
# This file is part of Delny.
#
# Delny is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Delny is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Delny; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
#
#
# Author: Floris Bruynooghe (flub)

"""Test the _qhull module from the delaunay package

This module provides the unittests for the _qhull module of the delaunay
package.
"""


import unittest

import Numeric
import RandomArray

import delaunay._qhull

from test import test_support


class TestQhullFunctions(unittest.TestCase):
    """This tests the types and structures returned."""
    def setUp(self):
        # Prepare a set of points and their neighbours.
        self.set = [(0,0),(2,1),(1,2),(4,0),(0,4),(4,4)]
        result = delaunay._qhull.delny(self.set)
        self.neighbours = result[0]
        self.elements = result[1]
        self.elements_by_index = result[2]

    def test_nb_dict(self):
        # delaunay._qhull.delny: neighbours are returned as a dict?
        self.assert_(isinstance(self.neighbours, dict))

    def test_nb_keys(self):
        # delaunay._qhull.delny: neighbours keys are of correct type?
        for i in self.neighbours.keys():
            self.assert_(isinstance(i, tuple))
            self.assertEqual(len(i), len(self.set[0]))
            for j in i:
                self.assert_(isinstance(j, float))

    def test_nb_values(self):
        # delaunay._qhull.delny: neighbours values are of correct type?
        for i in self.neighbours.values():
            self.assert_(isinstance(i, list))
            for j in i:
                self.assert_(isinstance(j, tuple))
                self.assertEqual(len(j), len(self.set[0]))
                for k in j:
                    self.assert_(isinstance(k, float))

    def test_nb_points(self):
        # delaunay._qhull.delny: all points in neighbours are from the set?
        for i in self.neighbours.keys():
            self.assert_(i in self.set)
        for i in self.neighbours.values():
            for j in i:
                self.assert_(j in self.set)
        
    def test_elem_list(self):
        # delaunay._qhull.delny: returned elements are in a list?
        self.assert_(isinstance(self.elements, list))

    def test_elem(self):
        # delaunay._qhull.delny: returned elements have correct type?
        for i in self.elements:
            self.assert_(isinstance(i, list))
            for j in i:
                self.assert_(isinstance(j, tuple))
                self.assertEqual(len(j), len(self.set[0]))
                for k in j:
                    self.assert_(isinstance(k, float))

    def test_elem_points(self):
        # delaunay._qhull.delny: all points from elements are in the set?
        for i in self.elements:
            for j in i:
                self.assert_(j in self.set)

    def test_elem_index(self):
        # Type of facet_list is correct?
        self.assert_(isinstance(self.elements_by_index, list))
        for i in self.elements_by_index:
            self.assert_(isinstance(i, list))
            for j in i:
                self.assert_(isinstance(j, int))


class TestPredictedOutputs2D(unittest.TestCase):
    """Values used in this class come from the qhull binary"""

    def setUp(self):
        self.set = [(0,0),(2,1),(1,2),(4,0),(0,4),(4,4)]
        self.nb, self.el, self.el_i = delaunay._qhull.delny(self.set)
    
    def test_neighbours(self):
        # delaunay._qhull.delny: neighbours are as predicted? (2D)
        nb = {(0,0): [(2,1), (4,0), (1,2), (0,4)],
              (0,4): [(1,2), (0,0), (4,4)],
              (1,2): [(0,4), (0,0), (2,1), (4,4)],
              (2,1): [(4,0), (0,0), (4,4), (1,2)],
              (4,0): [(2,1), (0,0), (4,4)],
              (4,4): [(2,1), (4,0), (1,2), (0,4)]}
        # sort the lists for each key
        for l1, l2 in zip(nb.values(), self.nb.values()):
            l1.sort()
            l2.sort()
        self.assertEqual(self.nb, nb)
        
    def test_elements(self):
        # delaunay._qhull.delny: elements are as predicted? (2D)
        el = [[(2,1), (4,0), (0,0)],
              [(4,4), (2,1), (4,0)],
              [(1,2), (0,4), (0,0)],
              [(1,2), (2,1), (0,0)],
              [(1,2), (4,4), (0,4)],
              [(1,2), (4,4), (2,1)]]
        for l in el:
            l.sort()
        for l in self.el:
            l.sort()
        el.sort()
        self.el.sort()
        self.assertEqual(self.el, el)

    def test_elements_by_index(self):
        # Elements are as predicted?  (2d)
        el_i = [[1, 3, 0], [5, 1, 3], [2, 4, 0],
                [2, 1, 0], [2, 5, 4], [2, 5, 1]]
        for l in el_i:
            l.sort()
        for l in self.el_i:
            l.sort()
        el_i.sort()
        self.el_i.sort()
        self.assertEqual(self.el_i, el_i)

    def disabled_test_square(self):
        # delaunay._qhull.delny: 2D square triangulates?
        # FIXME: For this to work option `Qz' is needed.  See notes
        # for ideas and issues.
        #set = [(0,0),(1,0),(0,1),(1,1)]
        #self.assert_(delaunay._qhull.delny(set))
        self.fail("currently not possible")


class TestPredictedOutputs3D(unittest.TestCase):
    """Values used in this class come from the qhull binary"""

    def setUp(self):
        self.set = [(0,0,1), (4,0,1), (0,4,1), (4,4,0), (2,1,2), (1,2,3)]
        self.nb, self.el, self.el_i = delaunay._qhull.delny(self.set)
    
    def test_neigbours(self):
        # delaunay._qhull.delny: neighbours are as predicted? (3D)
        nb = {(0,0,1): [(4,0,1), (0,4,1), (4,4,0), (2,1,2), (1,2,3)],
              (4,0,1): [(0,0,1), (4,4,0), (2,1,2), (1,2,3)],
              (0,4,1): [(0,0,1), (4,4,0), (2,1,2), (1,2,3)],
              (4,4,0): [(0,0,1), (4,0,1), (0,4,1), (2,1,2), (1,2,3)],
              (2,1,2): [(0,0,1), (4,0,1), (0,4,1), (4,4,0), (1,2,3)],
              (1,2,3): [(0,0,1), (4,0,1), (0,4,1), (4,4,0), (2,1,2)]}
        for l in nb.values():
            l.sort()
        for l in self.nb.values():
            l.sort()
        self.assertEqual(self.nb, nb)

    def test_elements(self):
        # delaunay._qhull.delny: elements are as predicted? (3D)
        el = [[(2,1,2), (4,4,0), (4,0,1), (0,0,1)],
              [(2,1,2), (4,4,0), (1,2,3), (4,0,1)],
              [(2,1,2), (1,2,3), (0,4,1), (0,0,1)],
              [(4,4,0), (2,1,2), (0,4,1), (0,0,1)],
              [(4,4,0), (2,1,2), (1,2,3), (0,4,1)]]
        for l in el:
            l.sort()
        for l in self.el:
            l.sort()
        el.sort()
        self.el.sort()
        self.assertEqual(self.el, el)

    def test_elements_by_index(self):
        # Elements by index are as predicted?
        el_i = [[4, 3, 1, 0], [4, 3, 5, 1],
                [4, 5, 2, 0], [3, 4, 2, 0], [3, 4, 5, 2]]
        for l in el_i:
            l.sort()
        for l in self.el_i:
            l.sort()
        el_i.sort()
        self.el_i.sort()
        self.assertEqual(self.el_i, el_i)


class EatingOfNodes(unittest.TestCase):
    def setUp(self):
        self.number = 50
        X = RandomArray.random(self.number)
        Y = RandomArray.random(self.number)
        Z = RandomArray.random(self.number)
        co = Numeric.array([X, Y, Z])
        self.points = []
        for i in range(len(co[0])):
            self.points.append(tuple(co[:,i].tolist()))

    def test_no_nodes(self):
        #_qhull.delny(set) does not eat nodes?
        # Do this many times as it does not always happen
        for i in range(self.number):
            neighbours, elements, elements_by_index \
                        = delaunay._qhull.delny(self.points)
            self.assertEqual(self.number, len(neighbours))


def test_main():
    test_support.run_unittest(TestQhullFunctions,
                              TestPredictedOutputs2D,
                              TestPredictedOutputs3D,
                              EatingOfNodes)


if __name__ == '__main__':
    test_main()
