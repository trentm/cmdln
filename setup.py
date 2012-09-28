#!/usr/bin/env python
# Copyright (c) 2002-2008 ActiveState Software

"""An improved cmd.py for writing multi-command scripts and shells.

`cmdln.py` is an extension of Python's default `cmd.py` module that
provides "a simple framework for writing line-oriented command
interpreters".  The idea (with both cmd.py and cmdln.py) is to be able
to quickly build multi-sub-command tools (think cvs or svn) and/or
simple interactive shells (think gdb or pdb).  Cmdln's extensions make
it more natural to write sub-commands, integrate optparse for simple
option processing, and make having good command documentation easier.
"""

import sys
import os
from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
try:
    import cmdln
finally:
    del sys.path[0]

classifiers = """\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 2
Topic :: Software Development :: Libraries :: Python Modules
"""

doclines = __doc__.split("\n")

setup(
    name="cmdln",
    version=cmdln.__version__,
    maintainer="Trent Mick",
    maintainer_email="trentm@gmail.com",
    url="http://code.google.com/p/cmdln/",
    license="http://www.opensource.org/licenses/mit-license.php",
    platforms=["any"],
    py_modules=["cmdln"],
    package_dir={"": "lib"},
    description=doclines[0],
    classifiers=filter(None, classifiers.split("\n")),
    long_description="\n".join(doclines[2:]),
)
