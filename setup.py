#!/usr/bin/env python
# Copyright (c) 2005 ActiveState Corp.

"""setup script for 'cmdln'"""

import sys
import os
import shutil
from distutils.core import setup

import cmdln


#---- setup mainline

setup(name="cmdln",
      version=cmdln.__version__,
      description="an improved cmd.py for writing multi-command scripts and shells",
      author="Trent Mick",
      author_email="TrentM@ActiveState.com",
      url="http://trentm.com/projects/cmdln/",
      license="MIT License",
      platforms=["Windows", "Linux", "Mac OS X", "Unix"],
      long_description="""\
`cmdln.py` is an extension of Python's default `cmd.py` module that
provides "a simple framework for writing line-oriented command
interpreters".  The idea (with both cmd.py and cmdln.py) is to be able
to quickly build multi-sub-command tools (think cvs or svn) and/or
simple interactive shells (think gdb or pdb).  Cmdln's extensions make
it more natural to write sub-commands, integrate optparse for simple
option processing, and make having good command documentation easier.
""",
      keywords=["cmdln", "cmd", "shell", "command-line"],

      py_modules=['cmdln'],
     )

