#!/usr/bin/env python

"""
    Hidden commands are those whose handler begins with "_do_" instead
    of the usual "do_". These do not show up in the default help output
    and in readline completion lists.

    $ python cmdln_hidden.py visible
    hi from visible command
    $ python cmdln_hidden.py hidden
    hi from hidden command

    $ python cmdln_hidden.py #expecttest: INTERACTIVE, PROMPT="shell> "
    shell> visible
    hi from visible command
    shell> hidden
    hi from hidden command
    shell> ^D

    XXX Add tests for hidden vs. visible commands in default help when
        that is implemented.
"""

import sys
import cmdln

class Shell(cmdln.RawCmdln):
    name = "shell"
    def do_visible(self, argv):
        print("hi from visible command")
    def do_hidden(self, argv):
        print("hi from hidden command")

if __name__ == "__main__":
    sys.exit( Shell().main(loop=cmdln.LOOP_IF_EMPTY) )
