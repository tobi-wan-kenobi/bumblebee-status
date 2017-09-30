# -*- coding: utf-8 -*-

"""
    xkbgroup.version
    ~~~~~~~~~~~~~~~~

    This module collects all version-related utilities.

    Global variables:
    * VERSION: current version of this library.

    Functions:
    * print_version: pretty prints current version.

    :copyright: (c) 2016 by Nguyen Duc My.
    :license: MIT, see LICENSE for more details.
"""


VERSION = "0.1.4.3"

def print_version(progname):
    """Prints the version along with the specified program name."""
    print("{} {}".format(progname, VERSION))


__all__ = ["VERSION", "print_version"]
