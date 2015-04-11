# This is just a play file for mucking around with cmdln.py

"""this is the module docstring"""


import os
import sys
import cmdln
import pprint
import getopt
from optparse import OptionParser
import logging


class Error(Exception):
    pass

log = logging.getLogger("foo")

from optparse import OptionParser
class CmdlnOptionParser(OptionParser):
    """OptionParser subclass for:
    - better error handling for user error in specifying options
    - better handling of the "help" action
    """
    #XXX Need to key off when optparse.py changes from sys.exit(<str>),
    #    Python 2.3, to self.exit(<status>, <msg>), Python 2.4, and
    #    adjust.
    def __init__(self, shell, subcmd, *args, **kwargs):
        OptionParser.__init__(self, *args, **kwargs)
        self.shell = shell
        self.subcmd = subcmd
    def print_help(self, file=None):
        retval = self.shell.do_help(["help", self.subcmd])
        self.exit(retval)
    def error(self, msg):
        #XXX make a CmdlnError class?
        #    Could raise optparse.OptionError???
        raise Error(self.subcmd+": "+msg)

class Shell(cmdln.Cmdln):
    def do_mksandbox(self, argv):
        """this is the mksandbox docstring"""
        # Process options and arguments.
        parser = CmdlnOptionParser(self, "mksandbox")
        parser.add_option("-f", "--force", dest="force", action="store_true")
        parser.add_option("-n", "--dry-run", dest="dryrun", action="store_true")
        parser.add_option("-B", "--base", dest="base")
        parser.set_defaults(help=False, force=False, dryrun=False, base="/Sandbox")
        try:
            options, args = parser.parse_args(argv[1:])
        except SystemExit, ex:
            if not ex.code:
                return
            else:
                return ex.code

            print dir(ex)
            print "ARGS:", ex.args
            print "CODE:", ex.code
            raise Error("boo")
        #if options.help:
        #    return self.do_help(["help", argv[0]])
        if len(args) != 0:
            raise Error("incorrect number of arguments: %r\n"
                        "Try `foo help %s'." % (args, argv[0]))


def main(argv):
    log.setLevel(logging.INFO)

##    # Process command line.
##    try:
##        optlist, args = getopt.getopt(argv[1:], "hVvq",
##            ["help", "version", "verbose", "quiet"])
##    except getopt.GetoptError, ex:
##        raise Error(str(ex))
##        return 1
##    help = False
##    for opt, optarg in optlist:
##        if opt in ("-h", "--help"):
##            help = True
##        elif opt in ("-V", "--version"):
##            ver = '.'.join(map(str, __version__))
##            print "foo %s" % ver
##            return 0
##        elif opt in ("-v", "--verbose"):
##            log.setLevel(logging.DEBUG)
##        elif opt in ("-q", "--quiet"):
##            log.setLevel(logging.WARN)
    parser = OptionParser("foo.py [options...] <subcmd> ...", version="foo 1.0.0")
##    parser.add_option("-V", "--version", action="store_true",
##                      help="print version and exit")
    parser.add_option("-V", action="version",
                      help="print version and exit")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="be more verbose")
    parser.add_option("-q", "--quiet", action="store_true",
                      help="quieter output")
    parser.disable_interspersed_args()
    options, args = parser.parse_args(argv[1:])

    shell = Shell()
    if help == True:
        return shell.cmd(["help"])
    else:
        return shell.main(args, loop=cmdln.LOOP_NEVER)

##
##    shell = Shell()
##    shell.add_option(...)
##    shell.add_option(...)

if __name__ == "__main__":
    if sys.version_info[:2] <= (2,2): __file__ = sys.argv[0]
    logging.basicConfig()
    try:
        retval = main(sys.argv)
    except SystemExit, ex:
        raise
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        exc_info = sys.exc_info()
        if log.isEnabledFor(logging.DEBUG):
            import traceback
            print
            traceback.print_exception(*exc_info)
        else:
            if hasattr(exc_info[0], "__name__"):
                #log.error("%s: %s", exc_info[0].__name__, exc_info[1])
                log.error(exc_info[1])
            else:  # string exception
                log.error(exc_info[0])
        sys.exit(1)
    else:
        sys.exit(retval)
