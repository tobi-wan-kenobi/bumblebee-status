"""Configuration handling

This module provides configuration information (loaded modules,
module parameters, etc.) to all other components
"""

import argparse

MODULE_HELP = ""

def create_parser():
    """Create the argument parser"""
    parser = argparse.ArgumentParser(description="display system data in the i3bar")
    parser.add_argument("-m", "--modules", nargs="+", default=[],
                        help=MODULE_HELP)
    return parser

class Config(object):
    """Top-level configuration class

    Parses commandline arguments and provides non-module
    specific configuration information.
    """
    def __init__(self, args=None):
        parser = create_parser()
        self._args = parser.parse_args(args if args else [])

    def modules(self):
        """Return a list of all activated modules"""
        return [{
            "module": x.split(":")[0],
            "name": x if not ":" in x else x.split(":")[1],
        } for x in self._args.modules]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
