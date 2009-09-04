#!/usr/bin/env python

# testcore.py - test of the core module
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
# Authors: Floris Bruynooghe (flub)

"""Test the core module from the delaunay package

This module provides the unittests for the core module of the delaunay
package.
"""


import unittest
import Numeric
import delaunay.core as core
from test import test_support


class TestTriangulation(unittest.TestCase):
    def test_constructor_2d(self):
        # delaunay.core.Triangulation(set): constructs fine? (2D)
        set = [(0,0),(2,1),(1,2),(4,0),(0,4),(4,4)]
        self.assert_(core.Triangulation(set))

    def test_constructor_3d(self):
        # delaunay.core.Triangulation(set): constructs fine? (3D)
        set = [(0,0,1), (4,0,1), (0,4,1), (4,4,0), (2,1,2), (1,2,3)]
        self.assert_(core.Triangulation(set))

    def test_sequence_types(self):
        # delaunay.core.Triangulation(): accepts all sequnce types?
        a = Numeric.array
        ltset = [(0,0),(2,1),(1,2),(4,0),(0,4),(4,4)]
        llset = [[0,0],[2,1],[1,2],[4,0],[0,4],[4,4]]
        tlset = ([0,0],[2,1],[1,2],[4,0],[0,4],[4,4])
        ttset = ((0,0),(2,1),(1,2),(4,0),(0,4),(4,4))
        lnset = [a((0,0)),a((2,1)),a((1,2)),a((4,0)),a((0,4)),a((4,4))]
        nnset = a([(0,0),(2,1),(1,2),(4,0),(0,4),(4,4)])
        all = (ltset, llset, tlset, ttset, lnset, nnset)
        for set in all:
            self.assert_(core.Triangulation(set))

    def test_dim(self):
        # delaunay.core.Triangulation(set, dim=?): constructs fine?
        set = [0,0,2,1,1,2,4,0,0,4,4,4]
        self.assert_(core.Triangulation(set, 2))
        set = [(0),(0),(2),(1),(1),(2),(4),(0),(0),(4),(4),(4)]
        self.assert_(core.Triangulation(set, 2))
        set = [(0,0,2),(1,1,2),(4,0,0),(4,4,4)]
        self.assert_(core.Triangulation(set, 2))
        set = [(0,0,2,1),(1,2,4,0),(0,4,4,4)]
        self.assert_(core.Triangulation(set, 2))


class TestTriangulationMethods(unittest.TestCase):
    def setUp(self):
        self.set = [(0,0),(2,1),(1,2),(4,0),(0,4),(4,4)]
        self.obj = core.Triangulation(self.set)

    def test_get_set(self):
        # delaunay.core.Triangulation.get_set(): returns correct set?
        self.set.sort()
        used_set = self.obj.get_set()
        used_set.sort()
        self.assertEqual(self.set, used_set)

    def test_getneighbours_type(self):
        # delaunay.core.Triangulation.get_neighbours(): correct type?
        # Type is dict?
        self.assert_(isinstance(self.obj.get_neighbours(), dict))
        # Type of keys of dict ok?
        for i in self.obj.get_neighbours().keys():
            self.assert_(isinstance(i, tuple))
            self.assertEqual(len(i), len(self.set[0]))
            for j in i:
                self.assert_(isinstance(j, float))
        # Type of values of dict ok?
        for i in self.obj.get_neighbours().values():
            self.assert_(isinstance(i, list))
            for j in i:
                self.assert_(isinstance(j, tuple))
                self.assertEqual(len(j), len(self.set[0]))
                for k in j:
                    self.assert_(isinstance(k, float))

    def test_getneighbours_points(self):
        # delaunay.core.Triangulation.get_neighbours(): points are from set?
        for i in self.obj.get_neighbours().keys():
            self.assert_(i in self.set)
        for i in self.obj.get_neighbours().values():
            for j in i:
                self.assert_(j in self.set)

    def test_getelements_type(self):
        # delaunay.core.Triangulation.get_elements(): correct type?
        # Type is list?
        self.assert_(isinstance(self.obj.get_elements(), list))
        # List contains lists of tuples  of correct dimension of floats?
        for i in self.obj.get_elements():
            self.assert_(isinstance(i, list))
            for j in i:
                self.assert_(isinstance(j, tuple))
                self.assertEqual(len(j), len(self.set[0]))
                for k in j:
                    self.assert_(isinstance(k, float))

    def test_getelements_points(self):
        # All points returned are from the set?
        for i in self.obj.get_elements():
            for j in i:
                self.assert_(j in self.set)

    def test_get_elements_by_index_type(self):
        # Correct type returned by .get_elements_indices()?
        self.assert_(isinstance(self.obj.get_elements_indices(), list))
        for i in self.obj.get_elements_indices():
            self.assert_(isinstance(i, list))
            for j in i:
                self.assert_(isinstance(j, int))

    def test_updateset(self):
        # delaunay.core.Triangulation.update_set(): modifies triangulation?
        old_elements = self.obj.get_elements()
        old_neighbours = self.obj.get_neighbours()
        new_set = [(0,0),(2,1),(1,2),(5,0),(0,5),(5,5)]
        self.obj.update_set(new_set)
        self.assertEqual(new_set.sort(), self.obj.get_set().sort())
        self.assertNotEqual(old_elements, self.obj.get_elements())
        self.assertNotEqual(old_neighbours, self.obj.get_neighbours())


def test_main():
    test_support.run_unittest(TestTriangulation,
                              TestTriangulationMethods)


if __name__ == '__main__':
    test_main()
