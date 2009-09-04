
GeoSolver is a python package for solving geometric constraint
problems. 

This distribution consists of:
    - a geometric constraints solver (geosolver)
    - a simple test module (solvertest) 
    - a graphical geometric constraint solving workbench (solvergui)
    - a python wrapper for qhull (Delny)

INSTALLATION INSTRUCTIONS
-------------------------

geosolver package
-----------------

You'll need Python2.5 or higher (but it's probably not compatible
with Python 3)

Copy directory 'geosolver' to the python library 
(e.g. /usr/lib/python2.X/site-packages) or add location of directory 
geosolver to PYTHONPATH (e.g. if geosolver is in /home/user/python, then
add /home/user/python to the python search path)

solvergui application 
---------------------

You'll need to install the geosolver package, as described above. 

In addition, you'll need to install Delny, which is 
a python wrapper to the qhull library, which is
used to compute convex hulls. 

Delny is included in this distribution, but not otherwise related. 
See the README in the Delny subdirectory for installation instructions. 

You will also need to have the following packages installed. 
These are not included in this distribution, but are 
available for most operating systems (e.g. as optional 
packages in most Linux distros, downloads for Windows)

- qhull (libqhull5) -- see http://www.qhull.org/
- pyQt4 -- see http://qt.nokia.com/
- pyOpenGL -- see http://pyopengl.sourceforge.net/
- Numpy -- http://numpy.scipy.org/


RUNNING
-------

To run geosolver tests:
>cd solvertest
>python test.py

To run solvergui:
>cd solvergui
>python main.py


DOCUMENTATION/API
-----------------

For developers, the best place to start is the pydoc 
documentation. The main API is the geomsolver.geometric 
module. For documentation type:

 pydoc geosolver.geometric








