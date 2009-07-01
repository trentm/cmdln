#!/usr/bin/env python

"""Generate a man page for the given cmdln.Cmdln subclass.

Usage:
    python mkmanpage.py mymodule.Foo > tmp/man1/foo.1

then via that man page with `man -M tmp foo.1`.
"""

from os.path import dirname, join, abspath
import sys

sys.path.insert(0, join(dirname(dirname(abspath(__file__))), "lib"))
import cmdln


def mkmanpage(name):
    """Return man page content for the given `cmdln.Cmdln` subclass name."""
    mod_name, class_name = name.rsplit('.', 1)
    mod = __import__(mod_name)
    inst = getattr(mod, class_name)()
    sections = cmdln.man_sections_from_cmdln(inst)
    sys.stdout.write(''.join(sections))


#---- mainline

if __name__ == "__main__":
    sys.exit( mkmanpage(sys.argv[1]) )

