import argparse
import logging

import util.store
import util.format

log = logging.getLogger(__name__)

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
        parser.add_argument('-a', '--autohide', nargs='+', default=[],
            help='Specify a list of modules to hide when not in warning/error state')
        parser.add_argument('-d', '--debug', action='store_true',
            help='Add debug fields to i3 output')
        parser.add_argument('-f', '--logfile', help='destination for the debug log file, if -d|--debug is specified; defaults to stderr')
        self.__args = parser.parse_args(args)

        parameters = [ item for sub in self.__args.parameters for item in sub ]
        for param in parameters:
            if not '=' in param:
                log.error('missing value for parameter "{}" - ignoring this parameter'.format(param))
                continue
            key, value = param.split('=', 1)
            self.set(key, value)

    def modules(self):
        return [item for sub in self.__args.modules for item in sub]

    def interval(self, default=1):
        return util.format.seconds(self.get('interval', default))

    def debug(self):
        return self.__args.debug

    def logfile(self):
        return self.__args.logfile

    def theme(self):
        return self.__args.theme

    def iconset(self):
        return self.__args.iconset

    def autohide(self, name):
        return name in self.__args.autohide

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
