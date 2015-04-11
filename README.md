# Why cmdln.py?

`cmdln.py` fixes some of the design flaws in `cmd.py` and takes advantage of
the `optparse` module so that it is more useful (and convenient) for
implementing command-line scripts/shells.

The main differences are:

- Instead of passing a command *line* to subcommand handlers, already
  parsed options and an args list are provided. This is *much* more
  convenient when the complexity of commands grows to have options,
  arguments with spaces, etc.
- By default the help for a subcommand is the associated method's
  docstring.  Default help output is also much nicer and some template
  vars can be used to automatically fill in some details.
- Defining command aliases is easy (using a new decorator).
- A `.main()` method is provided to make using your `Cmdln` subclass a
  little cleaner.
- The error handling (and associated hooks) have been improved so that
  trapping and dealing with errors in sub-command handlers (the `do_*`
  methods) can be done -- as might be wanted for a slighty more robust
  shell.

Install notes and intro docs are below. Please send any feedback to
[Trent Mick](mailto:trentm at google's mail thing).


# Python Versions

This currently supports Python 2.5, 2.6 and 2.7.
Working on 3.x support for cmdln 2.x.


# Install

To install it in your Python installation run *one* of the following:

    pip install cmdln
    pypm install cmdln      # if you use ActivePython (activestate.com/activepython)
    easy_install cmdln      # if this is the best you have
    python setup.py install

However, everything you need to run this is in "lib/cmdln.py". If it is
easier for you, you can just copy that file to somewhere on your PYTHONPATH
(to use as a module) or executable path (to use as a script).

# Introduction

`cmdln.py` is an extension of Python's default `cmd.py` module that
provides "a simple framework for writing line-oriented command
interpreters".  The idea (with both `cmd.py` and `cmdln.py`) is to be
able to quickly build multi-sub-command tools (think `cvs` or `svn`)
and/or simple interactive shells (think `gdb` or `pdb`).  `cmdln.py`'s
extensions make it more natural to write sub-commands, integrate
[optparse](http://docs.python.org/lib/module-optparse.html) for simple
option processing, and make having good command documentation easier.

For example, here is most of the scaffolding for the [svn
status](http://svnbook.red-bean.com/en/1.1/re26.html) command. (Note:
Some options were removed and the doc string truncated for brevity. See
[examples/svn.py](examples/svn.py) for a more complete scaffold
re-implementation of the `svn` command-line interface.)

    #!/usr/bin/env python
    import sys
    import cmdln

    class MySVN(cmdln.Cmdln):
        name = "svn"

        @cmdln.alias("stat", "st")
        @cmdln.option("-u", "--show-updates", action="store_true",
                      help="display update information")
        @cmdln.option("-v", "--verbose", action="store_true",
                      help="print extra information")
        def do_status(self, subcmd, opts, *paths):
            """${cmd_name}: print the status of working copy files and directories

            ${cmd_usage}
            ${cmd_option_list}
            """
            print "'svn %s' opts:  %s" % (subcmd, opts)
            print "'svn %s' paths: %s" % (subcmd, paths)


    if __name__ == "__main__":
        svn = MySVN()
        sys.exit(svn.main())


The base `cmdln.Cmdln` class is providing a number of things for free
here. (1) There is a reasonable default help string:

    $ python svn.py
    Usage:
        svn COMMAND [ARGS...]
        svn help [COMMAND]

    Commands:
        help (?)            give detailed help on a specific command
        status (st, stat)   print the status of working copy files and dire...

(2) A default `help` command is provided for getting detailed help on
specific sub-commands. This is how many such tools already work (e.g.
`svn` and `p4`, the command-line interface for the Perforce source
control system).

    $ python svn.py help status
    status (stat, st): print the status of working copy files and directories.

    Usage:
        svn status [PATHS...]

    Options:
        -h, --help          show this help message and exit
        -v, --verbose       print extra information
        -u, --show-updates  display update information

(3) It makes parsing the command line easy (with `optparse`
integration):

    $ python svn.py status -v foo bar baz
    'svn status' opts:  {'show_updates': None, 'verbose': True}
    'svn status' paths: ('foo', 'bar', 'baz')

and (4) defining command aliases easy:

    $ python svn.py st -v foo bar baz
    'svn st' opts:  {'show_updates': None, 'verbose': True}
    'svn st' paths: ('foo', 'bar', 'baz')

Read the [Getting Started docs](docs/getting_started.html) next.



# Development

Run the test suite via:

    make test

