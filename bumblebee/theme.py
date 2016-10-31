import os
import json

class Theme:
    def __init__(self, name="default"):
        self._data = None
        path = os.path.dirname(os.path.realpath(__file__))
        with open("%s/themes/%s.json" % (path, name)) as f:
            self._data = json.load(f)
        self._defaults = self._data.get("defaults", {})

    def _gettheme(self, obj, key):
        module = obj.__module__.split(".")[-1]
        module_theme = self._data.get(module, {})

        value = getattr(obj, key)() if hasattr(obj, key) else ""
        value = self._defaults.get(key, value)
        value = module_theme.get(key, value)

        return value

    def prefix(self, obj):
        return self._gettheme(obj, "prefix")

    def suffix(self, obj):
        return self._gettheme(obj, "suffix")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
