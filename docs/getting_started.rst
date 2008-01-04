Getting Started with ``cmdln.py``
=================================

.. contents:: Table of Contents


Not Even "Hello World"
----------------------

::

    #!/usr/bin/env python
    import sys
    import cmdln

    class Conan(cmdln.Cmdln):
        pass

    if __name__ == "__main__":
        conan = Conan()
        sys.exit( conan.main() )

This is the absolute bare minimum usage of ``Cmdln`` and, predictably, with
this you don't get much. But you don't get nothing. Save the above to a file
called "conan.py" and try it out. (Or you can download `the finished conan.py
<conan.py>`_.)::

    $ python conan.py
    Usage:
        conan.py COMMAND [ARGS...]
        conan.py help [COMMAND]

    Options:
        -h, --help  show this help message and exit

    Commands:
        help (?)   give detailed help on a specific sub-command

Basically you get help. A good command-line tool should make it easy to
figure out how to use the thing. You (mostly) get this for free with
``cmdln.py``. The help message is available (as with most good tools) with the
'-h' or '--help' option::

    $ python conan.py --help
    Usage:
        conan.py COMMAND [ARGS...]
    ...

And a reasonable error message is shown for incorrect usage::

    $ python conan.py -X
    conan.py: no such option: -X
    Try 'conan.py help' for info.

Good multi-subcommand tools (like 'svn' and 'conan') also provide a 'help'
command that is used to learn about the various subcommands. But first we
have to add some.


Hello World
-----------

::

    #!/usr/bin/env python
    import sys
    import cmdln

    class Conan(cmdln.Cmdln):
        name = "conan"                    # (1)
        def do_hello(self, subcmd, opts): # (2)
            """Conan greets thee"""       # (3)
            print "Ugh!"

    if __name__ == "__main__":
        conan = Conan()
        sys.exit( conan.main() )


We've added the "hello" command to Conan's vocabulary. Things to note:

1. A "name" value is used in Cmdln's various standard user messages.
   Generally you want to specify a name matching the command that users use
   to invoke your script. If not specified it is inferred from ``sys.argv``.

2. A command is defined with a ``do_COMMANDNAME`` method with the following
   signature::

        def do_COMMANDNAME(self, subcmd, opts, ...):
            """help content for the command"""
            ...

   More on the ...'s later.

3. A command function's docstring acts as its help string.

::

    $ python conan.py
    Usage:
        conan COMMAND [ARGS...]
        conan help COMMAND

    Options:
        -h, --help  show this help message and exit

    Commands:
        hello      Conan greets thee
        help (?)   give detailed help on a specific sub-command

    $ python conan.py hello
    Ugh!



The Standard "help" Command
---------------------------

As mentioned above, ``Cmdln`` provides a "help" command. The "help" command
provides help on other commands::

    $ python conan.py help help
    help (?): give detailed help on a specific sub-command

    conan help COMMAND

    $ python conan.py help hello
    Conan greets thee



Commands Features
-----------------

::

    #!/usr/bin/env python
    import sys
    import cmdln

    class Conan(cmdln.Cmdln):
        name = "conan"
        def do_hello(self, subcmd, opts):
            """Conan greets thee"""
            print "Ugh!"
        
        def do_crush(self, subcmd, opts, enemy):
            print "Crush %s!" % enemy

    if __name__ == "__main__":
        conan = Conan()
        sys.exit( conan.main() )

The "hello" command isn't that interesting. Let's work on a "crush"
command to show the facilities that ``Cmdln`` provides. In the first
incarnation "crush" takes one argument::

    $ python conan.py crush Trent
    Crush Trent!

*exactly* one argument::

    $ python conan.py crush            
    conan crush: takes exactly 1 argument (0 given)
    Try 'conan help crush' for info.

    $ python conan.py crush Trent Guido
    conan crush: takes exactly 1 argument (2 given)
    Try 'conan help crush' for info.

    $ python conan.py help crush
    conan: no help on 'crush'

We haven't provided any help for the "crush" command. Let's do that::

    ...
        def do_crush(self, subcmd, opts, enemy):
            """${cmd_name}: crush your enemy!

            ${cmd_usage}                            # (1)
            """
            print "Crush %s!" % enemy
    ...


Giving us::
    
    $ python conan.py help crush
    crush: crush your enemy!

    Usage:
        conan crush ENEMY


1. The ``Cmdln`` class tries to make it easy for you to write decent help.  It
   provides a number of template variables that you can use in your command
   help strings. Here we've used ``${cmd_usage}``. The authoritative list of
   these is the ``RawCmdln._help_preprocess`` method in ``cmdln.py``, but here
   are some of them::

        ${name}
            The tool's/shell's name, i.e. 'self.name'.
        ${option_list}
            A formatted table of options for this shell/tool.
        ${command_list}
            A formatted table of available sub-commands.
        ${help_list}
            A formatted table of additional help topics (i.e. 'help_*'
            methods with no matching 'do_*' method).
        ${cmd_name}
            The name (and aliases) for this sub-command formatted as:
            "NAME (ALIAS1, ALIAS2, ...)".
        ${cmd_usage}
            A formatted usage block inferred from the command function
            signature.
        ${cmd_option_list}
            A formatted table of options for this sub-command.

   Sometimes you'll want to hardcode your own help strings for better
   documentation, but often these template vars will do a good enough job.


We probably want Conan to be able to crush many enemies and perhaps use
different weapons::

    @cmdln.option("-w", "--weapon",                     # (1)
                  help="what weapon should Conan use?")
    def do_crush(self, subcmd, opts, *enemies):         # (2)
        """${cmd_name}: crush your enemies!

        ${cmd_usage}
        ${cmd_option_list}                              # (3)
        C.f. Conan the Barbarian.
        """
        action = {
            None: "Crush",
            "sword": "Swipe",
            "spear": "Pierce",
            "maul": "Crush",
        }.get(opts.weapon, None)                        # (4)
        if not action:
            print "Conan confused."
        else:
            for enemy in enemies:
                print "%s %s!" % (action, enemy)
            print "Yargh!"

We've changed a few things here:

1. We specified the '-w' option for 'crush'. Every command function has an
   associated ``optparser`` -- which is an instance of
   ``cmdln.SubCmdOptionParser`` (derived from ``optparse.OptionParser`` in the
   Python stdlib). By default each command supports a ``-h/--help`` option.
   More can be added (as we've done here) with the ``cmdln.option`` decorator_.
   This is synonymous to calling ``add_option`` on the underlying OptionParser
   as described here_.

   Note: Decorators were added in Python 2.4 so you'll have to have Python
   2.4 or greater to use the ``option`` decorator. An alternative is to create
   your own ``SubCmdOptionParser`` instance and assign it to the ``optparser``
   attribute of the command handler (which is pretty ugly but does the job)::

        def do_crush(self, subcmd, opts, *enemies):
            # ...
        do_foo.optparser = cmdln.SubCmdOptionParser()
        do_foo.optparser.add_option(
            "-w", "--weapon",
            help="what weapon should Conan use?")

2. We've changed the function signature to take a number of enemies using
   Python's syntax for declaring a variable number of arguments. This tells the
   underlying dispatcher in ``cmdln.py`` that ``crush`` accepts any number of
   arguments.

3. We've used the ``${cmd_option_list}`` template variable. This uses
   ``optparse``'s facility to nicely print out the available options and their
   help strings.

4. The parsed options are given to the third argument -- typically called
   ``opts``. This is a standard ``optparse.Values`` instance.

Let's try it out::

    $ python conan.py help crush
    crush: crush your enemies!

    Usage:
        conan crush [ENEMIES...]

    Options:
        -h, --help          show this help message and exit
        -w WEAPON, --weapon=WEAPON
                            what weapon should Conan use?

    C.f. Conan the Barbarian.

    $ python conan.py crush Trent Guido
    Crush Trent!
    Crush Guido!
    Yargh!

    $ python conan.py crush Trent Guido -w spear
    Pierce Trent!
    Pierce Guido!
    Yargh!

    $ python conan.py crush Trent Guido -w axe  
    Conan confused.

    $ python conan.py crush Trent Guido -w sword
    Swipe Trent!
    Swipe Guido!
    Yargh!


.. _decorator: http://www.python.org/peps/pep-0318.html
.. _here: http://docs.python.org/lib/optparse-tutorial.html



Command Aliases
---------------

With options it is often advisable to have both a long (descriptive) name
and a short (convenient) one. The same can be nice with commands. You can use
aliases for this. Lets show this with a new command::

    ...
    class Conan(cmdln.Cmdln):
        ...
        @cmdln.alias("what_is_best", "best")
        def do_what_is_best_in_life(self, subcmd, opts):
            """${cmd_name}: Big monologue"""
            print textwrap.dedent("""\
                To crush your enemies,
                see them driven before you,
                and hear the lamentations of the women.""")
    ...

Here we've defined two aliases for the ``what_is_best_in_life`` command:
``what_is_best`` and ``best``. These will be shown in the list of commands::

    $ python conan.py help
    ...
    Commands:
        crush             crush your enemies!
        hello             Conan greets thee
        help (?)          give detailed help on a specific sub-command
        what_is_best_in_life (best, what_is_best)
                          Big monologue

and in the help just for this command::

    $ python conan.py help what_is_best
    what_is_best_in_life (what_is_best, best): Big monologue

Note that the standard help command has ``?`` as an alias so that last command
could have been written ``python conan.py ? best``.

We can now ask Conan what is best in life::

    $ python conan.py best
    To crush your enemies,
    see them driven before you,
    and hear the lamentations of the women.


TODO
----

Eventually I'll add discussion of the following ``cmdln.py`` features in this
document. Until then, `use the source <../cmdln.py>`_.

- use "loop" option to main to show creating a shell: control prompt, intro
  message, error messages

- a different example to show "help_list" and separate ``help_*`` commands

- show passing in optparser to main()

- perhaps come back to Conan shell to show *overriding* the postcmd to make a
  shell counter: i.e. prompt has an incrementing number

- show usage of CmdlnOptionParser to add more base-level options
  Explain what is diff about it, i.e. why to use over optparse.OptionParser.

- hidden command _do_*

- "Don't do me any Favours": talk about RawCmdln and (self, argv)-style command
  signatures


