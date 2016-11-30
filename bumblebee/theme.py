import os
import copy
import json
import yaml
import glob

def getpath():
    return os.path.dirname("{}/../themes/".format(os.path.dirname(os.path.realpath(__file__))))

def themes():
    d = getpath()
    return [ os.path.basename(f).replace(".json", "") for f in glob.iglob("{}/*.json".format(d)) ]

class Theme:
    def __init__(self, config):
        self._config = config

        self._data = self.get_theme(config.theme())

        for iconset in self._data.get("icons", []):
            self.merge(self._data, self.get_theme(iconset))

        self._defaults = self._data.get("defaults", {})
        self._cycles = self._defaults.get("cycle", [])
        self.begin()

    def get_theme(self, name):
        for path in [ getpath(), "{}/icons/".format(getpath()) ]:
            if os.path.isfile("{}/{}.yaml".format(path, name)):
                with open("{}/{}.yaml".format(path, name)) as f:
                    return yaml.load(f)
            if os.path.isfile("{}/{}.json".format(path, name)):
                with open("{}/{}.json".format(path, name)) as f:
                    return json.load(f)
        return None

    # algorithm copied from
    # http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts
    # nicely done :)
    def merge(self, target, *args):
        if len(args) > 1:
            for item in args:
                self.merge(item)
            return target

        item = args[0]
        if not isinstance(item, dict):
            return item
        for key, value in item.items():
            if key in target and isinstance(target[key], dict):
                self.merge(target[key], value)
            else:
                target[key] = copy.deepcopy(value)
        return target

    def begin(self):
        self._config.set("theme.cycleidx", 0)
        self._cycle = self._cycles[0] if len(self._cycles) > 0 else {}
        self._background = [ None, None ]

    def next_widget(self):
        self._background[1] = self._background[0]
        idx = self._config.increase("theme.cycleidx", len(self._cycles), 0)
        self._cycle = self._cycles[idx] if len(self._cycles) > idx else {}

    def prefix(self, widget):
        return self._get(widget, "prefix", "")

    def suffix(self, widget):
        return self._get(widget, "suffix", "")

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

    def _get(self, widget, name, default = None):
        module = widget.module()
        state = widget.state()
        inst = widget.instance()
        inst = inst.replace("{}.".format(module), "")
        module_theme = self._data.get(module, {})
        state_theme = module_theme.get("states", {}).get(state, {})
        instance_theme = module_theme.get(inst, {})
        instance_state_theme = instance_theme.get("states", {}).get(state, {})

        value = None
        value = self._defaults.get(name, value)
        value = self._cycle.get(name, value)
        value = module_theme.get(name, value)
        value = state_theme.get(name, value)
        value = instance_theme.get(name, value)
        value = instance_state_theme.get(name, value)

        if type(value) is list:
            key = "{}{}".format(repr(widget), value)
            idx = self._config.parameter(key, 0)
            self._config.increase(key, len(value), 0)
            value = value[idx]

        return value if value else default

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
