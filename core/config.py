import argparse

import util.store

MODULE_HELP = 'Specify a space-separated list of modules to load. The order of the list determines their order in the i3bar (from left to right). Use <module>:<alias> to provide an alias in case you want to load the same module multiple times, but specify different parameters.'
PARAMETER_HELP = 'Provide configuration parameters in the form of <module>.<key>=<value>'
THEME_HELP = 'Specify the theme to use for drawing modules'

class Config(util.store.Store):
    def __init__(self, args):
        super(Config, self).__init__()

        parser = argparse.ArgumentParser(description='bumblebee-status is a modular, theme-able status line generator for the i3 window manager. https://github.com/tobi-wan-kenobi/bumblebee-status/wiki')
        parser.add_argument('-m', '--modules', nargs='+', action='append', default=[],
            help=MODULE_HELP)
        parser.add_argument('-p', '--parameters', nargs='+', action='append', default=[],
            help=PARAMETER_HELP)
        parser.add_argument('-t', '--theme', default='default', help=THEME_HELP)
        parser.add_argument('-i', '--iconset', default='auto',
            help='Specify the name of an iconset to use (overrides theme default)')
        self._args = parser.parse_args(args)

        parameters = [ item for sub in self._args.parameters for item in sub ]
        for param in parameters:
            key, value = param.split('=', 1)
            self.set(key, value)

    def modules(self):
        return [item for sub in self._args.modules for item in sub]

    def interval(self):
        return float(self.get('interval', 1))

    def theme(self):
        return self._args.theme

    def iconset(self):
        return self._args.iconset

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
