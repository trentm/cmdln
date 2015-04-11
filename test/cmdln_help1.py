#!/usr/bin/env python

"""
    $ python cmdln_help1.py help
    HelpShell: blah blah blah

    $ python cmdln_help1.py help documented
    documented: blah documented blah

    $ python cmdln_help1.py help hashelpfunc
    hashelpfunc: blah hashelpfunc blah

    $ python cmdln_help1.py help undocumented
    cmdln_help1.py: no help on 'undocumented'

    $ python cmdln_help1.py help undefined
    cmdln_help1.py: unknown command: 'undefined'
    Try 'cmdln_help1.py help' for info.

    $ python cmdln_help1.py #expecttest: INTERACTIVE, PROMPT="help-test> "
    help-test> help
    HelpShell: blah blah blah
    help-test> help documented
    documented: blah documented blah
    help-test> help hashelpfunc
    hashelpfunc: blah hashelpfunc blah
    help-test> help undocumented
    no help on 'undocumented'
    help-test> help undefined
    unknown command: 'undefined'
    help-test> ^D
"""

import sys
import cmdln

class HelpShell(cmdln.RawCmdln):
    """HelpShell: blah blah blah"""
    prompt = "help-test> "
    def do_documented(self, argv):
        """${cmd_name}: blah documented blah"""
    def do_undocumented(self, argv):
        pass
    def help_hashelpfunc(self):
        return "${cmd_name}: blah hashelpfunc blah"
    def do_hashelpfunc(self, argv):
        pass

if __name__ == "__main__":
    sys.exit(HelpShell().main(loop=cmdln.LOOP_IF_EMPTY))
