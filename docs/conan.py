#!/usr/bin/env python

import sys
import textwrap

# use cmdln.py up one dir (for development)
from os.path import dirname
sys.path.insert(0, dirname(dirname(__file__)))
try:
    import cmdln
finally:
    del sys.path[0]

class Conan(cmdln.Cmdln):
    name = "conan"
    def do_hello(self, subcmd, opts):
        """${cmd_name}: Conan greets thee"""
        print "Ugh!"
    
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
            print "Conan confused."
        else:
            for enemy in enemies:
                print "%s %s!" % (action, enemy)
            print "Yargh!"

    @cmdln.alias("what_is_best", "best")
    def do_what_is_best_in_life(self, subcmd, opts):
        """${cmd_name}: Big monologue"""
        print textwrap.dedent("""\
            To crush your enemies,
            see them driven before you,
            and hear the lamentations of the women.""")

if __name__ == "__main__":
    conan = Conan()
    sys.exit( conan.main() )
