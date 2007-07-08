#!/usr/bin/env python

"""
    $ sh -c "python cmdln_retval.py nothing && echo RETVAL=$?"
    RETVAL=0
    $ sh -c "python cmdln_retval.py success && echo RETVAL=$?"
    RETVAL=0
    $ sh -c "python cmdln_retval.py failure || echo RETVAL=$?"
    RETVAL=1
    $ sh -c "python cmdln_retval.py ultimate || echo RETVAL=$?"
    RETVAL=42

    $ sh -c "python cmdln_retval.py && echo RETVAL=$?" #expecttest: INTERACTIVE, PROMPT="shell> "
    shell> ^D
    RETVAL=0

    $ sh -c "python cmdln_retval.py && echo RETVAL=$?" #expecttest: INTERACTIVE, PROMPT="shell> "
    shell> exit
    RETVAL=0

    $ sh -c "python cmdln_retval.py || echo RETVAL=$?" #expecttest: INTERACTIVE, PROMPT="shell> "
    shell> exit 43
    RETVAL=43

Test for a non-zero exit value for a raised exception in subcommand
handling.

    $ sh -c "python cmdln_retval.py || echo RETVAL=$?" #expecttest: INTERACTIVE, PROMPT="shell> "
    shell> exit not-an-int
    Traceback.*RETVAL=1

    $ sh -c "python cmdln_retval.py exit not-an-int || echo RETVAL=$?"
    Traceback.*RETVAL=1

    $ sh -c "python cmdln_retval.py bogus-command || echo RETVAL=$?"
    shell: unknown command: 'bogus-command'
    Try 'shell help' for info.
    RETVAL=1
"""

import sys
import cmdln

class Shell(cmdln.RawCmdln):
    "This is my shell."
    name = "shell"
    def do_nothing(self, argv):
        pass
    def do_success(self, argv):
        return 0
    def do_failure(self, argv):
        return 1
    def do_ultimate(self, argv):
        return 42
    def do_exit(self, argv):
        """usage: exit [retval]"""
        self.stop = True
        if len(argv) <= 1:
            return 0
        else:
            return int(argv[1])


if __name__ == "__main__":
    sys.exit( Shell().main(loop=cmdln.LOOP_IF_EMPTY) )

