
"""Makefile for the cmdln project.

${common_task_list}

See `mk -h' for options.
"""

import sys
import os
from os.path import join, dirname, normpath, abspath, exists, basename
import re
from glob import glob
import webbrowser

from mklib.common import MkError
from mklib import Task
from mklib import sh



class bugs(Task):
    """Open bug database page."""
    def make(self):
        webbrowser.open("http://code.google.com/p/cmdln/issues/list")

class site(Task):
    """Open the Google Code project page."""
    def make(self):
        webbrowser.open("http://code.google.com/p/cmdln/")


class clean(Task):
    """Clean generated files and dirs."""
    def make(self):
        patterns = [
            "dist",
            "build",
            "MANIFEST",
            "*.pyc",
            "lib/*.pyc",
        ]
        for pattern in patterns:
            p = join(self.dir, pattern)
            for path in glob(p):
                sh.rm(path, log=self.log)

class sdist(Task):
    """python setup.py sdist"""
    def make(self):
        sh.run_in_dir("%spython setup.py sdist -f --formats zip"
                        % _setup_command_prefix(),
                      self.dir, self.log.debug)

class webdist(Task):
    """Build a web dist package for trentm.com/projects/
    
    "Web dist" packages are zip files with '.web' extension. All files in
    the zip must be under a dir named after the project. There must be a
    webinfo.xml file at <projname>/webinfo.xml. This file is "defined"
    by the parsing in trentm.com/build.py.
    """ 
    deps = ["docs"]

    def results(self):
        yield join(self.dir, "dist", "cmdln-%s.web" % _get_version())

    def make(self):
        assert sys.platform != "win32", "'webdist' not implemented for win32"
        build_dir = join(self.dir, "build", "webdist")
        zip_dir = join(build_dir, "cmdln")
        if exists(build_dir):
            sh.rm(build_dir)
        os.makedirs(zip_dir)

        # Copy the webdist bits to the build tree.
        manifest = [
            "src/trentm.com/project-info.xml",
            "src/trentm.com/index.markdown",
            "LICENSE.txt",
            "lib/cmdln.py",
            "src/trentm.com/logo.jpg",
        ]
        for src in manifest:
            sh.cp(src, dstdir=zip_dir, log=self.log.info)

        # Zip up the webdist contents.
        dist_dir = join(self.dir, "dist")
        bit = abspath(join(dist_dir, "cmdln-%s.web" % _get_version()))
        if exists(bit):
            os.remove(bit)
        if not exists(dist_dir):
            os.makedirs(dist_dir)
        sh.run_in_dir("zip -r %s cmdln" % bit, build_dir, self.log.info)

class pypi_upload(Task):
    """Upload release to pypi."""
    def make(self):
        tasks = (sys.platform == "win32"
                 and "sdist --formats zip bdist_wininst upload"
                 or "sdist --formats zip upload")
        sh.run_in_dir("%spython setup.py %s" % (_setup_command_prefix(), tasks),
                      self.dir, self.log.debug)

        sys.path.insert(0, join(self.dir, "lib"))
        url = "http://pypi.python.org/pypi/cmdln/"
        import webbrowser
        webbrowser.open_new(url)

class googlecode_upload(Task):
    """Upload sdist to Google Code project site."""
    deps = ["sdist"]
    def make(self):
        try:
            import googlecode_upload
        except ImportError:
            raise MkError("couldn't import `googlecode_upload` (get it from http://support.googlecode.com/svn/trunk/scripts/googlecode_upload.py)")

        ver = _get_version()
        sdist_path = join(self.dir, "dist", "cmdln-%s.zip" % ver)
        status, reason, url = googlecode_upload.upload_find_auth(
            sdist_path,
            "cmdln", # project_name
            "cmdln %s source package" % ver, # summary
            ["Featured", "Type-Archive"]) # labels
        if not url:
            raise MkError("couldn't upload sdsit to Google Code: %s (%s)"
                          % (reason, status))
        self.log.info("uploaded sdist to `%s'", url)

        project_url = "http://code.google.com/p/cmdln/"
        import webbrowser
        webbrowser.open_new(project_url)

class trentm_com_upload(Task):
    """Upload webdist to trentm.com bits (in prep for updating trentm.com)."""
    deps = ["webdist"]
    def make(self):
        ver = _get_version()
        dist_dir = join(self.dir, "dist")

        paths = [join(dist_dir, "cmdln-%s%s" % (ver, ext))
                 for ext in [".web"]]

        # Upload the bits.
        user = "trentm"
        host = "trentm.com"
        remote_dir = "~/data/bits/cmdln/%s" % _get_version()
        if sys.platform == "win32":
            ssh = "plink"
            scp = "pscp -unsafe"
        else:
            ssh = "ssh"
            scp = "scp"
        sh.run("%s %s@%s 'mkdir -p %s'" % (ssh, user, host, remote_dir),
               self.log.info)
        for path in paths:
            sh.run("%s %s %s@%s:%s" % (scp, path, user, host, remote_dir),
                   self.log.info)

class todo(Task):
    """Print out todo's and xxx's in the docs area."""
    def make(self):
        for path in _paths_from_path_patterns(['.'],
                excludes=[".svn", "*.pyc", "TO""DO.txt", "Makefile.py",
                          "*.png", "*.gif", "*.pprint", "*.prof",
                          "tmp-*"]):
            self._dump_pattern_in_path("TO\DO\\|XX\X", path)

        path = join(self.dir, "TO""DO.txt")
        todos = re.compile("^- ", re.M).findall(open(path, 'r').read())
        print "(plus %d TODOs from TO""DO.txt)" % len(todos)

    def _dump_pattern_in_path(self, pattern, path):
        os.system("grep -nH '%s' '%s'" % (pattern, path))


class docs(Task):
    """Regenerate some doc bits from project-info.xml."""
    deps = ["src/trentm.com/project-info.xml"]
    results = [
        "README.txt",
        "src/trentm.com/index.markdown"
    ]
    def make(self):
        project_info_xml = join("src", "trentm.com", "project-info.xml")
        index_markdown = join("src", "trentm.com", "index.markdown")
        sh.run_in_dir("projinfo -f %s -R -o README.txt --force"
                      % project_info_xml, self.dir)
        sh.run_in_dir("projinfo -f %s --index-markdown -o %s --force"
                      % (project_info_xml, index_markdown), self.dir)

class check_version(Task):
    """grep for version strings in source code
    
    List all things that look like version strings in the source code.
    Used for checking that versioning is updated across the board.  
    """
    sources = [
        "lib/cmdln.py",
        "src/trentm.com/project-info.xml",
    ]
    def make(self):
        pattern = r'[0-9]\+\(\.\|, \)[0-9]\+\(\.\|, \)[0-9]\+'
        sh.run_in_dir('grep -n "%s" %s' % (pattern, ' '.join(self.sources)),
                      self.dir)


#---- internal support stuff

# Recipe: paths_from_path_patterns (0.3.7)
def _should_include_path(path, includes, excludes):
    """Return True iff the given path should be included."""
    from os.path import basename
    from fnmatch import fnmatch

    base = basename(path)
    if includes:
        for include in includes:
            if fnmatch(base, include):
                try:
                    log.debug("include `%s' (matches `%s')", path, include)
                except (NameError, AttributeError):
                    pass
                break
        else:
            try:
                log.debug("exclude `%s' (matches no includes)", path)
            except (NameError, AttributeError):
                pass
            return False
    for exclude in excludes:
        if fnmatch(base, exclude):
            try:
                log.debug("exclude `%s' (matches `%s')", path, exclude)
            except (NameError, AttributeError):
                pass
            return False
    return True

_NOT_SPECIFIED = ("NOT", "SPECIFIED")
def _paths_from_path_patterns(path_patterns, files=True, dirs="never",
                              recursive=True, includes=[], excludes=[],
                              on_error=_NOT_SPECIFIED):
    """_paths_from_path_patterns([<path-patterns>, ...]) -> file paths

    Generate a list of paths (files and/or dirs) represented by the given path
    patterns.

        "path_patterns" is a list of paths optionally using the '*', '?' and
            '[seq]' glob patterns.
        "files" is boolean (default True) indicating if file paths
            should be yielded
        "dirs" is string indicating under what conditions dirs are
            yielded. It must be one of:
              never             (default) never yield dirs
              always            yield all dirs matching given patterns
              if-not-recursive  only yield dirs for invocations when
                                recursive=False
            See use cases below for more details.
        "recursive" is boolean (default True) indicating if paths should
            be recursively yielded under given dirs.
        "includes" is a list of file patterns to include in recursive
            searches.
        "excludes" is a list of file and dir patterns to exclude.
            (Note: This is slightly different than GNU grep's --exclude
            option which only excludes *files*.  I.e. you cannot exclude
            a ".svn" dir.)
        "on_error" is an error callback called when a given path pattern
            matches nothing:
                on_error(PATH_PATTERN)
            If not specified, the default is look for a "log" global and
            call:
                log.error("`%s': No such file or directory")
            Specify None to do nothing.

    Typically this is useful for a command-line tool that takes a list
    of paths as arguments. (For Unix-heads: the shell on Windows does
    NOT expand glob chars, that is left to the app.)

    Use case #1: like `grep -r`
      {files=True, dirs='never', recursive=(if '-r' in opts)}
        script FILE     # yield FILE, else call on_error(FILE)
        script DIR      # yield nothing
        script PATH*    # yield all files matching PATH*; if none,
                        # call on_error(PATH*) callback
        script -r DIR   # yield files (not dirs) recursively under DIR
        script -r PATH* # yield files matching PATH* and files recursively
                        # under dirs matching PATH*; if none, call
                        # on_error(PATH*) callback

    Use case #2: like `file -r` (if it had a recursive option)
      {files=True, dirs='if-not-recursive', recursive=(if '-r' in opts)}
        script FILE     # yield FILE, else call on_error(FILE)
        script DIR      # yield DIR, else call on_error(DIR)
        script PATH*    # yield all files and dirs matching PATH*; if none,
                        # call on_error(PATH*) callback
        script -r DIR   # yield files (not dirs) recursively under DIR
        script -r PATH* # yield files matching PATH* and files recursively
                        # under dirs matching PATH*; if none, call
                        # on_error(PATH*) callback

    Use case #3: kind of like `find .`
      {files=True, dirs='always', recursive=(if '-r' in opts)}
        script FILE     # yield FILE, else call on_error(FILE)
        script DIR      # yield DIR, else call on_error(DIR)
        script PATH*    # yield all files and dirs matching PATH*; if none,
                        # call on_error(PATH*) callback
        script -r DIR   # yield files and dirs recursively under DIR
                        # (including DIR)
        script -r PATH* # yield files and dirs matching PATH* and recursively
                        # under dirs; if none, call on_error(PATH*)
                        # callback
    """
    from os.path import basename, exists, isdir, join
    from glob import glob

    assert not isinstance(path_patterns, basestring), \
        "'path_patterns' must be a sequence, not a string: %r" % path_patterns
    GLOB_CHARS = '*?['

    for path_pattern in path_patterns:
        # Determine the set of paths matching this path_pattern.
        for glob_char in GLOB_CHARS:
            if glob_char in path_pattern:
                paths = glob(path_pattern)
                break
        else:
            paths = exists(path_pattern) and [path_pattern] or []
        if not paths:
            if on_error is None:
                pass
            elif on_error is _NOT_SPECIFIED:
                try:
                    log.error("`%s': No such file or directory", path_pattern)
                except (NameError, AttributeError):
                    pass
            else:
                on_error(path_pattern)

        for path in paths:
            if isdir(path):
                # 'includes' SHOULD affect whether a dir is yielded.
                if (dirs == "always"
                    or (dirs == "if-not-recursive" and not recursive)
                   ) and _should_include_path(path, includes, excludes):
                    yield path

                # However, if recursive, 'includes' should NOT affect
                # whether a dir is recursed into. Otherwise you could
                # not:
                #   script -r --include="*.py" DIR
                if recursive and _should_include_path(path, [], excludes):
                    for dirpath, dirnames, filenames in os.walk(path):
                        dir_indeces_to_remove = []
                        for i, dirname in enumerate(dirnames):
                            d = join(dirpath, dirname)
                            if dirs == "always" \
                               and _should_include_path(d, includes, excludes):
                                yield d
                            if not _should_include_path(d, [], excludes):
                                dir_indeces_to_remove.append(i)
                        for i in reversed(dir_indeces_to_remove):
                            del dirnames[i]
                        if files:
                            for filename in sorted(filenames):
                                f = join(dirpath, filename)
                                if _should_include_path(f, includes, excludes):
                                    yield f

            elif files and _should_include_path(path, includes, excludes):
                yield path

_g_version = None
def _get_version():
    global _g_version
    if _g_version is None:
        sys.path.insert(0, join(dirname(__file__), "lib"))
        try:
            import cmdln
            _g_version = cmdln.__version__
        finally:
            del sys.path[0]
    return _g_version

def _setup_command_prefix():
    prefix = ""
    if sys.platform == "darwin":
        # http://forums.macosxhints.com/archive/index.php/t-43243.html
        # This is an Apple customization to `tar` to avoid creating
        # '._foo' files for extended-attributes for archived files.
        prefix = "COPY_EXTENDED_ATTRIBUTES_DISABLE=1 "
    return prefix


