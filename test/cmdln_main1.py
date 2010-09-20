#!/usr/bin/env python

"""
    $ python cmdln_main1.py foo
    hello from foo

    $ python cmdln_main1.py #expecttest: INTERACTIVE, PROMPT="shell> "
    shell> foo
    hello from foo
    shell> ^D
"""

import sys
import cmdln

class Shell(cmdln.RawCmdln):
    "This is my shell."
    name = "shell"
    def do_foo(self, argv):
        print("hello from foo")

if __name__ == "__main__":
    sys.exit( Shell().main(loop=cmdln.LOOP_IF_EMPTY) )

