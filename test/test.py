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
    cmdln_src_dir = dirname(dirname(abspath(__file__)))
    if "PYTHONPATH" in os.environ:
        os.environ["PYTHONPATH"] = os.pathsep.join(
            [cmdln_src_dir, os.environ["PYTHONPATH"]])
    else:
        os.environ["PYTHONPATH"] = cmdln_src_dir

if __name__ == "__main__":
    retval = testlib.harness(setup_func=setup)
    sys.exit(retval)

