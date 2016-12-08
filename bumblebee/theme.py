"""Theme support"""

import os
import json

import bumblebee.error

def theme_path():
    """Return the path of the theme directory"""
    return os.path.dirname("{}/../themes/".format(os.path.dirname(os.path.realpath(__file__))))

class Theme(object):
    """Represents a collection of icons and colors"""
    def __init__(self, name):
        self._theme = self.load(name)

    def load(self, name):
        """Load and parse a theme file"""
        path = theme_path()
        themefile = "{}/{}.json".format(path, name)
        if os.path.isfile(themefile):
            try:
                with open(themefile) as data:
                    return json.load(data)
            except ValueError as exception:
                raise bumblebee.error.ThemeLoadError("JSON error: {}".format(exception))
        else:
            raise bumblebee.error.ThemeLoadError("no such theme: {}".format(name))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
