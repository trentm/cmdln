#!/usr/bin/env python

u"""Test cmdln.py unicode handling.

    $ python cmdln_unicode.py hi
    hi

    $ python cmdln_unicode.py #expecttest: INTERACTIVE, PROMPT="n\xe4me> "
    Welc\xf6me t\xf6 my shell.
    n\xe4me> hi
    hi
    n\xe4me> ^D
"""

import sys
import cmdln

class Shell(cmdln.RawCmdln):
    "This is my shell."
    name = u"n\xe4me"
    intro = u"Welc\xf6me t\xf6 my shell."
    def do_hi(self, argv):
        print "hi"


if __name__ == "__main__":
    sys.exit( Shell().main(loop=cmdln.LOOP_IF_EMPTY) )

