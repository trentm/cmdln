#!/usr/bin/env python

"""A demonstration for how one would start implementing 'svn' (the
Subversion source code control system command-line client) using
cmdln.py.
"""

import sys
import cmdln

class MySVN(cmdln.Cmdln):
    """Usage:
        svn SUBCOMMAND [ARGS...]
        svn help SUBCOMMAND

    Most subcommands take file and/or directory arguments, recursing
    on the directories.  If no arguments are supplied to such a
    command, it will recurse on the current directory (inclusive) by
    default.

    ${command_list}
    ${help_list}
    Subversion is a tool for version control.
    For additional information, see http://subversion.tigris.org/
    """
    name = "svn"

    def __init__(self, *args, **kwargs):
        cmdln.Cmdln.__init__(self, *args, **kwargs)
        cmdln.Cmdln.do_help.aliases.append("h")

    @cmdln.option("--no-auto-props", action='store_true',
                  help='disable automatic properties')
    @cmdln.option("--auto-props", action='store_true',
                  help='enable automatic properties')
    @cmdln.option("--force", action='store_true',
                  help='force operation to run')
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    def do_add(self, subcmd, opts, *args):
        """Put files and directories under version control, scheduling
        them for addition to repository.  They will be added in next commit.

        usage:
            add PATH...
        
        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("praise", "annotate", "ann")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("-v", "--verbose", action='store_true',
                  help='print extra information')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_blame(self, subcmd, opts, *args):
        """Output the content of specified files or
        URLs with revision and author information in-line.

        usage:
            blame TARGET...
        
        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_cat(self, subcmd, opts, *args):
        """Output the content of specified files or URLs.

        usage:
            cat TARGET...
        
        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("co")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_checkout(self, subcmd, opts, *args):
        """Check out a working copy from a repository.

        usage:
            checkout URL... [PATH]
        
        Note: If PATH is omitted, the basename of the URL will be used as
        the destination. If multiple URLs are given each will be checked
        out into a sub-directory of PATH, with the name of the sub-directory
        being the basename of the URL.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--diff3-cmd", metavar='ARG',
                  help='use ARG as merge command')
    def do_cleanup(self, subcmd, opts, *args):
        """Recursively clean up the working copy, removing locks, resuming
        unfinished operations, etc.

        usage:
            cleanup [PATH...]
        
        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("ci")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--editor-cmd", metavar='ARG',
                  help='use ARG as external editor')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--force-log", action='store_true',
                  help='force validity of log message source')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-F", "--file", metavar='ARG',
                  help='read data from file ARG')
    @cmdln.option("-m", "--message", metavar='ARG',
                  help='specify commit message ARG')
    def do_commit(self, subcmd, opts, *args):
        """Send changes from your working copy to the repository.

        usage:
            commit [PATH...]
        
        A log message must be provided, but it can be empty.  If it is not
        given by a --message or --file option, an editor will be started.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("cp")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--editor-cmd", metavar='ARG',
                  help='use ARG as external editor')
    @cmdln.option("--force-log", action='store_true',
                  help='force validity of log message source')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    @cmdln.option("-F", "--file", metavar='ARG',
                  help='read data from file ARG')
    @cmdln.option("-m", "--message", metavar='ARG',
                  help='specify commit message ARG')
    def do_copy(self, subcmd, opts, *args):
        """Duplicate something in working copy or repository, remembering history.

        usage:
            copy SRC DST
        
        SRC and DST can each be either a working copy (WC) path or URL:
          WC  -> WC:   copy and schedule for addition (with history)
          WC  -> URL:  immediately commit a copy of WC to URL
          URL -> WC:   check out URL into WC, schedule for addition
          URL -> URL:  complete server-side copy;  used to branch & tag

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("del", "remove", "rm")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--editor-cmd", metavar='ARG',
                  help='use ARG as external editor')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-F", "--file", metavar='ARG',
                  help='read data from file ARG')
    @cmdln.option("-m", "--message", metavar='ARG',
                  help='specify commit message ARG')
    @cmdln.option("--force-log", action='store_true',
                  help='force validity of log message source')
    @cmdln.option("--force", action='store_true',
                  help='force operation to run')
    def do_delete(self, subcmd, opts, *args):
        """Remove files and directories from version control.

        usage:
            1. delete PATH...
            2. delete URL...
        
        1. Each item specified by a PATH is scheduled for deletion upon
          the next commit.  Files, and directories that have not been
          committed, are immediately removed from the working copy.
          PATHs that are, or contain, unversioned or modified items will
          not be removed unless the --force option is given.
        
        2. Each item specified by a URL is deleted from the repository
          via an immediate commit.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("di")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--notice-ancestry", action='store_true',
                  help='notice ancestry when calculating differences')
    @cmdln.option("--no-diff-deleted", action='store_true',
                  help='do not print differences for deleted files')
    @cmdln.option("--diff-cmd", metavar='ARG',
                  help='use ARG as diff command')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-x", "--extensions", metavar='ARG',
                  help='pass ARG as bundled options to GNU diff')
    @cmdln.option("--new", metavar='ARG',
                  help='use ARG as the newer target')
    @cmdln.option("--old", metavar='ARG',
                  help='use ARG as the older target')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_diff(self, subcmd, opts, *args):
        """Display the differences between two paths.

        usage:
            1. diff [-r N[:M]] [TARGET[@REV]...]
            2. diff [-r N[:M]] --old=OLD-TGT[@OLDREV] [--new=NEW-TGT[@NEWREV]] \
                    [PATH...]
            3. diff OLD-URL[@OLDREV] NEW-URL[@NEWREV]
        
        1. Display the changes made to TARGETs as they are seen in REV between
           two revisions.  TARGETs may be working copy paths or URLs.
        
           N defaults to BASE if any TARGET is a working copy path, otherwise it
           must be specified.  M defaults to the current working version if any
           TARGET is a working copy path, otherwise it defaults to HEAD.
        
        2. Display the differences between OLD-TGT as it was seen in OLDREV and
           NEW-TGT as it was seen in NEWREV.  PATHs, if given, are relative to
           OLD-TGT and NEW-TGT and restrict the output to differences for those
           paths.  OLD-TGT and NEW-TGT may be working copy paths or URL[@REV]. 
           NEW-TGT defaults to OLD-TGT if not specified.  -r N makes OLDREV default
           to N, -r N:M makes OLDREV default to N and NEWREV default to M.
        
        3. Shorthand for 'svn diff --old=OLD-URL[@OLDREV] --new=NEW-URL[@NEWREV]'
        
        Use just 'svn diff' to display local modifications in a working copy.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--native-eol", metavar='ARG',
                  help="use a different EOL marker than the standard\nsystem marker for files with a native svn:eol-style\nproperty.  ARG may be one of 'LF', 'CR', 'CRLF'")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--force", action='store_true',
                  help='force operation to run')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_export(self, subcmd, opts, *args):
        """Create an unversioned copy of a tree.

        usage:
            1. export [-r REV] URL [PATH]
            2. export [-r REV] PATH1 [PATH2]
        
        1. Exports a clean directory tree from the repository specified by
           URL, at revision REV if it is given, otherwise at HEAD, into
           PATH. If PATH is omitted, the last component of the URL is used
           for the local directory name.
        
        2. Exports a clean directory tree from the working copy specified by
           PATH1, at revision REV if it is given, otherwise at WORKING, into
           PATH2.  If PATH2 is omitted, the last component of the PATH1 is used
           for the local directory name. If REV is not specified, all local
           changes will be preserved, but files not under version control will
           not be copied.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)


    @cmdln.option("--no-auto-props", action='store_true',
                  help='disable automatic properties')
    @cmdln.option("--auto-props", action='store_true',
                  help='enable automatic properties')
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--editor-cmd", metavar='ARG',
                  help='use ARG as external editor')
    @cmdln.option("--force-log", action='store_true',
                  help='force validity of log message source')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-F", "--file", metavar='ARG',
                  help='read data from file ARG')
    @cmdln.option("-m", "--message", metavar='ARG',
                  help='specify commit message ARG')
    def do_import(self, subcmd, opts, *args):
        """Commit an unversioned file or tree into the repository.

        usage:
            import [PATH] URL
        
        Recursively commit a copy of PATH to URL.
        If PATH is omitted '.' is assumed.  Parent directories are created
        as necessary in the repository.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    def do_info(self, subcmd, opts, *args):
        """Display information about a file or directory.

        usage:
            info [PATH...]
        
        Print information about each PATH (default: '.').

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("ls")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    @cmdln.option("-v", "--verbose", action='store_true',
                  help='print extra information')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_list(self, subcmd, opts, *args):
        """List directory entries in the repository.

        usage:
            list [TARGET...]
        
        List each TARGET file and the contents of each TARGET directory as
        they exist in the repository.  If TARGET is a working copy path, the
        corresponding repository URL will be used.
        
        The default TARGET is '.', meaning the repository URL of the current
        working directory.
        
        With --verbose, the following fields show the status of the item:
        
          Revision number of the last commit
          Author of the last commit
          Size (in bytes)
          Date and time of the last commit

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--xml", action='store_true',
                  help='output in XML')
    @cmdln.option("--incremental", action='store_true',
                  help='give output suitable for concatenation')
    @cmdln.option("--stop-on-copy", action='store_true',
                  help='do not cross copies while traversing history')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    @cmdln.option("-v", "--verbose", action='store_true',
                  help='print extra information')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_log(self, subcmd, opts, *args):
        """Show the log messages for a set of revision(s) and/or file(s).

        usage:
            1. log [PATH]
            2. log URL [PATH...]
        
        1. Print the log messages for a local PATH (default: '.').
           The default revision range is BASE:1.
        
        2. Print the log messages for the PATHs (default: '.') under URL.
           The default revision range is HEAD:1.
        
        With -v, also print all affected paths with each log message.
        With -q, don't print the log message body itself (note that this is
        compatible with -v).
        
        Each log message is printed just once, even if more than one of the
        affected paths for that revision were explicitly requested.  Logs
        follow copy history by default.  Use --stop-on-copy to disable this
        behavior, which can be useful for determining branchpoints.
        
        Examples:
          svn log
          svn log foo.c
          svn log http://www.example.com/repo/project/foo.c
          svn log http://www.example.com/repo/project foo.c bar.c

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--ignore-ancestry", action='store_true',
                  help='ignore ancestry when calculating merges')
    @cmdln.option("--diff3-cmd", metavar='ARG',
                  help='use ARG as merge command')
    @cmdln.option("--dry-run", action='store_true',
                  help='try operation but make no changes')
    @cmdln.option("--force", action='store_true',
                  help='force operation to run')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_merge(self, subcmd, opts, *args):
        """Apply the differences between two sources to a working copy path.

        usage:
            1. merge sourceURL1[@N] sourceURL2[@M] [WCPATH]
            2. merge sourceWCPATH1@N sourceWCPATH2@M [WCPATH]
            3. merge -r N:M SOURCE[@REV] [WCPATH]
        
        1. In the first form, the source URLs are specified at revisions
           N and M.  These are the two sources to be compared.  The revisions
           default to HEAD if omitted.
        
        2. In the second form, the URLs corresponding to the source working
           copy paths define the sources to be compared.  The revisions must
           be specified.
        
        3. In the third form, SOURCE can be a URL, or working copy item
           in which case the corresponding URL is used.  This URL in
           revision REV is compared as it existed between revisions N and 
           M.  If REV is not specified, HEAD is assumed.
        
        WCPATH is the working copy path that will receive the changes.
        If WCPATH is omitted, a default value of '.' is assumed, unless
        the sources have identical basenames that match a file within '.':
        in which case, the differences will be applied to that file.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--force-log", action='store_true',
                  help='force validity of log message source')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--editor-cmd", metavar='ARG',
                  help='use ARG as external editor')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-F", "--file", metavar='ARG',
                  help='read data from file ARG')
    @cmdln.option("-m", "--message", metavar='ARG',
                  help='specify commit message ARG')
    def do_mkdir(self, subcmd, opts, *args):
        """Create a new directory under version control.

        usage:
            1. mkdir PATH...
            2. mkdir URL...
        
        Create version controlled directories.
        
        1. Each directory specified by a working copy PATH is created locally
          and scheduled for addition upon the next commit.
        
        2. Each directory specified by a URL is created in the repository via
          an immediate commit.
        
        In both cases, all the intermediate directories must already exist.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("mv", "rename", "ren")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--force-log", action='store_true',
                  help='force validity of log message source')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--editor-cmd", metavar='ARG',
                  help='use ARG as external editor')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--force", action='store_true',
                  help='force operation to run')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    @cmdln.option("-F", "--file", metavar='ARG',
                  help='read data from file ARG')
    @cmdln.option("-m", "--message", metavar='ARG',
                  help='specify commit message ARG')
    def do_move(self, subcmd, opts, *args):
        """Move and/or rename something in working copy or repository.

        usage:
            move SRC DST
        
        Note:  this subcommand is equivalent to a 'copy' and 'delete'.
        
        SRC and DST can both be working copy (WC) paths or URLs:
          WC  -> WC:   move and schedule for addition (with history)
          URL -> URL:  complete server-side rename.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("pdel", "pd")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--revprop", action='store_true',
                  help='operate on a revision property (use with -r)')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    def do_propdel(self, subcmd, opts, *args):
        """Remove PROPNAME from files, dirs, or revisions.

        usage:
            1. propdel PROPNAME [PATH...]
            2. propdel PROPNAME --revprop -r REV [URL]
        
        1. Removes versioned props in working copy.
        2. Removes unversioned remote prop on repos revision.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("pedit", "pe")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--force", action='store_true',
                  help='force operation to run')
    @cmdln.option("--editor-cmd", metavar='ARG',
                  help='use ARG as external editor')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--revprop", action='store_true',
                  help='operate on a revision property (use with -r)')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_propedit(self, subcmd, opts, *args):
        """Edit property PROPNAME with an external editor on targets.

        usage:
            1. propedit PROPNAME PATH...
            2. propedit PROPNAME --revprop -r REV [URL]
        
        1. Edits versioned props in working copy.
        2. Edits unversioned remote prop on repos revision.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("pget", "pg")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--strict", action='store_true',
                  help='use strict semantics')
    @cmdln.option("--revprop", action='store_true',
                  help='operate on a revision property (use with -r)')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    def do_propget(self, subcmd, opts, *args):
        """Print value of PROPNAME on files, dirs, or revisions.

        usage:
            1. propget PROPNAME [PATH...]
            2. propget PROPNAME --revprop -r REV [URL]
        
        1. Prints versioned prop in working copy.
        2. Prints unversioned remote prop on repos revision.
        
        By default, this subcommand will add an extra newline to the end
        of the property values so that the output looks pretty.  Also,
        whenever there are multiple paths involved, each property value
        is prefixed with the path with which it is associated.  Use
        the --strict option to disable these beautifications (useful,
        for example, when redirecting binary property values to a file).

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("plist", "pl")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--revprop", action='store_true',
                  help='operate on a revision property (use with -r)')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    @cmdln.option("-v", "--verbose", action='store_true',
                  help='print extra information')
    def do_proplist(self, subcmd, opts, *args):
        """List all properties on files, dirs, or revisions.

        usage:
            1. proplist [PATH...]
            2. proplist --revprop -r REV [URL]
        
        1. Lists versioned props in working copy.
        2. Lists unversioned remote props on repos revision.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("pset", "ps")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--force", action='store_true',
                  help='force operation to run')
    @cmdln.option("--encoding", metavar='ARG',
                  help='treat value as being in charset encoding ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--revprop", action='store_true',
                  help='operate on a revision property (use with -r)')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-F", "--file", metavar='ARG',
                  help='read data from file ARG')
    def do_propset(self, subcmd, opts, *args):
        """Set PROPNAME to PROPVAL on files, dirs, or revisions.

        usage:
            1. propset PROPNAME [PROPVAL | -F VALFILE] PATH...
            2. propset PROPNAME --revprop -r REV [PROPVAL | -F VALFILE] [URL]
        
        1. Creates a versioned, local propchange in working copy.
        2. Creates an unversioned, remote propchange on repos revision.
        
        Note: svn recognizes the following special versioned properties
        but will store any arbitrary properties set:
          svn:ignore     - A newline separated list of file patterns to ignore.
          svn:keywords   - Keywords to be expanded.  Valid keywords are:
            URL, HeadURL             - The URL for the head version of the object.
            Author, LastChangedBy    - The last person to modify the file.
            Date, LastChangedDate    - The date/time the object was last modified.
            Rev, Revision,           - The last revision the object changed.
            LastChangedRevision
            Id                       - A compressed summary of the previous
                                         4 keywords.
          svn:executable - If present, make the file executable. This
            property cannot be set on a directory.  A non-recursive attempt
            will fail, and a recursive attempt will set the property only
            on the file children of the directory.
          svn:eol-style  - One of 'native', 'LF', 'CR', 'CRLF'.
          svn:mime-type  - The mimetype of the file.  Used to determine
            whether to merge the file, and how to serve it from Apache.
            A mimetype beginning with 'text/' (or an absent mimetype) is
            treated as text.  Anything else is treated as binary.
          svn:externals  - A newline separated list of module specifiers,
            each of which consists of a relative directory path, optional
            revision flags, and an URL.  For example
              foo             http://example.com/repos/zig
              foo/bar -r 1234 http://example.com/repos/zag

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    def do_resolved(self, subcmd, opts, *args):
        """Remove 'conflicted' state on working copy files or directories.

        usage:
            resolved PATH...
        
        Note:  this subcommand does not semantically resolve conflicts or
        remove conflict markers; it merely removes the conflict-related
        artifact files and allows PATH to be committed again.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-R", "--recursive", action='store_true',
                  help='descend recursively')
    @cmdln.option("--targets", metavar='ARG',
                  help='pass contents of file ARG as additional args')
    def do_revert(self, subcmd, opts, *args):
        """Restore pristine working copy file (undo most local edits).

        usage:
            revert PATH...
        
        Note:  this subcommand does not require network access, and resolves
        any conflicted states.  However, it does not restore removed directories.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("stat", "st")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--no-ignore", action='store_true',
                  help='disregard default and svn:ignore property ignores')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-v", "--verbose", action='store_true',
                  help='print extra information')
    @cmdln.option("-u", "--show-updates", action='store_true',
                  help='display update information')
    def do_status(self, subcmd, opts, *args):
        """Print the status of working copy files and directories.

        usage:
            status [PATH...]
        
        With no args, print only locally modified items (no network access).
        With -u, add working revision and server out-of-date information.
        With -v, print full revision information on every item.
        
        The first five columns in the output are each one character wide:
          First column: Says if item was added, deleted, or otherwise changed
            ' ' no modifications
            'A' Added
            'C' Conflicted
            'D' Deleted
            'G' Merged
            'I' Ignored
            'M' Modified
            'R' Replaced
            'X' item is unversioned, but is used by an externals definition
            '?' item is not under version control
            '!' item is missing (removed by non-svn command) or incomplete
            '~' versioned item obstructed by some item of a different kind
          Second column: Modifications of a file's or directory's properties
            ' ' no modifications
            'C' Conflicted
            'M' Modified
          Third column: Whether the working copy directory is locked
            ' ' not locked
            'L' locked
          Fourth column: Scheduled commit will contain addition-with-history
            ' ' no history scheduled with commit
            '+' history scheduled with commit
          Fifth column: Whether the item is switched relative to its parent
            ' ' normal
            'S' switched
        
        The out-of-date information appears in the eighth column (with -u):
            '*' a newer revision exists on the server
            ' ' the working copy is up to date
        
        Remaining fields are variable width and delimited by spaces:
          The working revision (with -u or -v)
          The last committed revision and last committed author (with -v)
          The working copy path is always the final field, so it can
            include spaces.
        
        Example output:
          svn status wc
           M     wc/bar.c
          A  +   wc/qax.c
        
          svn status -u wc
           M           965    wc/bar.c
                 *     965    wc/foo.c
          A  +         965    wc/qax.c
          Head revision:   981
        
          svn status --show-updates --verbose wc
           M           965       938 kfogel       wc/bar.c
                 *     965       922 sussman      wc/foo.c
          A  +         965       687 joe          wc/qax.c
                       965       687 joe          wc/zig.c
          Head revision:   981

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("sw")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--relocate", action='store_true',
                  help='relocate via URL-rewriting')
    @cmdln.option("--diff3-cmd", metavar='ARG',
                  help='use ARG as merge command')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_switch(self, subcmd, opts, *args):
        """Update the working copy to a different URL.

        usage:
            1. switch URL [PATH]
            2. switch --relocate FROM TO [PATH...]
        
        1. Update the working copy to mirror a new URL within the repository.
           This behaviour is similar to 'svn update', and is the way to
           move a working copy to a branch or tag within the same repository.
        
        2. Rewrite working copy URL metadata to reflect a syntactic change only.
           This is used when repository's root URL changes (such as a schema
           or hostname change) but your working copy still reflects the same
           directory within the same repository.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

    @cmdln.alias("up")
    @cmdln.option("--config-dir", metavar='ARG',
                  help='read user configuration files from directory ARG')
    @cmdln.option("--non-interactive", action='store_true',
                  help='do no interactive prompting')
    @cmdln.option("--no-auth-cache", action='store_true',
                  help='do not cache authentication tokens')
    @cmdln.option("--password", metavar='ARG',
                  help='specify a password ARG')
    @cmdln.option("--username", metavar='ARG',
                  help='specify a username ARG')
    @cmdln.option("--diff3-cmd", metavar='ARG',
                  help='use ARG as merge command')
    @cmdln.option("-q", "--quiet", action='store_true',
                  help='print as little as possible')
    @cmdln.option("-N", "--non-recursive", action='store_true',
                  help='operate on single directory only')
    @cmdln.option("-r", "--revision", metavar='ARG',
                  help='ARG (some commands also take ARG1:ARG2 range)\nA revision argument can be one of:\n   NUMBER       revision number\n   "{" DATE "}" revision at start of the date\n   "HEAD"       latest in repository\n   "BASE"       base rev of item\'s working copy\n   "COMMITTED"  last commit at or before BASE\n   "PREV"       revision just before COMMITTED')
    def do_update(self, subcmd, opts, *args):
        """Bring changes from the repository into the working copy.

        usage:
            update [PATH...]
        
        If no revision given, bring working copy up-to-date with HEAD rev.
        Else synchronize working copy to revision given by -r.
        
        For each updated item a line will start with a character reporting the
        action taken.  These characters have the following meaning:
        
          A  Added
          D  Deleted
          U  Updated
          C  Conflict
          G  Merged
        
        A character in the first column signifies an update to the actual file,
        while updates to the file's properties are shown in the second column.

        ${cmd_option_list}
        """
        print "'svn %s' opts: %s" % (subcmd, opts)
        print "'svn %s' args: %s" % (subcmd, args)

if __name__ == "__main__":
    svn = MySVN()
    sys.exit(svn.main())
