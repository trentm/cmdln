#!/usr/bin/env python
# Copyright (c) 2005 Trent Mick
# License: MIT License

"""Run doctests in various files in this project."""

import sys
from os.path import dirname, abspath, join
import unittest
import doctest

def suite():
    """Return a unittest.TestSuite to be used by test.py."""
    suite = unittest.TestSuite()
    sys.path.insert(0, join(dirname(dirname(abspath(__file__))), 'lib'))
    import cmdln
    suite.addTest(doctest.DocTestSuite(cmdln))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(sys.stdout, verbosity=2)
    result = runner.run(suite())
