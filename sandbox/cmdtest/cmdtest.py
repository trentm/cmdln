#!/usr/bin/env python
#
# Command-line script cmdtest
#
# TODO: license
#

#TODO: drop all globs and clear_globs stuff
r"""
    cmdtest -- a framework for running command-line examples in docstrings

    Usage:

        python cmdtest.py [<options...>] <scripts...>

    Options:
        -h, --help          Print this help and exit.
        -V, --version       Print the version of this script and exit.
        -v, --verbose       Increase the verbosity of output
        -q, --quiet         Only print output for warnings and errors.

    In simplest use, call cmdtest.py with each script to be tested as an
    argument:

        python cmdtest.py SCRIPT.py

    or, if cmdtest.py is on your Python path and you are using Python >=2.4:

        python -m cmdtest SCRIPT.py

    The will cause the shell command examples in the docstrings to get
    executed and verified.

    This won't display anything unless an example fails, in which case the
    failing example(s) and the cause(s) of the failure(s) are printed to stdout
    (why not stderr? because stderr is a lame hack <0.2 wink>), and the final
    line of output is "Test failed.".

    Run it with the -v switch instead:

        python cmdtest.py -v SCRIPT.py

    and a detailed report of all examples tried is printed to stdout, along
    with assorted summaries at the end.

    There are a variety of other ways to run cmdtests, including integration
    with the unittest framework, and support for running non-Python text
    files containing cmdtests.  There are also many ways to override parts
    of cmdtest's default behaviors.

    The cmdtest framework is based on Python's core "cmdtest" (originally
    written by Tim Peters) and borrows many of the same ideas.
"""

__version_info__ = (0,1,0)
#TODO: __all__

#TODO: clean up imports
from os.path import splitext, basename, dirname
import sys, traceback, inspect, linecache, os, re, types
import unittest, difflib, pdb, tempfile
import warnings
from StringIO import StringIO
import logging
import glob
import getopt


#TODO: this out of date?
# There are 4 basic classes:
#  - Example: a <source, want> pair, plus an intra-docstring line number.
#  - CmdTest: a collection of examples, parsed from a docstring, plus
#    info about where the docstring came from (name, filename, lineno).
#  - CmdTestFinder: extracts CmdTests from a given object's docstring and
#    its contained objects' docstrings.
#  - CmdTestRunner: runs CmdTest cases, and accumulates statistics.
#
# So the basic picture is:
#
#                             list of:
# +------+                   +---------+                   +-------+
# |object| --CmdTestFinder-> | CmdTest | --CmdTestRunner-> |results|
# +------+                   +---------+                   +-------+
#                            | Example |
#                            |   ...   |
#                            | Example |
#                            +---------+

# Option constants.
#TODO: rationalize constants, some for stdout vs. stderr?

OPTIONFLAGS_BY_NAME = {}
def register_optionflag(name):
    flag = 1 << len(OPTIONFLAGS_BY_NAME)
    OPTIONFLAGS_BY_NAME[name] = flag
    return flag

DONT_ACCEPT_BLANKLINE = register_optionflag('DONT_ACCEPT_BLANKLINE')
NORMALIZE_WHITESPACE = register_optionflag('NORMALIZE_WHITESPACE')
ELLIPSIS = register_optionflag('ELLIPSIS')
IGNORE_EXCEPTION_DETAIL = register_optionflag('IGNORE_EXCEPTION_DETAIL')

COMPARISON_FLAGS = (DONT_ACCEPT_BLANKLINE |
                    NORMALIZE_WHITESPACE |
                    ELLIPSIS |
                    IGNORE_EXCEPTION_DETAIL)

REPORT_UDIFF = register_optionflag('REPORT_UDIFF')
REPORT_CDIFF = register_optionflag('REPORT_CDIFF')
REPORT_NDIFF = register_optionflag('REPORT_NDIFF')
REPORT_ONLY_FIRST_FAILURE = register_optionflag('REPORT_ONLY_FIRST_FAILURE')

REPORTING_FLAGS = (REPORT_UDIFF |
                   REPORT_CDIFF |
                   REPORT_NDIFF |
                   REPORT_ONLY_FIRST_FAILURE)

# Special string markers for use in `want` strings:
BLANKLINE_MARKER = '<BLANKLINE>'
ELLIPSIS_MARKER = '...'

######################################################################
## Table of Contents
######################################################################
#  1. Utility Functions
#  2. Example & CmdTest -- store test cases
#  3. CmdTest Parser -- extracts examples from strings
#  4. CmdTest Finder -- extracts test cases from objects
#  5. CmdTest Runner -- runs test cases
#  6. Test Functions -- convenient wrappers for testing
#TODO: renumber
#  8. Unittest Support

######################################################################
## 1. Utility Functions
######################################################################

##def _normalize_module(module, depth=2):
##    """
##    Return the module specified by `module`.  In particular:
##      - If `module` is a module, then return module.
##      - If `module` is a string, then import and return the
##        module with that name.
##      - If `module` is None, then return the calling module.
##        The calling module is assumed to be the module of
##        the stack frame at the given depth in the call stack.
##    """
##    if inspect.ismodule(module):
##        return module
##    elif isinstance(module, (str, unicode)):
##        return __import__(module, globals(), locals(), ["*"])
##    elif module is None:
##        return sys.modules[sys._getframe(depth).f_globals['__name__']]
##    else:
##        raise TypeError("Expected a module, string, or None")

def _indent(s, indent=4):
    """
    Add the given number of space characters to the beginning every
    non-blank line in `s`, and return the result.
    """
    # This regexp matches the start of non-blank lines:
    return re.sub('(?m)^(?!$)', indent*' ', s)

def _exception_traceback(exc_info):
    """
    Return a string containing a traceback message for the given
    exc_info tuple (as returned by sys.exc_info()).
    """
    # Get a traceback message.
    excout = StringIO()
    exc_type, exc_val, exc_tb = exc_info
    traceback.print_exception(exc_type, exc_val, exc_tb, file=excout)
    return excout.getvalue()

# Override some StringIO methods.
class _SpoofOut(StringIO):
    def getvalue(self):
        result = StringIO.getvalue(self)
        # If anything at all was written, make sure there's a trailing
        # newline.  There's no way for the expected output to indicate
        # that a trailing newline is missing.
        if result and not result.endswith("\n"):
            result += "\n"
        # Prevent softspace from screwing up the next test case, in
        # case they used print with a trailing comma in an example.
        if hasattr(self, "softspace"):
            del self.softspace
        return result

    def truncate(self,   size=None):
        StringIO.truncate(self, size)
        if hasattr(self, "softspace"):
            del self.softspace

# Worst-case linear-time ellipsis matching.
def _ellipsis_match(want, got):
    """
    Essentially the only subtle case:
    >>> _ellipsis_match('aa...aa', 'aaa')
    False
    """
    if ELLIPSIS_MARKER not in want:
        return want == got

    # Find "the real" strings.
    ws = want.split(ELLIPSIS_MARKER)
    assert len(ws) >= 2

    # Deal with exact matches possibly needed at one or both ends.
    startpos, endpos = 0, len(got)
    w = ws[0]
    if w:   # starts with exact match
        if got.startswith(w):
            startpos = len(w)
            del ws[0]
        else:
            return False
    w = ws[-1]
    if w:   # ends with exact match
        if got.endswith(w):
            endpos -= len(w)
            del ws[-1]
        else:
            return False

    if startpos > endpos:
        # Exact end matches required more characters than we have, as in
        # _ellipsis_match('aa...aa', 'aaa')
        return False

    # For the rest, we only need to find the leftmost non-overlapping
    # match for each piece.  If there's no overall match that way alone,
    # there's no overall match period.
    for w in ws:
        # w may be '' at times, if there are consecutive ellipses, or
        # due to an ellipsis at the start or end of `want`.  That's OK.
        # Search for an empty string succeeds, and doesn't change startpos.
        startpos = got.find(w, startpos, endpos)
        if startpos < 0:
            return False
        startpos += len(w)

    return True

def _comment_line(line):
    "Return a commented form of the given line"
    line = line.rstrip()
    if line:
        return '# '+line
    else:
        return '#'

### [XX] Normalize with respect to os.path.pardir?
##def _module_relative_path(module, path):
##    if not inspect.ismodule(module):
##        raise TypeError, 'Expected a module: %r' % module
##    if path.startswith('/'):
##        raise ValueError, 'Module-relative files may not have absolute paths'
##
##    # Find the base directory for the path.
##    if hasattr(module, '__file__'):
##        # A normal module/package
##        basedir = os.path.split(module.__file__)[0]
##    elif module.__name__ == '__main__':
##        # An interactive session.
##        if len(sys.argv)>0 and sys.argv[0] != '':
##            basedir = os.path.split(sys.argv[0])[0]
##        else:
##            basedir = os.curdir
##    else:
##        # A module w/o __file__ (this includes builtins)
##        raise ValueError("Can't resolve paths relative to the module " +
##                         module + " (it has no __file__)")
##
##    # Combine the base directory and the path.
##    return os.path.join(basedir, *(path.split('/')))

#TODO: s/source/command/g
######################################################################
## 2. Example & CmdTest
######################################################################
## - An "example" is a <source, want> pair, where "source" is a
##   fragment of source code, and "want" is the expected output for
##   "source."  The Example class also includes information about
##   where the example was extracted from.
##
## - A "cmdtest" is a collection of examples, typically extracted from
##   a string (such as an object's docstring).  The CmdTest class also
##   includes information about where the string was extracted from.

class Example:
    """
    A single cmdtest example, consisting of command and expected
    output.  `Example` defines the following attributes:

      - command: A single shell command, always ending with a newline.
        The constructor adds a newline if needed.

      - want: The expected output from running the command (either
        from stdout, or a traceback in case of exception).  `want` ends
        with a newline unless it's empty, in which case it's an empty
        string.  The constructor adds a newline if needed.

      - exc_msg: The exception message generated by the example, if
        the example is expected to generate an exception; or `None` if
        it is not expected to generate an exception.  This exception
        message is compared against the return value of
        `traceback.format_exception_only()`.  `exc_msg` ends with a
        newline unless it's `None`.  The constructor adds a newline
        if needed.

      - lineno: The line number within the CmdTest string containing
        this Example where the Example begins.  This line number is
        zero-based, with respect to the beginning of the CmdTest.

      - indent: The example's indentation in the CmdTest string.
        I.e., the number of space characters that preceed the
        example's first prompt.

      - options: A dictionary mapping from option flags to True or
        False, which is used to override default options for this
        example.  Any option flags not contained in this dictionary
        are left at their default value (as specified by the
        CmdTestRunner's optionflags).  By default, no options are set.
    """
    def __init__(self, command, want, exc_msg=None, lineno=0, indent=0,
                 options=None):
        # Normalize inputs.
        if not command.endswith('\n'):
            command += '\n'
        if want and not want.endswith('\n'):
            want += '\n'
        if exc_msg is not None and not exc_msg.endswith('\n'):
            exc_msg += '\n'
        # Store properties.
        self.command = command
        self.want = want
        self.lineno = lineno
        self.indent = indent
        if options is None: options = {}
        self.options = options
        self.exc_msg = exc_msg

    def __repr__(self):
        return "<Example at line %d: '%s'>" % (self.lineno, self.command)

#TODO: look into "should be run in a single environment" because this
#      is different for cmdtest: separate cmdtest blocks in the same
#      docstring should *not* be the same session, should they? Maybe
#      they *should* be the same session. Yes. E.g.:
#
#       $ set FOO=bar
#
#       $ echo $FOO
#       bar
#
class CmdTest:
    """
    A collection of cmdtest examples that should be run in a single
    environment.  Each `CmdTest` defines the following attributes:

      - examples: the list of examples.

      - name: A name identifying the CmdTest (typically, the name of
        the object whose docstring this CmdTest was extracted from).

      - filename: The name of the file that this CmdTest was extracted
        from, or `None` if the filename is unknown.

      - lineno: The line number within filename where this CmdTest
        begins, or `None` if the line number is unavailable.  This
        line number is zero-based, with respect to the beginning of
        the file.

      - docstring: The string that the examples were extracted from,
        or `None` if the string is unavailable.
    """
    def __init__(self, examples, name, filename, lineno, docstring):
        """
        Create a new CmdTest containing the given examples.
        """
        assert not isinstance(examples, basestring), \
               "CmdTest no longer accepts str; use CmdTestParser instead"
        self.examples = examples
        self.docstring = docstring
        self.name = name
        self.filename = filename
        self.lineno = lineno

    def __repr__(self):
        if len(self.examples) == 0:
            examples = 'no examples'
        elif len(self.examples) == 1:
            examples = '1 example'
        else:
            examples = '%d examples' % len(self.examples)
        return ('<CmdTest %s from %s:%s (%s)>' %
                (self.name, self.filename, self.lineno, examples))

    # This lets us sort tests by name:
    def __cmp__(self, other):
        if not isinstance(other, CmdTest):
            return -1
        return cmp((self.name, self.filename, self.lineno, id(self)),
                   (other.name, other.filename, other.lineno, id(other)))

######################################################################
## 3. CmdTestParser
######################################################################

class CmdTestParser:
    """
    A class used to parse strings containing cmdtest examples.
    """
    # This regular expression is used to find cmdtest examples in a
    # string.  It defines three groups: `command` is the command string
    # (including leading indentation and prompts); `indent` is the
    # indentation of the first (PS1) line of the source code; and
    # `want` is the expected output (including leading indentation).
    _EXAMPLE_RE = re.compile(r'''
        # Source consists of a PS1 line followed by zero or more PS2 lines.
        (?P<command>
            (?:^(?P<indent> [ ]*) \$    .*)    # PS1 line
            (?:\n           [ ]*  >     .*)*)  # PS2 lines
        \n?
        # Want consists of any non-blank lines that do not start with PS1.
        (?P<want> (?:(?![ ]*$)    # Not a blank line
                     (?![ ]*\$)   # Not a line starting with PS1
                     .*$\n?       # But any other line
                  )*)
        ''', re.MULTILINE | re.VERBOSE)

    # A regular expression for handling `want` strings that contain
    # expected exceptions.  It divides `want` into three pieces:
    #    - the traceback header line (`hdr`)
    #    - the traceback stack (`stack`)
    #    - the exception message (`msg`), as generated by
    #      traceback.format_exception_only()
    # `msg` may have multiple lines.  We assume/require that the
    # exception message is the first non-indented line starting with a word
    # character following the traceback header line.
    _EXCEPTION_RE = re.compile(r"""
        # Grab the traceback header.  Different versions of Python have
        # said different things on the first traceback line.
        ^(?P<hdr> Traceback\ \(
            (?: most\ recent\ call\ last
            |   innermost\ last
            ) \) :
        )
        \s* $                # toss trailing whitespace on the header.
        (?P<stack> .*?)      # don't blink: absorb stuff until...
        ^ (?P<msg> \w+ .*)   #     a line *starts* with alphanum.
        """, re.VERBOSE | re.MULTILINE | re.DOTALL)

    # A callable returning a true value iff its argument is a blank line
    # or contains a single comment.
    _IS_BLANK_OR_COMMENT = re.compile(r'^[ ]*(#.*)?$').match

    def parse(self, string, name='<string>'):
        """
        Divide the given string into examples and intervening text,
        and return them as a list of alternating Examples and strings.
        Line numbers for the Examples are 0-based.  The optional
        argument `name` is a name identifying this string, and is only
        used for error messages.
        """
        string = string.expandtabs()
        # If all lines begin with the same indentation, then strip it.
        min_indent = self._min_indent(string)
        if min_indent > 0:
            string = '\n'.join([l[min_indent:] for l in string.split('\n')])

        output = []
        charno, lineno = 0, 0
        # Find all cmdtest examples in the string:
        for m in self._EXAMPLE_RE.finditer(string):
            # Add the pre-example text to `output`.
            output.append(string[charno:m.start()])
            # Update lineno (lines before this example)
            lineno += string.count('\n', charno, m.start())
            # Extract info from the regexp match.
            (command, options, want, exc_msg) = \
                     self._parse_example(m, name, lineno)
            # Create an Example, and add it to the list.
            if not self._IS_BLANK_OR_COMMENT(command):
                output.append( Example(command, want, exc_msg,
                                    lineno=lineno,
                                    indent=min_indent+len(m.group('indent')),
                                    options=options) )
            # Update lineno (lines inside this example)
            lineno += string.count('\n', m.start(), m.end())
            # Update charno.
            charno = m.end()
        # Add any remaining post-example text to `output`.
        output.append(string[charno:])
        return output

    def get_cmdtest(self, string, name, filename, lineno):
        """
        Extract all cmdtest examples from the given string, and
        collect them into a `CmdTest` object.

        `name`, `filename`, and `lineno` are attributes for
        the new `CmdTest` object.  See the documentation for `CmdTest`
        for more information.
        """
        return CmdTest(self.get_examples(string, name),
                       name, filename, lineno, string)

    def get_examples(self, string, name='<string>'):
        """
        Extract all cmdtest examples from the given string, and return
        them as a list of `Example` objects.  Line numbers are
        0-based, because it's most common in cmdtests that nothing
        interesting appears on the same line as opening triple-quote,
        and so the first interesting line is called \"line 1\" then.

        The optional argument `name` is a name identifying this
        string, and is only used for error messages.
        """
        return [x for x in self.parse(string, name)
                if isinstance(x, Example)]

    def _parse_example(self, m, name, lineno):
        """
        Given a regular expression match from `_EXAMPLE_RE` (`m`),
        return a pair `(command, want)`, where `command` is the matched
        example's command code (with prompts and indentation stripped);
        and `want` is the example's expected output (with indentation
        stripped).

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        # Get the example's indentation level.
        indent = len(m.group('indent'))

        # Divide command into lines; check that they're properly
        # indented; and then strip their indentation & prompts.
        command_lines = m.group('command').split('\n')
        self._check_prompt_blank(command_lines, indent, name, lineno)
        self._check_prefix(command_lines[1:], ' '*indent + '>', name, lineno)
        command = '\n'.join([cl[indent+1:] for cl in command_lines])

        # Divide want into lines; check that it's properly indented; and
        # then strip the indentation.  Spaces before the last newline should
        # be preserved, so plain rstrip() isn't good enough.
        want = m.group('want')
        want_lines = want.split('\n')
        if len(want_lines) > 1 and re.match(r' *$', want_lines[-1]):
            del want_lines[-1]  # forget final newline & spaces after it
        self._check_prefix(want_lines, ' '*indent, name,
                           lineno + len(command_lines))
        want = '\n'.join([wl[indent:] for wl in want_lines])

        # If `want` contains a traceback message, then extract it.
        m = self._EXCEPTION_RE.match(want)
        if m:
            exc_msg = m.group('msg')
        else:
            exc_msg = None

        # Extract options from the command.
        options = self._find_options(command, name, lineno)
        #TODO: parse *out* the option string/comment: it will 
        #      muck up execution on Windows, and possibly muck up
        #      multi-line commands on all systems

        return command, options, want, exc_msg

    # This regular expression looks for option directives in the
    # command string of an example.  Option directives are comments
    # starting with "cmdtest:".  Warning: this may give false
    # positives for string-literals that contain the string
    # "#cmdtest:".  Eliminating these false positives would require
    # actually parsing the string; but we limit them by ignoring any
    # line containing "#cmdtest:" that is *followed* by a quote mark.
    _OPTION_DIRECTIVE_RE = re.compile(r'#\s*cmdtest:\s*([^\n\'"]*)$',
                                      re.MULTILINE)

    def _find_options(self, command, name, lineno):
        """
        Return a dictionary containing option overrides extracted from
        option directives in the given command string.

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        options = {}
        # (note: with the current regexp, this will match at most once:)
        for m in self._OPTION_DIRECTIVE_RE.finditer(command):
            option_strings = m.group(1).replace(',', ' ').split()
            for option in option_strings:
                if (option[0] not in '+-' or
                    option[1:] not in OPTIONFLAGS_BY_NAME):
                    raise ValueError('line %r of the cmdtest for %s '
                                     'has an invalid option: %r' %
                                     (lineno+1, name, option))
                flag = OPTIONFLAGS_BY_NAME[option[1:]]
                options[flag] = (option[0] == '+')
        if options and self._IS_BLANK_OR_COMMENT(command):
            raise ValueError('line %r of the cmdtest for %s has an option '
                             'directive on a line with no example: %r' %
                             (lineno, name, command))
        return options

    # This regular expression finds the indentation of every non-blank
    # line in a string.
    _INDENT_RE = re.compile('^([ ]*)(?=\S)', re.MULTILINE)

    def _min_indent(self, s):
        "Return the minimum indentation of any non-blank line in `s`"
        indents = [len(indent) for indent in self._INDENT_RE.findall(s)]
        if len(indents) > 0:
            return min(indents)
        else:
            return 0

    def _check_prompt_blank(self, lines, indent, name, lineno):
        """
        Given the lines of a command string (including prompts and
        leading indentation), check to make sure that every prompt is
        followed by a space character.  If any line is not followed by
        a space character, then raise ValueError.
        """
        for i, line in enumerate(lines):
            if len(line) >= indent+2 and line[indent+1] != ' ':
                raise ValueError('line %r of the docstring for %s '
                                 'lacks blank after %s: %r' %
                                 (lineno+i+1, name,
                                  line[indent:indent+1], line))

    def _check_prefix(self, lines, prefix, name, lineno):
        """
        Check that every line in the given list starts with the given
        prefix; if any line does not, then raise a ValueError.
        """
        for i, line in enumerate(lines):
            if line and not line.startswith(prefix):
                raise ValueError('line %r of the docstring for %s has '
                                 'inconsistent leading whitespace: %r' %
                                 (lineno+i+1, name, line))


######################################################################
## 4. CmdTest Finder
######################################################################

#TODO: perhaps "CmdTestFinder = doctest.DocTestFinder" would work?
class CmdTestFinder:
    """
    A class used to extract the CmdTests that are relevant to a given
    object, from its docstring and the docstrings of its contained
    objects.  Doctests can currently be extracted from the following
    object types: modules, functions, classes, methods, staticmethods,
    classmethods, and properties.
    """

    def __init__(self, verbose=False, parser=CmdTestParser(),
                 recurse=True, exclude_empty=True):
        """
        Create a new cmdtest finder.

        The optional argument `parser` specifies a class or
        function that should be used to create new CmdTest objects (or
        objects that implement the same interface as CmdTest).  The
        signature for this factory function should match the signature
        of the CmdTest constructor.

        If the optional argument `recurse` is false, then `find` will
        only examine the given object, and not any contained objects.

        If the optional argument `exclude_empty` is false, then `find`
        will include tests for objects with empty docstrings.
        """
        self._parser = parser
        self._verbose = verbose
        self._recurse = recurse
        self._exclude_empty = exclude_empty

    def find(self, filepath):
        """
        Return a list of the CmdTests that are defined by the given
        script's docstring, or by any of its contained objects'
        docstrings.

        TODO:
            - STARTHERE
            - must note that the script *must be importable* without
              side-effect
            - ideally would not *import* the module to get this info,
              but would just compile it (a la pythoncile)
        """
        # Import the given script.
        import imp
        name = splitext(basename(filepath))[0]
        iinfo = imp.find_module(name, [dirname(filepath)])
        obj = module = imp.load_module(name, *iinfo)

        # Read the module's source code.  This is used by
        # CmdTestFinder._find_lineno to find the line number for a
        # given object's docstring.
        try:
            file = inspect.getsourcefile(obj) or inspect.getfile(obj)
            source_lines = linecache.getlines(file)
            if not source_lines:
                source_lines = None
        except TypeError:
            source_lines = None

        # Recursively explore `obj`, extracting CmdTests.
        tests = []
        self._find(tests, obj, name, module, source_lines, {})
        return tests

    def _from_module(self, module, object):
        """
        Return true if the given object is defined in the given
        module.
        """
        if module is None:
            return True
        elif inspect.isfunction(object):
            return module.__dict__ is object.func_globals
        elif inspect.isclass(object):
            return module.__name__ == object.__module__
        elif inspect.getmodule(object) is not None:
            return module is inspect.getmodule(object)
        elif hasattr(object, '__module__'):
            return module.__name__ == object.__module__
        elif isinstance(object, property):
            return True # [XX] no way not be sure.
        else:
            raise ValueError("object must be a class or function")

    def _find(self, tests, obj, name, module, source_lines, seen):
        """
        Find tests for the given object and any contained objects, and
        add them to `tests`.
        """
        if self._verbose:
            print 'Finding tests in %s' % name

        # If we've already processed this object, then ignore it.
        if id(obj) in seen:
            return
        seen[id(obj)] = 1

        # Find a test for this object, and add it to the list of tests.
        test = self._get_test(obj, name, module, source_lines)
        if test is not None:
            tests.append(test)

        # Look for tests in a module's contained objects.
        if inspect.ismodule(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                valname = '%s.%s' % (name, valname)
                # Recurse to functions & classes.
                if ((inspect.isfunction(val) or inspect.isclass(val)) and
                    self._from_module(module, val)):
                    self._find(tests, val, valname, module, source_lines,
                               seen)

        # Look for tests in a module's __test__ dictionary.
        if inspect.ismodule(obj) and self._recurse:
            for valname, val in getattr(obj, '__test__', {}).items():
                if not isinstance(valname, basestring):
                    raise ValueError("CmdTestFinder.find: __test__ keys "
                                     "must be strings: %r" %
                                     (type(valname),))
                if not (inspect.isfunction(val) or inspect.isclass(val) or
                        inspect.ismethod(val) or inspect.ismodule(val) or
                        isinstance(val, basestring)):
                    raise ValueError("CmdTestFinder.find: __test__ values "
                                     "must be strings, functions, methods, "
                                     "classes, or modules: %r" %
                                     (type(val),))
                valname = '%s.__test__.%s' % (name, valname)
                self._find(tests, val, valname, module, source_lines,
                           seen)

        # Look for tests in a class's contained objects.
        if inspect.isclass(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                # Special handling for staticmethod/classmethod.
                if isinstance(val, staticmethod):
                    val = getattr(obj, valname)
                if isinstance(val, classmethod):
                    val = getattr(obj, valname).im_func

                # Recurse to methods, properties, and nested classes.
                if ((inspect.isfunction(val) or inspect.isclass(val) or
                      isinstance(val, property)) and
                      self._from_module(module, val)):
                    valname = '%s.%s' % (name, valname)
                    self._find(tests, val, valname, module, source_lines,
                               seen)

    def _get_test(self, obj, name, module, source_lines):
        """
        Return a CmdTest for the given object, if it defines a docstring;
        otherwise, return None.
        """
        # Extract the object's docstring.  If it doesn't have one,
        # then return None (no test for this object).
        if isinstance(obj, basestring):
            docstring = obj
        else:
            try:
                if obj.__doc__ is None:
                    docstring = ''
                else:
                    docstring = obj.__doc__
                    if not isinstance(docstring, basestring):
                        docstring = str(docstring)
            except (TypeError, AttributeError):
                docstring = ''

        # Find the docstring's location in the file.
        lineno = self._find_lineno(obj, source_lines)

        # Don't bother if the docstring is empty.
        if self._exclude_empty and not docstring:
            return None

        # Return a CmdTest for this object.
        if module is None:
            filename = None
        else:
            filename = getattr(module, '__file__', module.__name__)
            if filename[-4:] in (".pyc", ".pyo"):
                filename = filename[:-1]
        return self._parser.get_cmdtest(docstring, name,
                                        filename, lineno)

    def _find_lineno(self, obj, source_lines):
        """
        Return a line number of the given object's docstring.  Note:
        this method assumes that the object has a docstring.
        """
        lineno = None

        # Find the line number for modules.
        if inspect.ismodule(obj):
            lineno = 0

        # Find the line number for classes.
        # Note: this could be fooled if a class is defined multiple
        # times in a single file.
        if inspect.isclass(obj):
            if source_lines is None:
                return None
            pat = re.compile(r'^\s*class\s*%s\b' %
                             getattr(obj, '__name__', '-'))
            for i, line in enumerate(source_lines):
                if pat.match(line):
                    lineno = i
                    break

        # Find the line number for functions & methods.
        if inspect.ismethod(obj): obj = obj.im_func
        if inspect.isfunction(obj): obj = obj.func_code
        if inspect.istraceback(obj): obj = obj.tb_frame
        if inspect.isframe(obj): obj = obj.f_code
        if inspect.iscode(obj):
            lineno = getattr(obj, 'co_firstlineno', None)-1

        # Find the line number where the docstring starts.  Assume
        # that it's the first line that begins with a quote mark.
        # Note: this could be fooled by a multiline function
        # signature, where a continuation line begins with a quote
        # mark.
        if lineno is not None:
            if source_lines is None:
                return lineno+1
            pat = re.compile('(^|.*:)\s*\w*("|\')')
            for lineno in range(lineno, len(source_lines)):
                if pat.match(source_lines[lineno]):
                    return lineno

        # We couldn't find the line number.
        return None

######################################################################
## 5. CmdTest Runner
######################################################################

class CmdTestRunner:
    """
    A class used to run CmdTest test cases, and accumulate statistics.
    The `run` method is used to process a single CmdTest case.  It
    returns a tuple `(f, t)`, where `t` is the number of test cases
    tried, and `f` is the number of test cases that failed.

        TODO: this is wrong
        >>> tests = CmdTestFinder().find("foo.py")
        >>> runner = CmdTestRunner(verbose=False)
        >>> for test in tests:
        ...     print runner.run(test)
        (0, 1)
        (0, 1)

    The `summarize` method prints a summary of all the test cases that
    have been run by the runner, and returns an aggregated `(f, t)`
    tuple:

        >>> runner.summarize(verbose=1)
        2 items passed all tests:
           1 tests in foo
           1 tests in foo.bar
        2 tests in 2 items.
        2 passed and 0 failed.
        Test passed.
        (0, 2)

    The aggregated number of tried examples and failed examples is
    also available via the `tries` and `failures` attributes:

        >>> runner.tries
        2
        >>> runner.failures
        0

    The comparison between expected outputs and actual outputs is done
    by an `OutputChecker`.  This comparison may be customized with a
    number of option flags; see the documentation for `testmod` for
    more information.  If the option flags are insufficient, then the
    comparison may also be customized by passing a subclass of
    `OutputChecker` to the constructor.

    The test runner's display output can be controlled in two ways.
    First, an output function (`out`) can be passed to
    `TestRunner.run`; this function will be called with strings that
    should be displayed.  It defaults to `sys.stdout.write`.  If
    capturing the output is not sufficient, then the display output
    can be also customized by subclassing CmdTestRunner, and
    overriding the methods `report_start`, `report_success`,
    `report_unexpected_exception`, and `report_failure`.
    """
    # This divider string is used to separate failure messages, and to
    # separate sections of the summary.
    DIVIDER = "*" * 70

    def __init__(self, checker=None, verbose=None, optionflags=0):
        """
        Create a new test runner.

        Optional keyword arg `checker` is the `OutputChecker` that
        should be used to compare the expected outputs and actual
        outputs of cmdtest examples.

        Optional keyword arg 'verbose' prints lots of stuff if true,
        only failures if false; by default, it's true iff '-v' is in
        sys.argv.

        Optional argument `optionflags` can be used to control how the
        test runner compares expected output to actual output, and how
        it displays failures.  See the documentation for `testmod` for
        more information.
        """
        self._checker = checker or OutputChecker()
        if verbose is None:
            verbose = '-v' in sys.argv
        self._verbose = verbose
        self.optionflags = optionflags
        self.original_optionflags = optionflags

        # Keep track of the examples we've run.
        self.tries = 0
        self.failures = 0
        self._name2ft = {}

##        # Create a fake output target for capturing cmdtest output.
##        #TODO: probably don't need this for process running
##        self._fakeout = _SpoofOut()

    #/////////////////////////////////////////////////////////////////
    # Reporting methods
    #/////////////////////////////////////////////////////////////////

    def report_start(self, out, test, example):
        """
        Report that the test runner is about to process the given
        example.  (Only displays a message if verbose=True)
        """
        if self._verbose:
            if example.want:
                out('Trying:\n' + _indent(example.source) +
                    'Expecting:\n' + _indent(example.want))
            else:
                out('Trying:\n' + _indent(example.source) +
                    'Expecting nothing\n')

    def report_success(self, out, test, example, got):
        """
        Report that the given example ran successfully.  (Only
        displays a message if verbose=True)
        """
        if self._verbose:
            out("ok\n")

    def report_failure(self, out, test, example, got):
        """
        Report that the given example failed.
        """
        out(self._failure_header(test, example) +
            self._checker.output_difference(example, got, self.optionflags))

    def report_unexpected_exception(self, out, test, example, exc_info):
        """
        Report that the given example raised an unexpected exception.
        """
        out(self._failure_header(test, example) +
            'Exception raised:\n' + _indent(_exception_traceback(exc_info)))

    def _failure_header(self, test, example):
        out = [self.DIVIDER]
        if test.filename:
            if test.lineno is not None and example.lineno is not None:
                lineno = test.lineno + example.lineno + 1
            else:
                lineno = '?'
            out.append('File "%s", line %s, in %s' %
                       (test.filename, lineno, test.name))
        else:
            out.append('Line %s, in %s' % (example.lineno+1, test.name))
        out.append('Failed example:')
        source = example.source
        out.append(_indent(source))
        return '\n'.join(out)

    #/////////////////////////////////////////////////////////////////
    # CmdTest Running
    #/////////////////////////////////////////////////////////////////

    def __run(self, test, out):
        """
        Run the examples in `test`.  Write the outcome of each example
        with one of the `CmdTestRunner.report_*` methods, using the
        writer function `out`.  Return a tuple `(f, t)`, where `t` is
        the number of examples tried, and `f` is the number of examples
        that failed.
        """
        # Keep track of the number of failures and tries.
        failures = tries = 0

        # Save the option flags (since option directives can be used
        # to modify them).
        original_optionflags = self.optionflags

        SUCCESS, FAILURE, BOOM = range(3) # `outcome` state

        check = self._checker.check_output

        # Process each example.
        for examplenum, example in enumerate(test.examples):

            # If REPORT_ONLY_FIRST_FAILURE is set, then supress
            # reporting after the first failure.
            quiet = (self.optionflags & REPORT_ONLY_FIRST_FAILURE and
                     failures > 0)

            # Merge in the example's options.
            self.optionflags = original_optionflags
            if example.options:
                for (optionflag, val) in example.options.items():
                    if val:
                        self.optionflags |= optionflag
                    else:
                        self.optionflags &= ~optionflag

            # Record that we started this example.
            tries += 1
            if not quiet:
                self.report_start(out, test, example)

            log.debug("run %r", example)
            # - look at pexpect, Expect really *is* the right way to do
            #   this
            continue

            # Run the example in the given context (globs), and record
            # any exception that gets raised.  (But don't intercept
            # keyboard interrupts.)
            raise "TODO: this has got to change"
            try:
                # Don't blink!  This is where the user's code gets run.
                exec compile(example.source, filename, "single",
                             compileflags, 1) in test.globs
                self.debugger.set_continue() # ==== Example Finished ====
                exception = None
            except KeyboardInterrupt:
                raise
            except:
                exception = sys.exc_info()
                self.debugger.set_continue() # ==== Example Finished ====

            got = self._fakeout.getvalue()  # the actual output
            self._fakeout.truncate(0)
            outcome = FAILURE   # guilty until proved innocent or insane

            # If the example executed without raising any exceptions,
            # verify its output.
            if exception is None:
                if check(example.want, got, self.optionflags):
                    outcome = SUCCESS

            # The example raised an exception:  check if it was expected.
            else:
                exc_info = sys.exc_info()
                exc_msg = traceback.format_exception_only(*exc_info[:2])[-1]
                if not quiet:
                    got += _exception_traceback(exc_info)

                # If `example.exc_msg` is None, then we weren't expecting
                # an exception.
                if example.exc_msg is None:
                    outcome = BOOM

                # We expected an exception:  see whether it matches.
                elif check(example.exc_msg, exc_msg, self.optionflags):
                    outcome = SUCCESS

                # Another chance if they didn't care about the detail.
                elif self.optionflags & IGNORE_EXCEPTION_DETAIL:
                    m1 = re.match(r'[^:]*:', example.exc_msg)
                    m2 = re.match(r'[^:]*:', exc_msg)
                    if m1 and m2 and check(m1.group(0), m2.group(0),
                                           self.optionflags):
                        outcome = SUCCESS

            # Report the outcome.
            if outcome is SUCCESS:
                if not quiet:
                    self.report_success(out, test, example, got)
            elif outcome is FAILURE:
                if not quiet:
                    self.report_failure(out, test, example, got)
                failures += 1
            elif outcome is BOOM:
                if not quiet:
                    self.report_unexpected_exception(out, test, example,
                                                     exc_info)
                failures += 1
            else:
                assert False, ("unknown outcome", outcome)

        # Restore the option flags (in case they were modified)
        self.optionflags = original_optionflags

        # Record and return the number of failures and tries.
        self.__record_outcome(test, failures, tries)
        return failures, tries

    def __record_outcome(self, test, f, t):
        """
        Record the fact that the given CmdTest (`test`) generated `f`
        failures out of `t` tried examples.
        """
        f2, t2 = self._name2ft.get(test.name, (0,0))
        self._name2ft[test.name] = (f+f2, t+t2)
        self.failures += f
        self.tries += t

    def run(self, test, out=None):
        """
        Run the examples in `test`, and display the results using the
        writer function `out`.

        The output of each example is checked using
        `CmdTestRunner.check_output`, and the results are formatted by
        the `CmdTestRunner.report_*` methods.
        """
        return self.__run(test, out)

    #/////////////////////////////////////////////////////////////////
    # Summarization
    #/////////////////////////////////////////////////////////////////
    def summarize(self, verbose=None):
        """
        Print a summary of all the test cases that have been run by
        this CmdTestRunner, and return a tuple `(f, t)`, where `f` is
        the total number of failed examples, and `t` is the total
        number of tried examples.

        The optional `verbose` argument controls how detailed the
        summary is.  If the verbosity is not specified, then the
        CmdTestRunner's verbosity is used.
        """
        if verbose is None:
            verbose = self._verbose
        notests = []
        passed = []
        failed = []
        totalt = totalf = 0
        for x in self._name2ft.items():
            name, (f, t) = x
            assert f <= t
            totalt += t
            totalf += f
            if t == 0:
                notests.append(name)
            elif f == 0:
                passed.append( (name, t) )
            else:
                failed.append(x)
        if verbose:
            if notests:
                print len(notests), "items had no tests:"
                notests.sort()
                for thing in notests:
                    print "   ", thing
            if passed:
                print len(passed), "items passed all tests:"
                passed.sort()
                for thing, count in passed:
                    print " %3d tests in %s" % (count, thing)
        if failed:
            print self.DIVIDER
            print len(failed), "items had failures:"
            failed.sort()
            for thing, (f, t) in failed:
                print " %3d of %3d in %s" % (f, t, thing)
        if verbose:
            print totalt, "tests in", len(self._name2ft), "items."
            print totalt - totalf, "passed and", totalf, "failed."
        if totalf:
            print "***Test Failed***", totalf, "failures."
        elif verbose:
            print "Test passed."
        return totalf, totalt

    #/////////////////////////////////////////////////////////////////
    # Backward compatibility cruft to maintain cmdtest.master.
    #/////////////////////////////////////////////////////////////////
    #TODO: drop this?
    def merge(self, other):
        d = self._name2ft
        for name, (f, t) in other._name2ft.items():
            if name in d:
                print "*** CmdTestRunner.merge: '" + name + "' in both" \
                    " testers; summing outcomes."
                f2, t2 = d[name]
                f = f + f2
                t = t + t2
            d[name] = f, t

class OutputChecker:
    """
    A class used to check whether the actual output from a cmdtest
    example matches the expected output.  `OutputChecker` defines two
    methods: `check_output`, which compares a given pair of outputs,
    and returns true if they match; and `output_difference`, which
    returns a string describing the differences between two outputs.
    """
    def check_output(self, want, got, optionflags):
        """
        Return True iff the actual output from an example (`got`)
        matches the expected output (`want`).  These strings are
        always considered to match if they are identical; but
        depending on what option flags the test runner is using,
        several non-exact match types are also possible.  See the
        documentation for `TestRunner` for more information about
        option flags.
        """
        # Handle the common case first, for efficiency:
        # if they're string-identical, always return true.
        if got == want:
            return True

        # The values True and False replaced 1 and 0 as the return
        # value for boolean comparisons in Python 2.3.
        if not (optionflags & DONT_ACCEPT_TRUE_FOR_1):
            if (got,want) == ("True\n", "1\n"):
                return True
            if (got,want) == ("False\n", "0\n"):
                return True

        # <BLANKLINE> can be used as a special sequence to signify a
        # blank line, unless the DONT_ACCEPT_BLANKLINE flag is used.
        if not (optionflags & DONT_ACCEPT_BLANKLINE):
            # Replace <BLANKLINE> in want with a blank line.
            want = re.sub('(?m)^%s\s*?$' % re.escape(BLANKLINE_MARKER),
                          '', want)
            # If a line in got contains only spaces, then remove the
            # spaces.
            got = re.sub('(?m)^\s*?$', '', got)
            if got == want:
                return True

        # This flag causes cmdtest to ignore any differences in the
        # contents of whitespace strings.  Note that this can be used
        # in conjunction with the ELLIPSIS flag.
        if optionflags & NORMALIZE_WHITESPACE:
            got = ' '.join(got.split())
            want = ' '.join(want.split())
            if got == want:
                return True

        # The ELLIPSIS flag says to let the sequence "..." in `want`
        # match any substring in `got`.
        if optionflags & ELLIPSIS:
            if _ellipsis_match(want, got):
                return True

        # We didn't find any match; return false.
        return False

    # Should we do a fancy diff?
    def _do_a_fancy_diff(self, want, got, optionflags):
        # Not unless they asked for a fancy diff.
        if not optionflags & (REPORT_UDIFF |
                              REPORT_CDIFF |
                              REPORT_NDIFF):
            return False

        # If expected output uses ellipsis, a meaningful fancy diff is
        # too hard ... or maybe not.  In two real-life failures Tim saw,
        # a diff was a major help anyway, so this is commented out.
        # [todo] _ellipsis_match() knows which pieces do and don't match,
        # and could be the basis for a kick-ass diff in this case.
        ##if optionflags & ELLIPSIS and ELLIPSIS_MARKER in want:
        ##    return False

        # ndiff does intraline difference marking, so can be useful even
        # for 1-line differences.
        if optionflags & REPORT_NDIFF:
            return True

        # The other diff types need at least a few lines to be helpful.
        return want.count('\n') > 2 and got.count('\n') > 2

    def output_difference(self, example, got, optionflags):
        """
        Return a string describing the differences between the
        expected output for a given example (`example`) and the actual
        output (`got`).  `optionflags` is the set of option flags used
        to compare `want` and `got`.
        """
        want = example.want
        # If <BLANKLINE>s are being used, then replace blank lines
        # with <BLANKLINE> in the actual output string.
        if not (optionflags & DONT_ACCEPT_BLANKLINE):
            got = re.sub('(?m)^[ ]*(?=\n)', BLANKLINE_MARKER, got)

        # Check if we should use diff.
        if self._do_a_fancy_diff(want, got, optionflags):
            # Split want & got into lines.
            want_lines = want.splitlines(True)  # True == keep line ends
            got_lines = got.splitlines(True)
            # Use difflib to find their differences.
            if optionflags & REPORT_UDIFF:
                diff = difflib.unified_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:] # strip the diff header
                kind = 'unified diff with -expected +actual'
            elif optionflags & REPORT_CDIFF:
                diff = difflib.context_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:] # strip the diff header
                kind = 'context diff with expected followed by actual'
            elif optionflags & REPORT_NDIFF:
                engine = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK)
                diff = list(engine.compare(want_lines, got_lines))
                kind = 'ndiff with -expected +actual'
            else:
                assert 0, 'Bad diff option'
            # Remove trailing whitespace on diff output.
            diff = [line.rstrip() + '\n' for line in diff]
            return 'Differences (%s):\n' % kind + _indent(''.join(diff))

        # If we're not using diff, then simply list the expected
        # output followed by the actual output.
        if want and got:
            return 'Expected:\n%sGot:\n%s' % (_indent(want), _indent(got))
        elif want:
            return 'Expected:\n%sGot nothing\n' % _indent(want)
        elif got:
            return 'Expected nothing\nGot:\n%s' % _indent(got)
        else:
            return 'Expected nothing\nGot nothing\n'

class CmdTestError(Exception):
    """base cmdtest exception class"""
    pass 

class CmdTestFailure(CmdTestError):
    """A CmdTest example has failed in debugging mode.

    The exception instance has variables:

    - test: the CmdTest object being run

    - example: the Example object that failed

    - got: the actual output
    """
    def __init__(self, test, example, got):
        self.test = test
        self.example = example
        self.got = got

    def __str__(self):
        return str(self.test)

class UnexpectedException(CmdTestError):
    """A CmdTest example has encountered an unexpected exception

    The exception instance has variables:

    - test: the CmdTest object being run

    - example: the Example object that failed

    - exc_info: the exception info
    """
    def __init__(self, test, example, exc_info):
        self.test = test
        self.example = example
        self.exc_info = exc_info

    def __str__(self):
        return str(self.test)

class DebugRunner(CmdTestRunner):
    r"""Run doc tests but raise an exception as soon as there is a failure.

       If an unexpected exception occurs, an UnexpectedException is raised.
       It contains the test, the example, and the original exception:

         >>> runner = DebugRunner(verbose=False)
         >>> test = CmdTestParser().get_cmdtest('>>> raise KeyError\n42',
         ...                                    'foo', 'foo.py', 0)
         >>> try:
         ...     runner.run(test)
         ... except UnexpectedException, failure:
         ...     pass

         >>> failure.test is test
         True

         >>> failure.example.want
         '42\n'

         >>> exc_info = failure.exc_info
         >>> raise exc_info[0], exc_info[1], exc_info[2]
         Traceback (most recent call last):
         ...
         KeyError

       We wrap the original exception to give the calling application
       access to the test and example information.

       If the output doesn't match, then a CmdTestFailure is raised:

         >>> test = CmdTestParser().get_cmdtest('''
         ...      >>> x = 1
         ...      >>> x
         ...      2
         ...      ''', 'foo', 'foo.py', 0)

         >>> try:
         ...    runner.run(test)
         ... except CmdTestFailure, failure:
         ...    pass

       CmdTestFailure objects provide access to the test:

         >>> failure.test is test
         True

       As well as to the example:

         >>> failure.example.want
         '2\n'

       and the actual output:

         >>> failure.got
         '1\n'

       If a failure or error occurs, the globals are left intact:

         >>> del test.globs['__builtins__']
         >>> test.globs
         {'x': 1}

         >>> test = CmdTestParser().get_cmdtest('''
         ...      >>> x = 2
         ...      >>> raise KeyError
         ...      ''', 'foo', 'foo.py', 0)

         >>> runner.run(test)
         Traceback (most recent call last):
         ...
         UnexpectedException: <CmdTest foo from foo.py:0 (2 examples)>

         >>> del test.globs['__builtins__']
         >>> test.globs
         {'x': 2}

       But the globals are cleared if there is no error:

         >>> test = CmdTestParser().get_cmdtest('''
         ...      >>> x = 2
         ...      ''', 'foo', 'foo.py', 0)

         >>> runner.run(test)
         (0, 1)

         >>> test.globs
         {}

       """

    def run(self, test, compileflags=None, out=None):
        r = CmdTestRunner.run(self, test, compileflags, out, False)
        return r

    def report_unexpected_exception(self, out, test, example, exc_info):
        raise UnexpectedException(test, example, exc_info)

    def report_failure(self, out, test, example, got):
        raise CmdTestFailure(test, example, got)

######################################################################
## 6. Test Functions
######################################################################
# These should be backwards compatible.

# For backward compatibility, a global instance of a CmdTestRunner
# class, updated by testmod.
master = None

#TODO: drop testmod?
def testmod(m=None, name=None, globs=None, verbose=None,
            report=True, optionflags=0, extraglobs=None,
            raise_on_error=False, exclude_empty=False):
    """m=None, name=None, globs=None, verbose=None,
       report=True, optionflags=0, extraglobs=None, raise_on_error=False,
       exclude_empty=False

    Test examples in docstrings in functions and classes reachable
    from module m (or the current module if m is not supplied), starting
    with m.__doc__.

    Also test examples reachable from dict m.__test__ if it exists and is
    not None.  m.__test__ maps names to functions, classes and strings;
    function and class docstrings are tested even if the name is private;
    strings are tested directly, as if they were docstrings.

    Return (#failures, #tests).

    See cmdtest.__doc__ for an overview.

    Optional keyword arg "name" gives the name of the module; by default
    use m.__name__.

    Optional keyword arg "globs" gives a dict to be used as the globals
    when executing examples; by default, use m.__dict__.  A copy of this
    dict is actually used for each docstring, so that each docstring's
    examples start with a clean slate.

    Optional keyword arg "extraglobs" gives a dictionary that should be
    merged into the globals that are used to execute examples.  By
    default, no extra globals are used.

    Optional keyword arg "verbose" prints lots of stuff if true, prints
    only failures if false; by default, it's true iff "-v" is in sys.argv.

    Optional keyword arg "report" prints a summary at the end when true,
    else prints nothing at the end.  In verbose mode, the summary is
    detailed, else very brief (in fact, empty if all tests passed).

    Optional keyword arg "optionflags" or's together module constants,
    and defaults to 0.  Possible values (see the docs for details):

        DONT_ACCEPT_TRUE_FOR_1
        DONT_ACCEPT_BLANKLINE
        NORMALIZE_WHITESPACE
        ELLIPSIS
        IGNORE_EXCEPTION_DETAIL
        REPORT_UDIFF
        REPORT_CDIFF
        REPORT_NDIFF
        REPORT_ONLY_FIRST_FAILURE

    Optional keyword arg "raise_on_error" raises an exception on the
    first unexpected exception or failure. This allows failures to be
    post-mortem debugged.

    Advanced tomfoolery:  testmod runs methods of a local instance of
    class cmdtest.Tester, then merges the results into (or creates)
    global Tester instance cmdtest.master.  Methods of cmdtest.master
    can be called directly too, if you want to do something unusual.
    Passing report=0 to testmod is especially useful then, to delay
    displaying a summary.  Invoke cmdtest.master.summarize(verbose)
    when you're done fiddling.
    """
    global master

    # If no module was given, then use __main__.
    if m is None:
        # DWA - m will still be None if this wasn't invoked from the command
        # line, in which case the following TypeError is about as good an error
        # as we should expect
        m = sys.modules.get('__main__')

    # Check that we were actually given a module.
    if not inspect.ismodule(m):
        raise TypeError("testmod: module required; %r" % (m,))

    # If no name was given, then use the module's name.
    if name is None:
        name = m.__name__

    # Find, parse, and run all tests in the given module.
    finder = CmdTestFinder(exclude_empty=exclude_empty)

    if raise_on_error:
        runner = DebugRunner(verbose=verbose, optionflags=optionflags)
    else:
        runner = CmdTestRunner(verbose=verbose, optionflags=optionflags)

    for test in finder.find(m, name, globs=globs, extraglobs=extraglobs):
        runner.run(test)

    if report:
        runner.summarize()

    if master is None:
        master = runner
    else:
        master.merge(runner)

    return runner.failures, runner.tries

##def testfile(filename, module_relative=True, name=None, package=None,
##             globs=None, verbose=None, report=True, optionflags=0,
##             extraglobs=None, raise_on_error=False, parser=CmdTestParser()):
##    """
##    Test examples in the given file.  Return (#failures, #tests).
##
##    Optional keyword arg "module_relative" specifies how filenames
##    should be interpreted:
##
##      - If "module_relative" is True (the default), then "filename"
##         specifies a module-relative path.  By default, this path is
##         relative to the calling module's directory; but if the
##         "package" argument is specified, then it is relative to that
##         package.  To ensure os-independence, "filename" should use
##         "/" characters to separate path segments, and should not
##         be an absolute path (i.e., it may not begin with "/").
##
##      - If "module_relative" is False, then "filename" specifies an
##        os-specific path.  The path may be absolute or relative (to
##        the current working directory).
##
##    Optional keyword arg "name" gives the name of the test; by default
##    use the file's basename.
##
##    Optional keyword argument "package" is a Python package or the
##    name of a Python package whose directory should be used as the
##    base directory for a module relative filename.  If no package is
##    specified, then the calling module's directory is used as the base
##    directory for module relative filenames.  It is an error to
##    specify "package" if "module_relative" is False.
##
##    Optional keyword arg "globs" gives a dict to be used as the globals
##    when executing examples; by default, use {}.  A copy of this dict
##    is actually used for each docstring, so that each docstring's
##    examples start with a clean slate.
##
##    Optional keyword arg "extraglobs" gives a dictionary that should be
##    merged into the globals that are used to execute examples.  By
##    default, no extra globals are used.
##
##    Optional keyword arg "verbose" prints lots of stuff if true, prints
##    only failures if false; by default, it's true iff "-v" is in sys.argv.
##
##    Optional keyword arg "report" prints a summary at the end when true,
##    else prints nothing at the end.  In verbose mode, the summary is
##    detailed, else very brief (in fact, empty if all tests passed).
##
##    Optional keyword arg "optionflags" or's together module constants,
##    and defaults to 0.  Possible values (see the docs for details):
##
##        DONT_ACCEPT_TRUE_FOR_1
##        DONT_ACCEPT_BLANKLINE
##        NORMALIZE_WHITESPACE
##        ELLIPSIS
##        IGNORE_EXCEPTION_DETAIL
##        REPORT_UDIFF
##        REPORT_CDIFF
##        REPORT_NDIFF
##        REPORT_ONLY_FIRST_FAILURE
##
##    Optional keyword arg "raise_on_error" raises an exception on the
##    first unexpected exception or failure. This allows failures to be
##    post-mortem debugged.
##
##    Optional keyword arg "parser" specifies a CmdTestParser (or
##    subclass) that should be used to extract tests from the files.
##
##    Advanced tomfoolery:  testmod runs methods of a local instance of
##    class cmdtest.Tester, then merges the results into (or creates)
##    global Tester instance cmdtest.master.  Methods of cmdtest.master
##    can be called directly too, if you want to do something unusual.
##    Passing report=0 to testmod is especially useful then, to delay
##    displaying a summary.  Invoke cmdtest.master.summarize(verbose)
##    when you're done fiddling.
##    """
##    global master
##
##    if package and not module_relative:
##        raise ValueError("Package may only be specified for module-"
##                         "relative paths.")
##
##    # Relativize the path
##    if module_relative:
##        package = _normalize_module(package)
##        filename = _module_relative_path(package, filename)
##
##    # If no name was given, then use the file's name.
##    if name is None:
##        name = os.path.basename(filename)
##
##    # Assemble the globals.
##    if globs is None:
##        globs = {}
##    else:
##        globs = globs.copy()
##    if extraglobs is not None:
##        globs.update(extraglobs)
##
##    if raise_on_error:
##        runner = DebugRunner(verbose=verbose, optionflags=optionflags)
##    else:
##        runner = CmdTestRunner(verbose=verbose, optionflags=optionflags)
##
##    # Read the file, convert it to a test, and run it.
##    s = open(filename).read()
##    test = parser.get_cmdtest(s, name, filename, 0)
##    runner.run(test)
##
##    if report:
##        runner.summarize()
##
##    if master is None:
##        master = runner
##    else:
##        master.merge(runner)
##
##    return runner.failures, runner.tries


######################################################################
## 8. Unittest Support
######################################################################

_unittest_reportflags = 0

def set_unittest_reportflags(flags):
    """Sets the unittest option flags.

    The old flag is returned so that a runner could restore the old
    value if it wished to:

      >>> import cmdtest
      >>> old = cmdtest._unittest_reportflags
      >>> cmdtest.set_unittest_reportflags(REPORT_NDIFF |
      ...                          REPORT_ONLY_FIRST_FAILURE) == old
      True

      >>> cmdtest._unittest_reportflags == (REPORT_NDIFF |
      ...                                   REPORT_ONLY_FIRST_FAILURE)
      True

    Only reporting flags can be set:

      >>> cmdtest.set_unittest_reportflags(ELLIPSIS)
      Traceback (most recent call last):
      ...
      ValueError: ('Only reporting flags allowed', 8)

      >>> cmdtest.set_unittest_reportflags(old) == (REPORT_NDIFF |
      ...                                   REPORT_ONLY_FIRST_FAILURE)
      True
    """
    global _unittest_reportflags

    if (flags & REPORTING_FLAGS) != flags:
        raise ValueError("Only reporting flags allowed", flags)
    old = _unittest_reportflags
    _unittest_reportflags = flags
    return old


class CmdTestCase(unittest.TestCase):
    def __init__(self, test, optionflags=0, setUp=None, tearDown=None,
                 checker=None):
        unittest.TestCase.__init__(self)
        self._ct_optionflags = optionflags
        self._ct_checker = checker
        self._ct_test = test
        self._ct_setUp = setUp
        self._ct_tearDown = tearDown

    def setUp(self):
        test = self._ct_test

        if self._ct_setUp is not None:
            self._ct_setUp(test)

    def tearDown(self):
        test = self._ct_test

        if self._ct_tearDown is not None:
            self._ct_tearDown(test)

    def runTest(self):
        test = self._ct_test
        old = sys.stdout
        new = StringIO()
        optionflags = self._ct_optionflags

        if not (optionflags & REPORTING_FLAGS):
            # The option flags don't include any reporting flags,
            # so add the default reporting flags
            optionflags |= _unittest_reportflags

        runner = CmdTestRunner(optionflags=optionflags,
                               checker=self._ct_checker, verbose=False)

        try:
            runner.DIVIDER = "-"*70
            failures, tries = runner.run(test, out=new.write)
        finally:
            sys.stdout = old

        if failures:
            raise self.failureException(self.format_failure(new.getvalue()))

    def format_failure(self, err):
        test = self._ct_test
        if test.lineno is None:
            lineno = 'unknown line number'
        else:
            lineno = '%s' % test.lineno
        lname = '.'.join(test.name.split('.')[-1:])
        return ('Failed cmdtest test for %s\n'
                '  File "%s", line %s, in %s\n\n%s'
                % (test.name, test.filename, lineno, lname, err)
                )

    def debug(self):
        r"""Run the test case without results and without catching exceptions

           The unit test framework includes a debug method on test cases
           and test suites to support post-mortem debugging.  The test code
           is run in such a way that errors are not caught.  This way a
           caller can catch the errors and initiate post-mortem debugging.

           The CmdTestCase provides a debug method that raises
           UnexpectedException errors if there is an unexepcted
           exception:

             >>> test = CmdTestParser().get_cmdtest('>>> raise KeyError\n42',
             ...                'foo', 'foo.py', 0)
             >>> case = CmdTestCase(test)
             >>> try:
             ...     case.debug()
             ... except UnexpectedException, failure:
             ...     pass

           The UnexpectedException contains the test, the example, and
           the original exception:

             >>> failure.test is test
             True

             >>> failure.example.want
             '42\n'

             >>> exc_info = failure.exc_info
             >>> raise exc_info[0], exc_info[1], exc_info[2]
             Traceback (most recent call last):
             ...
             KeyError

           If the output doesn't match, then a CmdTestFailure is raised:

             >>> test = CmdTestParser().get_cmdtest('''
             ...      >>> x = 1
             ...      >>> x
             ...      2
             ...      ''', 'foo', 'foo.py', 0)
             >>> case = CmdTestCase(test)

             >>> try:
             ...    case.debug()
             ... except CmdTestFailure, failure:
             ...    pass

           CmdTestFailure objects provide access to the test:

             >>> failure.test is test
             True

           As well as to the example:

             >>> failure.example.want
             '2\n'

           and the actual output:

             >>> failure.got
             '1\n'

           """

        self.setUp()
        runner = DebugRunner(optionflags=self._ct_optionflags,
                             checker=self._ct_checker, verbose=False)
        runner.run(self._ct_test)
        self.tearDown()

    def id(self):
        return self._ct_test.name

    def __repr__(self):
        name = self._ct_test.name.split('.')
        return "%s (%s)" % (name[-1], '.'.join(name[:-1]))

    __str__ = __repr__

    def shortDescription(self):
        return "Cmdtest: " + self._ct_test.name

#TODO: add 'env' and 'cwd' optional arguments
def CmdTestSuite(files, test_finder=None, **options):
    """
    Convert cmdtest tests for a Python script (or set of scripts) to a
    unittest test suite.

    This converts each documentation string in the Python script(s) that
    contains cmdtest tests to a unittest test case.  If any of the
    tests in a doc string fail, then the test case fails.  An exception
    is raised showing the name of the file containing the test and a
    (sometimes approximate) line number.

    The `files` argument is a path to a Python script or an iterable
    of script paths.

    A number of options may be provided as keyword arguments:

    setUp
      A set-up function.  This is called before running the
      tests in each file. The setUp function will be passed a CmdTest
      object.  The setUp function can access the test globals as the
      globs attribute of the test passed.

    tearDown
      A tear-down function.  This is called after running the
      tests in each file.  The tearDown function will be passed a CmdTest
      object.  The tearDown function can access the test globals as the
      globs attribute of the test passed.

    optionflags
       A set of cmdtest option flags expressed as an integer.
    """
    if isinstance(files, basestring):
        files = [file]
    if test_finder is None:
        test_finder = CmdTestFinder()

    alltests = []
    for file in files:
        #TODO: pass 'env' and 'cwd' through here
        tests = test_finder.find(file)
        if not tests:
            # Why do we want to do this? Because it reveals a bug that
            # might otherwise be hidden.
            raise ValueError(file, "has no cmdtests")
        alltests += [(file, t) for t in tests]

    alltests.sort()
    suite = unittest.TestSuite()
    for file, test in alltests:
        if len(test.examples) == 0:
            continue
        suite.addTest(CmdTestCase(test, **options))

    return suite

#TODO: want to allow these? The name "CmdFile" is confusing: it is meant
#      to be a file that is not a Python script that just has test cases
#      in it.
##class CmdFileCase(CmdTestCase):
##
##    def id(self):
##        return '_'.join(self._ct_test.name.split('.'))
##
##    def __repr__(self):
##        return self._ct_test.filename
##    __str__ = __repr__
##
##    def format_failure(self, err):
##        return ('Failed cmdtest test for %s\n  File "%s", line 0\n\n%s'
##                % (self._ct_test.name, self._ct_test.filename, err)
##                )
##
##def CmdFileTest(path, module_relative=True, package=None,
##                parser=CmdTestParser(), **options):
##    if package and not module_relative:
##        raise ValueError("Package may only be specified for module-"
##                         "relative paths.")
##
##    # Relativize the path.
##    if module_relative:
##        package = _normalize_module(package)
##        path = _module_relative_path(package, path)
##
##    # Find the file and read it.
##    name = os.path.basename(path)
##    doc = open(path).read()
##
##    # Convert it to a test, and wrap it in a CmdFileCase.
##    test = parser.get_cmdtest(doc, name, path, 0)
##    return CmdFileCase(test, **options)
##
##def CmdFileSuite(*paths, **kw):
##    """A unittest suite for one or more cmdtest files.
##
##    The path to each cmdtest file is given as a string; the
##    interpretation of that string depends on the keyword argument
##    "module_relative".
##
##    A number of options may be provided as keyword arguments:
##
##    module_relative
##      If "module_relative" is True, then the given file paths are
##      interpreted as os-independent module-relative paths.  By
##      default, these paths are relative to the calling module's
##      directory; but if the "package" argument is specified, then
##      they are relative to that package.  To ensure os-independence,
##      "filename" should use "/" characters to separate path
##      segments, and may not be an absolute path (i.e., it may not
##      begin with "/").
##
##      If "module_relative" is False, then the given file paths are
##      interpreted as os-specific paths.  These paths may be absolute
##      or relative (to the current working directory).
##
##    package
##      A Python package or the name of a Python package whose directory
##      should be used as the base directory for module relative paths.
##      If "package" is not specified, then the calling module's
##      directory is used as the base directory for module relative
##      filenames.  It is an error to specify "package" if
##      "module_relative" is False.
##
##    setUp
##      A set-up function.  This is called before running the
##      tests in each file. The setUp function will be passed a CmdTest
##      object.  The setUp function can access the test globals as the
##      globs attribute of the test passed.
##
##    tearDown
##      A tear-down function.  This is called after running the
##      tests in each file.  The tearDown function will be passed a CmdTest
##      object.  The tearDown function can access the test globals as the
##      globs attribute of the test passed.
##
##    optionflags
##      A set of cmdtest option flags expressed as an integer.
##
##    parser
##      A CmdTestParser (or subclass) that should be used to extract
##      tests from the files.
##    """
##    suite = unittest.TestSuite()
##
##    # We do this here so that _normalize_module is called at the right
##    # level.  If it were called in CmdFileTest, then this function
##    # would be the caller and we might guess the package incorrectly.
##    if kw.get('module_relative', True):
##        kw['package'] = _normalize_module(kw.get('package'))
##
##    for path in paths:
##        suite.addTest(CmdFileTest(path, **kw))
##
##    return suite


######################################################################
## 9. Mainline
######################################################################

# STARTHERE:
# - currently working through:
#       python cmdtest.py test_helloworld.py
#   starting at "STARTHERE"
# - come up with a basic plan and test to work my way through
# - write the first process handling
# - write some test cases and finish this (NOT based on Expect)
# - use it for cmdln.py
#

log = logging.getLogger("cmdtest")

def cmdtest(files):
    log.debug("cmdtest(files=%s)", files)
    r = unittest.TextTestRunner()
    suite = CmdTestSuite(files)
    r.run(suite)
    

def main(argv):
    log.setLevel(logging.INFO)
    
    # Process command line.
    try:
        optlist, args = getopt.getopt(argv[1:], "hVvq",
            ["help", "version", "verbose", "quiet"])
    except getopt.GetoptError, ex:
        raise Error(str(ex))
    for opt, optarg in optlist:
        #TODO: should perhaps have -d (logging DEBUG) option to separate
        #      verbose debugging output and verbose testing output
        if opt in ("-h", "--help"):
            sys.stdout.write(__doc__)
            return 0
        elif opt in ("-V", "--version"):
            ver = '.'.join(map(str, __version_info__))
            print "cmdtest %s" % ver
            return 0
        elif opt in ("-v", "--verbose"):
            log.setLevel(logging.DEBUG)
        elif opt in ("-q", "--quiet"):
            log.setLevel(logging.WARN)

    files = []
    for pattern in args:
        if sys.platform == "win32":
            files += glob.glob(pattern)
        else:
            files.append(pattern)
    if sys.platform == "win32" and not files:
        log.warn("no files found matching '%s'", "', '".join(args))
    return cmdtest(files)


if __name__ == "__main__":
    if sys.version_info[:2] <= (2,2): __file__ = sys.argv[0]
    logging.basicConfig()
    try:
        retval = main(sys.argv)
    except KeyboardInterrupt:
        sys.exit(1)
    except SystemExit:
        raise
    except:
        exc_info = sys.exc_info()
        if log.isEnabledFor(logging.DEBUG):
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



