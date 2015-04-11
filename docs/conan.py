#!/usr/bin/env python

from __future__ import print_function
import sys
import textwrap

# Use ../lib/cmdln.py.
from os.path import dirname, join, abspath
sys.path.insert(0, join(dirname(dirname(abspath(__file__))), "lib"))
try:
    import cmdln
finally:
    del sys.path[0]

class Conan(cmdln.Cmdln):
    name = "conan"
    def do_hello(self, subcmd, opts):
        """${cmd_name}: Conan greets thee"""
        print("Ugh!")

    @cmdln.option("-w", "--weapon", help="what weapon should Conan use?")
    def do_crush(self, subcmd, opts, *enemies):
        """${cmd_name}: crush your enemies!

        ${cmd_usage}
        ${cmd_option_list}
        C.f. Conan the Barbarian.
        """
        action = {
            None: "Crush",
            "sword": "Swipe",
            "spear": "Pierce",
            "maul": "Crush",
        }.get(opts.weapon, None)
        if not action:
            print("Conan confused.")
        else:
            for enemy in enemies:
                print("%s %s!" % (action, enemy))
            print("Yargh!")

    @cmdln.alias("what_is_best", "best")
    def do_what_is_best_in_life(self, subcmd, opts):
        """${cmd_name}: Big monologue"""
        print(textwrap.dedent("""\
            To crush your enemies,
            see them driven before you,
            and hear the lamentations of the women."""))

if __name__ == "__main__":
    conan = Conan()
    sys.exit( conan.main() )
