import os
import json
import glob

def getpath():
    return os.path.dirname("{}/themes/".format(os.path.dirname(os.path.realpath(__file__))))

def themes():
    d = getpath()
    return [ os.path.basename(f).replace(".json", "") for f in glob.iglob("{}/*.json".format(d)) ]

class Theme:
    def __init__(self, config):
        self._config = config
        with open("{}/{}.json".format(getpath(), config.theme())) as f:
            self._data = json.load(f)
        self._defaults = self._data.get("defaults", {})
        self._cycles = self._defaults.get("cycle", [])
        self.begin()

    def begin(self):
        self._config.set("theme.cycleidx", 0)
        self._cycle = self._cycles[0] if len(self._cycles) > 0 else {}
        self._background = [ None, None ]

    def next_widget(self):
        self._background[1] = self._background[0]
        idx = self._config.increase("theme.cycleidx", len(self._cycles), 0)
        self._cycle = self._cycles[idx] if len(self._cycles) > idx else {}

    def prefix(self, widget):
        return self._get(widget, "prefix")

    def suffix(self, widget):
        return self._get(widget, "suffix")

    def color(self, widget):
        result = self._get(widget, "fg")
        if widget.warning():
            result = self._get(widget, "fg-warning")
        if widget.critical():
            result = self._get(widget, "fg-critical")
        return result

    def background(self, widget):
        result = self._get(widget, "bg")
        if widget.warning():
            result = self._get(widget, "bg-warning")
        if widget.critical():
            result = self._get(widget, "bg-critical")
        self._background[0] = result
        return result

    def separator(self, widget):
        return self._get(widget, "separator")

    def default_separators(self, widget):
        return self._get(widget, "default-separators")

    def separator_color(self, widget):
        return self.background(widget)

    def separator_background(self, widget):
        return self._background[1]

    def separator_block_width(self, widget):
        return self._get(widget, "separator-block-width")

    def _get(self, widget, name):
        module = widget.module()
        state = widget.state()
        module_theme = self._data.get(module, {})
        state_theme = module_theme.get("states", {}).get(state, {})

        value = None
        value = self._defaults.get(name, value)
        value = self._cycle.get(name, value)
        value = module_theme.get(name, value)
        value = state_theme.get(name, value)

        if type(value) is list:
            key = "{}{}".format(repr(widget), value)
            idx = self._config.parameter(key, 0)
            self._config.increase(key, len(value), 0)
            value = value[idx]

        return value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
