import os
import argparse
import textwrap

import bumblebee.theme
import bumblebee.module

class Config(object):
    def __init__(self, args):
        self._raw = args
        self._parser = self.parser()
        self._indent = " "*4

        if len(args) == 0:
            self._parser.print_help()
            self._parser.exit()

        self._args = self._parser.parse_args(args)

        if self._args.list == "modules":
            self.print_modules()
        if self._args.list == "themes":
            self.print_themes()
        if self._args.list:
            self._parser.exit()

    def parser(self):
        parser = argparse.ArgumentParser(description="display system data in the i3bar")
        parser.add_argument("-m", "--modules", nargs="+",
            help="List of modules to load. The order of the list determines "
            "their order in the i3bar (from left to right)",
            default=[])
        parser.add_argument("-l", "--list",
            help="List: 'modules', 'themes' ",
            choices = [ "modules", "themes" ],
            default="modules")
        parser.add_argument("-t", "--theme", help="Specify which theme to use for "
            "drawing the modules",
            default="default")

        return parser

    def print_themes(self):
        print(textwrap.fill(", ".join(bumblebee.theme.themes()),
            80, initial_indent = self._indent, subsequent_indent = self._indent
        ))

    def print_modules(self):
        for m in bumblebee.module.modules():

            print("{}{}: ".format(self._indent, m.name()))
            print textwrap.fill("About : {}".format(m.description()),
                80, initial_indent=self._indent*2, subsequent_indent=self._indent*4)
            print textwrap.fill("Usage : {}".format(m.usage()),
                80, initial_indent=self._indent*2, subsequent_indent=self._indent*4)
            print textwrap.fill("Notes : {}".format(m.notes()),
                80, initial_indent=self._indent*2, subsequent_indent=self._indent*4)
            print ""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
