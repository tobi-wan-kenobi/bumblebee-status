# pylint: disable=C0103

"""Theme support"""

import os
import copy
import json

import bumblebee.error

def theme_path():
    """Return the path of the theme directory"""
    return os.path.dirname("{}/../themes/".format(os.path.dirname(os.path.realpath(__file__))))

class Theme(object):
    """Represents a collection of icons and colors"""
    def __init__(self, name):
        self._init(self.load(name))

    def _init(self, data):
        """Initialize theme from data structure"""
        for iconset in data.get("icons", []):
            self._merge(data, self._load_icons(iconset))
        self._theme = data
        self._defaults = data.get("defaults", {})

    def prefix(self, widget):
        """Return the theme prefix for a widget's full text"""
        return self._get(widget, "prefix", None)

    def suffix(self, widget):
        """Return the theme suffix for a widget's full text"""
        return self._get(widget, "suffix", None)

    def fg(self, widget):
        """Return the foreground color for this widget"""
        return self._get(widget, "fg", None)

    def bg(self, widget):
        """Return the background color for this widget"""
        return self._get(widget, "bg", None)

    def loads(self, data):
        """Initialize the theme from a JSON string"""
        theme = json.loads(data)
        self._init(theme)

    def _load_icons(self, name):
        """Load icons for a theme"""
        path = "{}/icons/".format(theme_path())
        return self.load(name, path=path)

    def load(self, name, path=theme_path()):
        """Load and parse a theme file"""
        themefile = "{}/{}.json".format(path, name)

        if os.path.isfile(themefile):
            try:
                with open(themefile) as data:
                    return json.load(data)
            except ValueError as exception:
                raise bumblebee.error.ThemeLoadError("JSON error: {}".format(exception))
        else:
            raise bumblebee.error.ThemeLoadError("no such theme: {}".format(name))

    def _get(self, widget, name, default=None):
        """Return the config value 'name' for 'widget'"""
        module_theme = self._theme.get(widget.module, {})

        padding = None
        if name != "padding":
            padding = self._get(widget, "padding")

        value = self._defaults.get(name, default)
        value = module_theme.get(name, value)

        if value and padding:
            value = u"{}{}{}".format(padding, value, padding)

        return value

    # algorithm copied from
    # http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts
    # nicely done :)
    def _merge(self, target, *args):
        """Merge two arbitrarily nested data structures"""
        if len(args) > 1:
            for item in args:
                self._merge(item)
            return target

        item = args[0]
        if not isinstance(item, dict):
            return item
        for key, value in item.items():
            if key in target and isinstance(target[key], dict):
                self._merge(target[key], value)
            else:
                target[key] = copy.deepcopy(value)
        return target

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
