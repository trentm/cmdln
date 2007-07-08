#!/usr/bin/env python

import sys
import cmdln


class Client(cmdln.Cmdln):
    name = "p4"

    def get_optparser(self):
        parser = cmdln.Cmdln.get_optparser(self)
        parser.add_option("-c", dest="client")
        parser.add_option("-C", dest="charset")
        parser.add_option("-d", dest="dir")
        parser.add_option("-H", dest="host")
        parser.add_option("-G", action="store_true", dest="marshal")
        parser.add_option("-L", dest="language")
        parser.add_option("-p", dest="port")
        parser.add_option("-P", dest="password")
        parser.add_option("-s", action="store_true", dest="script")
        parser.add_option("-u", dest="user")
        parser.add_option("-x", dest="file")
        return parser

    def help_commands(self):
        return """
        Perforce client commands:

            $(command_list}
        """

    @cmdln.option("-c", dest="changelist")
    @cmdln.option("-t", dest="filetype")
    def do_add(self, subcmd, opts, *paths):
        """Open a new file to add it to the depot
        
        usage:
            p4 add [PATHS...]

        ${cmd_option_list}
        """
        print "p4 %s: opts=%s paths=%r" % (subcmd, opts, paths)

    def do_admin(self, subcmd, opts, action):
        """Perform administrative operations on the server"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    @cmdln.option("-a", action="store_true", dest="all")
    @cmdln.option("-c", action="store_true", dest="changenums")
    @cmdln.option("-q", action="store_true", dest="quiet")
    def do_annotate(self, opts, args):
        """Print file lines along with their revisions"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    @cmdln.option("-f", action="store_true", dest="force")
    @cmdln.option("-d", action="store_true", dest="delete")
    @cmdln.option("-o", action="store_true", dest="output")
    @cmdln.option("-i", action="store_true", dest="input")
    def do_branch(self, opts, args):
        """Create or edit a branch specification"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    def do_branches(self, opts, args):
        """Display list of branches"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    @cmdln.option("-f", action="store_true", dest="force")
    @cmdln.option("-s", action="store_true", dest="fix_status")
    @cmdln.option("-d", action="store_true", dest="delete")
    @cmdln.option("-o", action="store_true", dest="output")
    @cmdln.option("-i", action="store_true", dest="input")
    def do_change(self, opts, args):
        """Create or edit a changelist description"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    @cmdln.option("-i", action="store_true", dest="integrated")
    @cmdln.option("-t", action="store_true", dest="time")
    @cmdln.option("-l", action="store_true", dest="long")
    @cmdln.option("-c", dest="client")
    @cmdln.option("-m", dest="max")
    @cmdln.option("-s", dest="status")
    @cmdln.option("-u", dest="user")
    def do_changes(self, opts, args):
        """Display list of pending and submitted changelists"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    @cmdln.option("-f", action="store_true", dest="force")
    @cmdln.option("-t", dest="template")
    @cmdln.option("-d", action="store_true", dest="delete")
    @cmdln.option("-o", action="store_true", dest="output")
    @cmdln.option("-i", action="store_true", dest="input")
    def do_client(self, opts, args):
        """Create or edit a client specification and its view"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    def do_clients(self, opts, args):
        """Display list of known clients"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, action)

    #...

if __name__ == "__main__":
    client = Client()
    sys.exit( client.main(sys.argv) )



