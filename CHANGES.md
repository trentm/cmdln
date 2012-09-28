# cmdln Changelog

## 1.1.3  (not released yet)

- Stop using `string.whitespace` because it can be an 8-bit string with
  non-ASCII chars in it, leading to potential `UnicodeDecodeError`s. See
  Komodo Bug 81316.


## 1.1.2

- Some Python 2.6-ification. No functional change.


## 1.1.1

- Issue 1: fix readline-based completion and history (from Joshua
  Gallagher).
- Experimental automatic bash completion support. See r8 for details:
    svn diff -r7:8 http://cmdln.googlecode.com/svn/trunk/cmdln.py
- Some minor improvements to line2argv processing (r7).
- Fix "${help_list}" layout problems and more closely follow optparse
  option list help output (r4).
- Moved project to Google Code (http://code.google.com/p/cmdln)
  for Subversion there and for the issue tracker.


## 1.1.0

- Experimental Bash completion integration. See "bash completion support"
  section in cmdln.py for details.


## 1.0.0

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


## 0.8.3

- Fix a bug where errors with passing an incorrect number of args to
  functions in do_foo() implementations would be masked.


## 0.8.2

- Remove the implicit prefixing of a command's help string with
  "${cmd_name}: ". This can be surprising for the case of a "help_FOO"
  function without an associated "cmd_FOO" function.


## 0.8.1

- Work on getting started docs.
- Improve the ${command_list} output to better handle *long* command
  names.
- Add ${cmd_usage} template var: infering a usage from the command
  handler signature.
- Add ${option_list} template var for the option table for the whole
  Cmdln class and add this to the default help output.


## v0.8.0

- First version at which I started stabilizing it for public release.
  I've been batting around modules to improve on `cmd.py` for a long
  time -- variously called `tm/cmd.py`, 'cmd2.py', 'tmCmd.py',
  'linecmd.py', 'argvcmd.py', etc.
