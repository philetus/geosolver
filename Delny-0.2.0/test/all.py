#!/usr/bin/env python

# all.py - run all test modules in this directory.
#
# Copyright 2006 Floris Bruynooghe
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


import os
import os.path
from test import regrtest

# FIXME: temp imports
from pprint import pprint


testdir = os.path.abspath(os.path.dirname(__file__))
files = [os.path.join(testdir, f) for f in os.listdir(testdir)]
test_modules = []
for f in filter(os.path.isfile, files):
    if f[-3:] != ".py":
        continue
    f = os.path.basename(f)
    if f.startswith("test_"):
        test_modules.append(f[:-3])

for module in map(__import__, test_modules):
    print "\nRunning tests from %s:" % module.__name__
    print "="*(20+len(module.__name__)), "\n"
    module.test_main()
