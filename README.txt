cmdln.py -- an improved cmd.py
==============================

Download the latest cmdln.py packages from here:
    (archive) http://cmdln.googlecode.com/files/cmdln-1.1.2.zip


Home            : http://trentm.com/projects/cmdln/
License         : MIT (see LICENSE.txt)
Platforms       : Windows, Linux, Mac OS X, Unix
Current Version : 1.1.2
Dev Status      : well tested; a similar design has been used in various
                  heavily used scripts at ActiveState for a while; some
                  features of this module *are* faily new though
Requirements    : Python >= 2.3 (http://www.activestate.com/ActivePython/),
                  (Python >= 2.4 to use some features using decorators)
Documentation   : Why cmdln.py?
                  Install Notes
                  Introduction
                  Getting Started (docs/getting_started.html)
                  Change Log


Why cmdln.py?
-------------

`cmdln.py` fixes some of the design flaws in `cmd.py` and takes
advantage of new Python stdlib modules (e.g. optparse) so that it is
more useful (and convenient) for implementing command-line
scripts/shells.

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


Install Notes
-------------

Download the latest `cmdln.py` source package, unzip it, and run
`python setup.py install`:

    unzip cmdln-1.1.2.zip
    cd cmdln-1.1.2
    python setup.py install

If your install fails then please visit [the Troubleshooting
FAQ](http://trentm.com/faq.html#troubleshooting-python-package-installation).

This will install `cmdln.py` into your Python's site-packages area.
`cmdln.py` has no external dependencies that aren't part of the Python
standard library so, if you like, you may simple copy `cmdln.py` into
your own Python packages.


Introduction
------------

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


Change Log
----------

### v1.1.2
- Some Python 2.6-ification. No functional change.

### v1.1.1
- Issue 1: fix readline-based completion and history (from Joshua
  Gallagher).
- Experimental automatic bash completion support. See r8 for details:
    svn diff -r7:8 http://cmdln.googlecode.com/svn/trunk/cmdln.py
- Some minor improvements to line2argv processing (r7).
- Fix "${help_list}" layout problems and more closely follow optparse
  option list help output (r4).
- Moved project to Google Code (http://code.google.com/p/cmdln)
  for Subversion there and for the issue tracker.

### v1.1.0
- Experimental Bash completion integration. See "bash completion support"
  section in cmdln.py for details.

### v1.0.0
- [backward incompat] `Cmdln.main()` no longer takes an `optparser`
  argument. Top-level option parsing has been changed so that top-level
  options for a `Cmdln` subclass can more naturally be defined and
  handled on the class definition. Changes:
  - `Cmdln.main()` calls `self.get_optparser` to get an option handler.
    Subclasses should overload this method for custom top-level options.
  - After option parsing, but before sub-command handling, the
    `self.postoptparse()` hook is called.
- Add a `version` attribute on `Cmdln` subclasses. If set, the default
  top-level option parser will have a `--version` attribute.
- [backward incompat] Simplify the StopProcessing/opts.stop handling for
  option handling in subcommands. The "opts" argument to "do_*"
  sub-command functions will no longer have a "stop" value.
  StopProcessing is now called StopOptionProcessing. This shouldn't
  affect simple usage of cmdln.py.

### v0.8.3
- Fix a bug where errors with passing an incorrect number of args to
  functions in do_foo() implementations would be masked.

### v0.8.2
- Remove the implicit prefixing of a command's help string with
  "${cmd_name}: ". This can be surprising for the case of a "help_FOO"
  function without an associated "cmd_FOO" function.

### v0.8.1
- Work on getting started docs.
- Improve the ${command_list} output to better handle *long* command
  names.
- Add ${cmd_usage} template var: infering a usage from the command
  handler signature.
- Add ${option_list} template var for the option table for the whole
  Cmdln class and add this to the default help output.

### v0.8.0

- First version at which I started stabilizing it for public release.
  I've been batting around modules to improve on `cmd.py` for a long
  time -- variously called `tm/cmd.py`, 'cmd2.py', 'tmCmd.py',
  'linecmd.py', 'argvcmd.py', etc.

