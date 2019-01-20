# pylint: disable=C0103

"""Theme support"""

import os
import glob
import copy
import json
import io
import re
import logging

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    pass

import bumblebee.error

def theme_path():
    """Return the path of the theme directory"""
    return [
        os.path.dirname("{}/../themes/".format(os.path.dirname(os.path.realpath(__file__)))),
        os.path.dirname(os.path.expanduser("~/.config/bumblebee-status/themes/")),
    ]

def themes():
    themes = {}

    for path in theme_path():
        for filename in glob.iglob("{}/*.json".format(path)):
            if "test" not in filename:
                themes[os.path.basename(filename).replace(".json", "")] = 1
    result = list(themes.keys())
    result.sort()
    return result

class Theme(object):
    """Represents a collection of icons and colors"""
    def __init__(self, name, iconset="auto"):
        self._widget = None
        self._cycle_idx = 0
        self._cycle = {}
        self._prevbg = None
        self._colorset = {}
        self._iconset = iconset

        self.load_symbols()

        data = self.load(name)
        if not data:
            raise bumblebee.error.ThemeLoadError("no such theme")
        self._init(data)

    def load_symbols(self):
        self._symbols = {}
        path = os.path.expanduser("~/.config/bumblebee-status/")
        try:
            os.makedirs(path)
        except Exception:
            pass
        try:
            if os.path.exists("{}/symbols.json".format(path)):
                data = json.load(io.open("{}/symbols.json".format(path)))
                self._symbols = {}
                for icon in data["icons"]:
                    code = int(icon["unicode"], 16)
                    try:
                        code = unichr(code)
                    except Exception:
                        code = chr(code)
                    self._symbols["${{{}}}".format(icon["id"])] = code
                    self._symbols["${{{}}}".format(icon["name"])] = code
        except Exception as e:
            logging.error("failed to load symbols: {}".format(str(e)))

    def _init(self, data):
        """Initialize theme from data structure"""
        self._theme = data
        if self._iconset != "auto":
            self._merge(data, self._load_icons(self._iconset))
        else:
            for iconset in data.get("icons", []):
                self._merge(data, self._load_icons(iconset))
        for colorset in data.get("colors", []):
            self._merge(self._colorset, self._load_colors(colorset))
        self._defaults = data.get("defaults", {})
        self._cycles = self._theme.get("cycle", [])
        self.reset()

    def data(self):
        """Return the raw theme data"""
        return self._theme

    def reset(self):
        """Reset theme to initial state"""
        self._cycle = self._cycles[0] if len(self._cycles) > 0 else {}
        self._cycle_idx = 0
        self._widget = None
        self._prevbg = None

    def icon(self, widget):
        icon = self._get(widget, "icon", None)
        if icon is None:
            return self._get(widget, "prefix", None)

    def padding(self, widget):
        """Return padding for widget"""
        return self._get(widget, "padding", "")

    def prefix(self, widget, default=None):
        """Return the theme prefix for a widget's full text"""
        padding = self.padding(widget)
        pre = self._get(widget, "prefix", None)
        return u"{}{}{}".format(padding, pre, padding) if pre else default

    def symbol(self, widget, name, default=None):
        return self._get(widget, name, default)

    def suffix(self, widget, default=None):
        """Return the theme suffix for a widget's full text"""
        padding = self._get(widget, "padding", "")
        suf = self._get(widget, "suffix", None)
        return u"{}{}{}".format(padding, suf, padding) if suf else default

    def fg(self, widget):
        """Return the foreground color for this widget"""
        return self._get(widget, "fg", None)

    def bg(self, widget):
        """Return the background color for this widget"""
        return self._get(widget, "bg", None)

    def align(self, widget):
        """Return the widget alignment"""
        return self._get(widget, "align", None)

    def minwidth(self, widget):
        """Return the minimum width string for this widget"""
        return self._get(widget, "minwidth", "")

    def separator(self, widget):
        """Return the separator between widgets"""
        return self._get(widget, "separator", None)

    def separator_fg(self, widget):
        """Return the separator's foreground/text color"""
        return self.bg(widget)

    def separator_bg(self, widget):
        """Return the separator's background color"""
        return self._prevbg

    def separator_block_width(self, widget):
        """Return the SBW"""
        return self._get(widget, "separator-block-width", None)

    def _load_wal_colors(self):
        walfile = os.path.expanduser("~/.cache/wal/colors.json")
        result = {}
        with io.open(walfile) as data:
            colors = json.load(data)
            for field in ["special", "colors"]:
                for key in colors[field]:
                    result[key] = colors[field][key]
        return result

    def _load_colors(self, name):
        """Load colors for a theme"""
        try:
            if name == "wal":
                return self._load_wal_colors()
        except Exception as e:
            logging.error("failed to load colors: {}".format(str(e)))

    def _load_icons(self, name):
        """Load icons for a theme"""
        result = {}
        for path in theme_path():
            self._merge(result, self.load(name, path="{}/icons/".format(path)))

        return self._replace_symbols(result)

    def _replace_symbols(self, data):
        rep = json.dumps(data)
        tokens = re.findall(r"\${[^}]+}", rep)
        for token in tokens:
            rep = rep.replace(token, self._symbols[token])
        return json.loads(rep)

    def load(self, name, path=theme_path()):
        """Load and parse a theme file"""
        result = None

        full_name = os.path.expanduser(name)
        if os.path.isfile(full_name):
            path = os.path.dirname(full_name)
            name = os.path.basename(full_name)
            name,_,_ = name.rpartition(".json")
            return self.load(name, path)

        if not isinstance(path, list):
            path = [path]
        for p in path:
            themefile = "{}/{}.json".format(p, name)

            if os.path.isfile(themefile):
                try:
                    with io.open(themefile, encoding="utf-8") as data:
                        if result is None:
                            result = json.load(data)
                        else:
                            self._merge(result, json.load(data))
                except ValueError as exception:
                    raise bumblebee.error.ThemeLoadError("JSON error: {}".format(exception))

        return result

    def _get(self, widget, name, default=None):
        """Return the config value 'name' for 'widget'"""

        if not self._widget:
            self._widget = widget

        if self._widget != widget:
            self._prevbg = self.bg(self._widget)
            self._widget = widget
            if len(self._cycles) > 0:
                self._cycle_idx = (self._cycle_idx + 1) % len(self._cycles)
                self._cycle = self._cycles[self._cycle_idx]

        module_theme = self._theme.get(widget.module, {})
        class_theme = self._theme.get(widget.cls(), {})

        state_themes = []
        # avoid infinite recursion
        states = widget.state()
        if name not in states:
            for state in states:
                state_themes.append(self._get(widget, state, {}))

        value = self._defaults.get(name, default)
        value = widget.get("theme.{}".format(name), value)
        value = self._cycle.get(name, value)
        value = class_theme.get(name, value)
        value = module_theme.get(name, value)

        for theme in state_themes:
            value = theme.get(name, value)

        if isinstance(value, list):
            key = "{}-idx".format(name)
            idx = widget.get(key, 0)
            widget.set(key, (idx + 1) % len(value))
            value = value[idx]

        mod = widget.get_module()
        if mod and not mod.parameter("is-unittest"):
            value = widget.get_module().parameter("theme.{}".format(name), value)

        if isinstance(value, list) or isinstance(value, dict):
            return value
        return self._colorset.get(value, value)

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
                if not key in target:
                    target[key] = copy.deepcopy(value)
        return target

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
