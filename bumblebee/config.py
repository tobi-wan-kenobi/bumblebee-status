import os
import argparse
import textwrap

import bumblebee.theme
import bumblebee.module

class print_usage(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        argparse.Action.__init__(self, option_strings, dest, nargs, **kwargs)
        self._indent = " "*4

    def __call__(self, parser, namespace, value, option_string=None):
        if value == "modules":
            self.print_modules()
        elif value == "themes":
            self.print_themes()
        else:
            parser.print_help()
        parser.exit()

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

class ModuleConfig(object):
    def __init__(self, config, prefix):
        self._prefix = prefix
        self._config = config

    def set(self, name, value):
        name = self._prefix + name
        return self._config.set(name, value)

    def parameter(self, name, default=None):
        name = self._prefix + name
        return self._config.parameter(name, default)

    def increase(self, name, limit, default):
        name = self._prefix + name
        return self._config.increase(name, limit, default)

class Config(object):
    def __init__(self, args):
        self._raw = args
        self._parser = self._parser()
        self._store = {}

        if len(args) == 0:
            self._parser.print_help()
            self._parser.exit()

        self._args = self._parser.parse_args(args)

        for p in self._args.parameters:
            key, value = p.split("=")
            self.parameter(key, value)

    def set(self, name, value):
        self._store[name] = value

    def parameter(self, name, default=None):
        if not name in self._store:
            self.set(name, default)
        return self._store.get(name, default)

    def increase(self, name, limit, default):
        self._store[name] += 1
        if self._store[name] >= limit:
            self._store[name] = default
        return self._store[name]

    def theme(self):
        return self._args.theme

    def modules(self):
        result = []
        for m in self._args.modules:
            items = m.split(":")
            result.append({ "name": items[0], "alias": items[1] if len(items) > 1 else None })
        return result

    def _parser(self):
        parser = argparse.ArgumentParser(description="display system data in the i3bar")
        parser.add_argument("-m", "--modules", nargs="+",
            help="List of modules to load. The order of the list determines "
            "their order in the i3bar (from left to right)",
            default=[],
        )
        parser.add_argument("-l", "--list",
            help="List: 'modules', 'themes' ",
            choices = [ "modules", "themes" ],
            action=print_usage,
        )
        parser.add_argument("-p", "--parameters", nargs="+",
            help="Provide configuration parameters to individual modules.",
            default=[]
        )
        parser.add_argument("-t", "--theme", help="Specify which theme to use for "
            "drawing the modules",
            default="default",
        )

        return parser

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
