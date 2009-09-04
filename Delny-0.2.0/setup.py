#!/usr/bin/env python

# setup.py - build and install the Delny package
#
# Copyright 2004 Floris Bruynooghe
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

"""Delaunay triangulation.

This package can be used to make a Delaunay triangulation of a set of
n-dimennsional points.  Currently it uses the C libqhull library to do
the triangulation.
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: DFSG approved
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: English
Operating System :: OS Independent
Programming Language :: C
Programming Language :: Python
Topic :: Scientific/Engineering
"""


from distutils.core import setup, Extension


# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
import sys
if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None


module_qhull=Extension("delaunay._qhull",
                       sources=["delaunay/_qhullmodule.c"],
                       libraries=["qhull"])

doclines = __doc__.split("\n")

setup(name="Delny",
      version="0.2.0",
      author="Floris Bruynooghe",
      author_email="floris.bruynooghe@gmail.com",
      maintainer="Floris Bruynooghe",
      maintainer_email="floris.bruynooghe@gmail.com",
      url="http://flub.stuffwillmade.org/delny",
      license="GNU General Pucblic License (GPL)",
      description=doclines[0],
      long_description="\n".join(doclines[2:]),
      keywords=["delaunay", "qhull", "geometry", "triangulation"],
      platforms=["any"],
      download_url="http://flub.stuffwillmade.org/delny/dist/Delny-0.2.0.tar.gz",
      classifiers=filter(None, classifiers.split("\n")),
      packages=["delaunay"],
      ext_modules=[module_qhull])
