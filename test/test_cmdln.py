#!/usr/bin/env python
# Copyright (c) 2005 Trent Mick
# License: MIT License

"""Test specially formated cmdln_*.py files

Each cmdln_*.py implemented a cmdln.Cmdln subclass and its module
docstring is an 'expect' script to test running it.

Usage:
    Run all cmdln_*.py tests:
        python test_cmdln.py

    As part of a large test suite:
        import test_cmdln
        test_cmdln.suite() # returns a unittest.TestSuite

    Test just specified cmdln_* files:
        python test_cmdln.py <file-pattern>...

"""

import sys
import os
import unittest
import difflib
import pprint
import shutil
import glob


PY3 = sys.version_info[0] == 3




#---- support stuff

def banner(text, ch='=', length=78):
    """Return a banner line centering the given text.

        "text" is the text to show in the banner. None can be given to have
            no text.
        "ch" (optional, default '=') is the banner line character (can
            also be a short string to repeat).
        "length" (optional, default 78) is the length of banner to make.

    Examples:
        >>> banner("Peggy Sue")
        '================================= Peggy Sue =================================='
        >>> banner("Peggy Sue", ch='-', length=50)
        '------------------- Peggy Sue --------------------'
        >>> banner("Pretty pretty pretty pretty Peggy Sue", length=40)
        'Pretty pretty pretty pretty Peggy Sue'
    """
    if text is None:
        return ch * length
    elif len(text) + 2 + len(ch)*2 > length:
        # Not enough space for even one line char (plus space) around text.
        return text
    else:
        remain = length - (len(text) + 2)
        prefix_len = remain / 2
        suffix_len = remain - prefix_len
        if len(ch) == 1:
            prefix = ch * prefix_len
            suffix = ch * suffix_len
        else:
            prefix = ch * (prefix_len/len(ch)) + ch[:prefix_len%len(ch)]
            suffix = ch * (suffix_len/len(ch)) + ch[:suffix_len%len(ch)]
        return prefix + ' ' + text + ' ' + suffix

def indented(text, indent=' '*4):
    lines = text.splitlines(1)
    return indent + indent.join(lines)


#---- Expect shorthand to expect translation

SHELL_PROMPT = "$ "

class SpawnBlock:
    def __init__(self, spawnline):
        self._parse(spawnline) # sets self.cmd and self.options
        self.lines = []

    def _parse(self, line):
        self.options = {}
        parts = line[len(SHELL_PROMPT):].split("#", 1)
        if len(parts) == 1:
            self.cmd = parts[0]
        else:
            self.cmd, optstr = parts
            landmark = "expecttest:"
            if optstr.startswith(landmark):
                for opt in optstr[len(landmark):].split(","):
                    opt = opt.strip()
                    if '=' in opt:
                        name, value = opt.split('=')
                        if value.startswith('"'):
                            value = value[1:-1]
                    else:
                        name, value = opt, True
                    self.options[name] = value

    def addline(self, line):
        self.lines.append(line)

    def generate(self):
        """Return executable "expect" code for this spawn-block."""
        expect = ["spawn "+self.cmd]
        interactive = self.options.get("INTERACTIVE", False)
        if interactive:
            prompt = self.options["PROMPT"]
        if sys.platform == "win32":
            eol_expect = r"\n"
            eol_expect_repr = r"\\n"
            eof_expect = r"\032\r" # Ctrl-Z + return
        else:
            eol_expect = r"\r\n"
            eol_expect_repr = r"\\r\\n"
            eof_expect = r"\004" # Ctrl-D

        for line in self.lines:
            if interactive and line.startswith(prompt):
                expect.append(r"""expect {
    -i $spawn_id
    -re "^%s" {}
    default {
        puts stderr {ERROR: expected "%s"}
        puts stderr "       got      \"$expect_out(buffer)\""
        exit 1
    }
}""" % (prompt, prompt))
                input = line[len(prompt):]
                if input in ("^D", "^Z"):
                    #XXX Around the post-10.4 (Tiger) OS X release
                    #    updates for 10.3 this 'expect' started failing.
                    #    Adding the "(....)?" helps. I don't know enough
                    #    Tcl to figure out exactly what those friggin'
                    #    chars are.
                    expect += [r'send "%s"' % eof_expect,
                               r'expect -re "^(....)?%s$"' % eol_expect]
                else:
                    expect += [r'send "%s\r"' % input,
                               r'expect -re "^%s%s"' % (input, eol_expect)]
            else:
                expected = tcl_escape(line)
                if line == "<BLANKLINE>":
                    expected = r"\s*" # a "blank line" can have whitespace
                expect.append(r"""expect {
    -i $spawn_id
    -re {^%s%s} {}
    default {
        puts stderr {ERROR: expected "%s%s"}
        puts stderr "       got      \"$expect_out(buffer)\""
        exit 1
    }
}""" % (expected,
        eol_expect,
        expected.replace('\\', ''),
        eol_expect_repr))

        # Trap EOF for current process and make sure there isn't
        # unexpected trailing output.
        expect.append(r"""expect {
    -i $spawn_id
    eof {
    } -re "^.+$" {
        puts stderr "error: unexpected trailing output: '$expect_out(buffer)'\n"
        exit 1
    } timeout {
        puts stderr {ERROR: timed out waiting for EOF from '%s'}
        exit 1
    }
}""" % self.cmd)

        return '\n'.join(expect)

def tcl_escape(s):
    """Escape the given string as appropriate for using in a Tcl string
    and regex.
    """
    return s.replace("[", "\\[").replace("]", "\\]") \
            .replace("$", "\\$") \
            .replace("?", "\\?") \
            .replace("(", "\\(").replace(")", "\\)")

def strip_prefix(line, prefix):
    junk, content = line[:len(prefix)], line[len(prefix):].rstrip()
    if junk.strip(): # line in block with short indentation
        raise ValueError("too-short indentation on line: '%s'"
                         % line)
    assert '\t' not in junk, \
           "error: tab in expect-line prefix: '%s'" % line
    return content

def parse_expect_content(content):
    """Generate parsed "expect" lines.

    "Expect" blocks begin with a "spawn" line -- one that is prefixed
    with a shell prompt -- and end with a blank line or the end of the
    content. A "parsed" line is one with the indentation removed, if
    any.

    Generates 2-tuples
        (<line-type>, <parsed-line>)
    where <line-type> is "spawn" for spawn-lines or "other" for other
    lines.
    """
    if not content:
        raise StopIteration
    prefix = None
    for line in content.splitlines(0):
        if not line.strip():
            prefix = None # end of a block
        elif line.lstrip().startswith(SHELL_PROMPT):
            if prefix is None: # start of a new block
                idx = line.index(SHELL_PROMPT)
                prefix, content = line[:idx], line[idx:].rstrip()
                assert '\t' not in prefix, \
                       "error: tab in expect-line prefix: '%s'" % line
            else:
                content = strip_prefix(line, prefix)
            yield "spawn", content
        elif prefix is not None:
            yield "other", strip_prefix(line, prefix)

def generate_expect(content):
    # Break into "spawn"-block. A new spawn block starts with what
    # will become an expect "spawn" command. Specifically a block
    # that begins with the '$ ' shell prompt.
    blocks = []
    block = None
    for type, line in parse_expect_content(content):
        assert type in ("spawn", "other"), \
               "unexpected spawn line type: %r" % type
        if type == "spawn":
            block = SpawnBlock(line)
            blocks.append(block)
        else:
            assert block is not None, \
                   "'other' spawn line without leading 'spawn' line: %r" % line
            block.addline(line)

    expect = ["#!/usr/bin/env tclsh",
              "",
              "package require Expect",
              "set timeout 3",
              "set send_slow {10 .001}",
              ""]
    for block in blocks:
        expect.append(block.generate())
    return '\n'.join(expect) + '\n'


#----- test cases

class CmdlnTestCase(unittest.TestCase):
    pass

def _testOneCmdln(self, modname, fname):
    _debug = False  # Set to true to dump status info for each test run.

    mod = __import__(modname)
    doc = mod.__doc__
    if not PY3 and isinstance(doc, unicode):
        doc = doc.encode("utf-8")
    expect = generate_expect(doc)
    if False:
        tmpfname = ".%s.exp.tmp" % modname
        open(tmpfname, 'w').write(expect)
        retval = os.system("tclsh "+tmpfname)
        if hasattr(os, "WEXITSTATUS"):
            retval = os.WEXITSTATUS(retval)
        stdout = stderr = ""
    else:
        if _debug:
            tmpfname = ".%s.exp.tmp" % modname
            open(tmpfname, 'w').write(expect)
        import process
        p = process.ProcessOpen("tclsh")
        p.stdin.write(expect)
        p.stdin.close()
        retval = p.wait()
        if hasattr(os, "WEXITSTATUS"):
            retval = os.WEXITSTATUS(retval)
        stdout = p.stdout.read()
        stderr = p.stderr.read()
        p.close()
    self.failIf(retval, """\
'%s' did not behave as expected:
%s
%s
%s
%s
%s
%s
%s""" % (fname,
         indented(banner("expect shorthand", length=72)),
         indented(doc or ""),
         indented(banner("stdout", length=72)),
         indented(stdout),
         indented(banner("stderr", length=72)),
         indented(stderr),
         indented(banner(None, length=72))))


if __name__ == "__main__" and sys.argv[1:]:
    testfiles = []
    for arg in sys.argv[1:]:
        testfiles += glob.glob(arg)
else:
    testfiles = glob.glob("cmdln_*.py")
for fname in testfiles:
    if not fname.endswith('.py'):
        continue
    base = os.path.basename(os.path.splitext(fname)[0])
    testfunc = lambda self, base=base, fname=fname: _testOneCmdln(self, base, fname)
    if base.startswith("cmdln_"):
        base = base[len("cmdln_"):]
    testname = 'test_'+base
    setattr(CmdlnTestCase, testname, testfunc)



#---- mainline

def suite():
    """Return a unittest.TestSuite to be used by test.py."""
    return unittest.makeSuite(CmdlnTestCase)

if __name__ == "__main__":
    runner = unittest.TextTestRunner(sys.stdout, verbosity=2)
    s = suite()
    result = runner.run(s)
