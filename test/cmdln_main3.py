#!/usr/bin/env python

"""
    $ python cmdln_main3.py
    This is my shell.

    $ python cmdln_main3.py foo
    hello from foo
"""

import sys
import cmdln

class Shell(cmdln.RawCmdln):
    "This is my shell."
    name = "shell"
    def do_foo(self, argv):
        print("hello from foo")

if __name__ == "__main__":
    shell = Shell()
    retval = shell.main(loop=cmdln.LOOP_NEVER) # don't want a command loop
    sys.exit(retval)

