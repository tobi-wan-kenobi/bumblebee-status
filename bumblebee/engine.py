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
    def __init__(self, config):
        self._modules = []
        self._config = config
        self._theme = bumblebee.theme.Theme(config)
        self._output = bumblebee.output.output(config)

    def load_module(self, name):
        module = importlib.import_module("bumblebee.modules.{}".format(name))
        return getattr(module, "Module")(self._output, self._config)

    def load_modules(self):
        for m in self._config.modules():
            self._modules.append(self.load_module(m))

    def register_event(self, eventspec):
        return
        # TODO
        event = eventspec.split(self._args.split)
        if len(event) < 3:
            raise Exception("invalid click event format, expected 3 parameters")
        self._output.add_callback(
            module = event[0],
            button = int(event[1]),
            cmd = event[2],
        )

    def register_events(self):
        return
        # TODO
        for e in self._args.events:
            self.register_event(e)

    def run(self):
        self._output.start()

        while True:
            self._theme.begin()
            for m in self._modules:
                self._output.draw(m.widgets(), self._theme)
            self._output.flush()
            self._output.wait()

        self._output.stop()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
