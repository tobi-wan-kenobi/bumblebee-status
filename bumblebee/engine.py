import os
import sys
import glob
import pkgutil
import textwrap
import argparse
import importlib
import bumblebee.theme
import bumblebee.output
import bumblebee.modules

class Arguments:
    def __init__(self):
        parser = self.create_parser()

        if len(sys.argv) == 1:
            parser.print_help()
            parser.exit()

        self._args = parser.parse_args()

        if self._args.list:
            self.print_module_list()
            self.print_theme_list()
            parser.exit()

    def args(self):
        return self._args

    def create_parser(self):
        parser = argparse.ArgumentParser(description="display system data in the i3bar")
        parser.add_argument("-m", "--modules", nargs="+",
            help="List of modules to load. The order of the list determines "
            "their order in the i3bar (from left to right)",
            default=[])
        parser.add_argument("-e", "--events", nargs="+",
            help="List of click events that should be handled. Format is: "
            "<module name><splitter, see -s><button ID><splitter><command to execute>",
            default=[])
        parser.add_argument("-l", "--list", action="store_true",
            help="List all available modules and themes")
        parser.add_argument("-t", "--theme", help="Specify which theme to use for "
            "drawing the modules",
            default="default")
        parser.add_argument("-i", "--interval", help="Specify the update interval",
            default=1, type=int)
        parser.add_argument("-s", "--split", help="Specify string to use for "
            "splitting modules and their arguments", default="::")

        return parser

    def print_theme_list(self):
        d = bumblebee.theme.getpath()

        print "available themes:"
        print textwrap.fill(", ".join(
            [ os.path.basename(f).replace(".json", "") for f in glob.iglob("{}/*.json".format(d)) ]
            ),
            80, initial_indent = "    ", subsequent_indent = "    "
        )

    def print_module_list(self):
        print "available modules:"
        path = os.path.dirname(bumblebee.modules.__file__)
        for mod in [ name for _, name, _ in pkgutil.iter_modules([path])]:
            m = importlib.import_module("bumblebee.modules.{}".format(mod))

            desc = "n/a" if not hasattr(m, "description") else getattr(m, "description")()
            usage = "n/a" if not hasattr(m, "usage") else getattr(m, "usage")()
            notes = "n/a" if not hasattr(m, "notes") else getattr(m, "notes")()

            print "    {}: ".format(mod)
            print textwrap.fill("Description: {}".format(desc),
                80, initial_indent="        ", subsequent_indent="                     ")
            print textwrap.fill("Usage      : {}".format(usage),
                80, initial_indent="        ", subsequent_indent="                     ")
            print textwrap.fill("Notes      : {}".format(notes),
                80, initial_indent="        ", subsequent_indent="                     ")
            print ""

class Engine:
    def __init__(self, args):
        self._modules = []
        self._args = args
        self._theme = bumblebee.theme.Theme(args)
        self._output = bumblebee.output.output(args)

    def load_module(self, modulespec):
        name = modulespec.split(self._args.split)[0]
        args = None if name == modulespec else modulespec.split(self._args.split)[1:]
        module = importlib.import_module("bumblebee.modules.{}".format(name))
        return getattr(module, "Module")(self._output, args)

    def load_modules(self):
        for m in self._args.modules:
            self._modules.append(self.load_module(m))

    def register_event(self, eventspec):
        event = eventspec.split(self._args.split)
        if len(event) < 3:
            raise Exception("invalid click event format, expected 3 parameters")
        self._output.add_callback(
            module = event[0],
            button = int(event[1]),
            cmd = event[2],
        )

    def register_events(self):
        for e in self._args.events:
            self.register_event(e)

    def run(self):
        print self._output.start()

        while True:
            # improve this
            self._theme.reset()
            for m in self._modules:
                self._output.add(m, self._theme)
                self._theme.next()
            print self._output.get()
            sys.stdout.flush()
            self._output.wait(self._args.interval)

        print self._output.stop()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
