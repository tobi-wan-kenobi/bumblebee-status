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
