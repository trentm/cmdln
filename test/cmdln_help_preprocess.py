#!/usr/bin/env python

r"""
    $ python cmdln_help_preprocess.py
    Usage:
        svn COMMAND [ARGS...]
        svn help [COMMAND]
    <BLANKLINE>    
    Options:
        -h, --help  show this help message and exit
    <BLANKLINE>
    Commands:
        help (?)          give detailed help on a specific sub-command
        status (st, stat) 
                          Print the status of working copy files and directories.
    <BLANKLINE>
    Additional help topics (run `svn help TOPIC'):
        foo


    $ python cmdln_help_preprocess.py help
    Usage:
        svn COMMAND [ARGS...]
        svn help [COMMAND]
    <BLANKLINE>    
    Options:
        -h, --help  show this help message and exit
    <BLANKLINE>
    Commands:
        help (?)          give detailed help on a specific sub-command
        status (st, stat) 
                          Print the status of working copy files and directories.
    <BLANKLINE>
    Additional help topics (run `svn help TOPIC'):
        foo


    $ python cmdln_help_preprocess.py help status
    status (stat, st): Print the status of working copy files and directories.
    <BLANKLINE>
    Usage:
        svn status [PATHS...]
    <BLANKLINE>
    Options:
        -h, --help          show this help message and exit
        -u, --show-updates  display update information
        -v, --verbose       print extra information
        -N, --non-recursive
                            operate on single directory only
        -q, --quiet         print as little as possible
        --no-ignore         disregard default and svn:ignore property ignores
        --username=USERNAME
                            specify a username ARG
        --password=PASSWORD
                            specify a password ARG
        --no-auth-cache     do not cache authentication tokens
        --non-interactive   do no interactive prompting
        --config-dir=CONFIG_DIR
                            read user configuration files from directory ARG
    <BLANKLINE>
    ...discussion...
"""

import os
import sys
try:
    import cmdln
except ImportError:
    sys.path.insert(0, os.pardir)
    import cmdln
    del sys.path[0]


class MySVN(cmdln.Cmdln):
    name = "svn"

    @cmdln.alias("stat", "st")
    @cmdln.option("--config-dir",
                  help="read user configuration files from directory ARG")
    @cmdln.option("--non-interactive", action="store_true", 
                  help="do no interactive prompting")
    @cmdln.option("--no-auth-cache", action="store_true",
                  help="do not cache authentication tokens")
    @cmdln.option("--password",
                  help="specify a password ARG")
    @cmdln.option("--username",
                  help="specify a username ARG")
    @cmdln.option("--no-ignore", action="store_true",
                  help="disregard default and svn:ignore property ignores")
    @cmdln.option("-q", "--quiet", action="store_true",
                  help="print as little as possible")
    @cmdln.option("-N", "--non-recursive", action="store_true",
                  help="operate on single directory only")
    @cmdln.option("-v", "--verbose", action="store_true",
                  help="print extra information")
    @cmdln.option("-u", "--show-updates", action="store_true",
                  help="display update information")
    def do_status(self, subcmd, opts, *paths):
        """${cmd_name}: Print the status of working copy files and directories.

        ${cmd_usage}
        ${cmd_option_list}
        ...discussion...
        """
        print "handle 'svn %s'" % subcmd
        print "...opts=%s" % opts
        print "...paths=%s" % (paths,)

    def help_foo(self):
        return """
        blah blah blah
        """


if __name__ == "__main__":
    svn = MySVN()
    sys.exit(svn.main())

