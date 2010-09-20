#!/usr/bin/env python

"""
    $ python cmdln_main2.py
    This is my shell.

    $ python cmdln_main2.py foo
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
    retval = shell.cmd(sys.argv[1:]) # just run one command
    sys.exit(retval)

