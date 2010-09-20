#!/usr/bin/env python

"""The cmdln.py test suite entry point."""

import os
from os.path import dirname, abspath, join
import sys

sys.path.insert(0, join(dirname(dirname(abspath(__file__))), "support", "testlib"))
try:
    import testlib
finally:
    del sys.path[0]


def setup():
    cmdln_lib_dir = join(dirname(dirname(abspath(__file__))), "lib")
    if "PYTHONPATH" in os.environ:
        os.environ["PYTHONPATH"] = os.pathsep.join(
            [cmdln_lib_dir, os.environ["PYTHONPATH"]])
    else:
        os.environ["PYTHONPATH"] = cmdln_lib_dir
    sys.path.insert(0, cmdln_lib_dir)

#TODO: hook test_doctests.py into this
if __name__ == "__main__":
    retval = testlib.harness(
        testdir_from_ns={None: dirname(abspath(__file__))},
        setup_func=setup)
    sys.exit(retval)

