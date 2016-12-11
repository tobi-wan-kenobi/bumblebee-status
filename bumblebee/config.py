"""Configuration handling

This module provides configuration information (loaded modules,
module parameters, etc.) to all other components
"""

import argparse
import bumblebee.store

MODULE_HELP = ""
THEME_HELP = ""
PARAMETER_HELP = ""

def create_parser():
    """Create the argument parser"""
    parser = argparse.ArgumentParser(description="display system data in the i3bar")
    parser.add_argument("-m", "--modules", nargs="+", default=[],
        help=MODULE_HELP)
    parser.add_argument("-t", "--theme", default="default", help=THEME_HELP)
    parser.add_argument("-p", "--parameters", nargs="+", default=[],
        help=PARAMETER_HELP)
    return parser

class Config(bumblebee.store.Store):
    """Top-level configuration class

    Parses commandline arguments and provides non-module
    specific configuration information.
    """
    def __init__(self, args=None):
        super(Config, self).__init__()
        parser = create_parser()
        self._args = parser.parse_args(args if args else [])

        for param in self._args.parameters:
            key, value = param.split("=")
            self.set(key, value)

    def modules(self):
        """Return a list of all activated modules"""
        return [{
            "module": x.split(":")[0],
            "name": x if not ":" in x else x.split(":")[1],
        } for x in self._args.modules]

    def theme(self):
        """Return the name of the selected theme"""
        return self._args.theme

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
