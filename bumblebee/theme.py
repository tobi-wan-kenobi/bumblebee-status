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
        theme = self.load(name)
        self._init(self.load(name))

    def _init(self, data):
        """Initialize theme from data structure"""
        self._defaults = data.get("defaults", {})

    def prefix(self, widget):
        """Return the theme prefix for a widget's full text"""
        return self._get(widget, "prefix", None)

    def suffix(self, widget):
        """Return the theme suffix for a widget's full text"""
        return self._get(widget, "suffix", None)

    def loads(self, data):
        theme = json.loads(data)
        self._init(theme)

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

    def _get(self, widget, name,default=None):
        value = default
        value = self._defaults.get(name, value)

        return value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
