#!/usr/bin/env python

"""
    $ python cmdln_helloworld.py #expecttest: INTERACTIVE, PROMPT="hi> "
    hi> hi
    Hi, stranger!
    hi> hi Trent
    Hi, Trent!
    hi> ^D

    $ python cmdln_helloworld.py hi Guido
    Hi, Guido!
"""

import sys
import cmdln

class HelloWorld(cmdln.RawCmdln):
    prompt = "hi> "
    def do_hi(self, argv):
        """say hi"""
        name = len(argv)>1 and argv[1] or "stranger"
        print "Hi, %s!" % name

if __name__ == "__main__":
    sys.exit(HelloWorld().main(loop=cmdln.LOOP_IF_EMPTY))

