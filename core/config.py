import argparse

MODULE_HELP = "Specify a space-separated list of modules to load. The order of the list determines their order in the i3bar (from left to right). Use <module>:<alias> to provide an alias in case you want to load the same module multiple times, but specify different parameters."

class Config(object):
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='bumblebee-status is a modular, theme-able status line generator for the i3 window manager. https://github.com/tobi-wan-kenobi/bumblebee-status/wiki')
        parser.add_argument("-m", "--modules", nargs="+", action='append', default=[],
            help=MODULE_HELP)
        self._args = parser.parse_args(args)

    def modules(self):
        return [item for sub in self._args.modules for item in sub]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
