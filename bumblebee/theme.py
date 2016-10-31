import os
import json

class Theme:
    def __init__(self, name="default"):
        self._data = None
        path = os.path.dirname(os.path.realpath(__file__))
        with open("{}/themes/{}.json".format(path, name)) as f:
            self._data = json.load(f)
        self._defaults = self._data.get("defaults", {})

    def _gettheme(self, obj, key):
        module = obj.__module__.split(".")[-1]
        module_theme = self._data.get(module, {})

        value = getattr(obj, key)() if hasattr(obj, key) else None
        value = self._defaults.get(key, value)
        value = module_theme.get(key, value)

        if hasattr(obj, "state"):
            state = getattr(obj, "state")()
            state_theme = module_theme.get("states", {}).get(state, {})

            value = state_theme.get(key, value)

        return value

    def color(self, obj):
        return self._gettheme(obj, "fg")

    def background(self, obj):
        return self._gettheme(obj, "bg")

    def default_separators(self, obj):
        return self._gettheme(obj, "default_separators")

    def prefix(self, obj):
        return self._gettheme(obj, "prefix")

    def suffix(self, obj):
        return self._gettheme(obj, "suffix")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
