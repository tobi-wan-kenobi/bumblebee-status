import os
import io
import json
import logging
import copy
import glob

import core.event
import util.algorithm
import util.xresources

log = logging.getLogger(__name__)

THEME_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PATHS = [
    ".",
    os.path.join(THEME_BASE_DIR, "../../themes")
]

if os.environ.get("XDG_DATA_DIRS"):
    PATHS.extend([
        os.path.join(p, "bumblebee-status/themes") for p in os.environ["XDG_DATA_DIRS"].split(":")
    ])

PATHS.extend([
    os.path.expanduser("~/.config/bumblebee-status/themes"),
    os.path.expanduser("~/.local/share/bumblebee-status/themes"),  # PIP
    "/usr/share/bumblebee-status/themes",
])


def themes():
    themes_dict = {}

    for path in PATHS:
        for filename in glob.iglob("{}/*.json".format(path)):
            if "test" not in filename:
                themes_dict[os.path.basename(filename).replace(".json", "")] = 1
    result = list(themes_dict.keys())
    result.sort()
    return result


def merge_replace(value, new_value, key):
    if not isinstance(value, dict):
        return new_value
    if isinstance(new_value, dict):
        return util.algorithm.merge(new_value, value)
    # right now, merging needs explicit pango support :(
    if "pango" in value:
        value["pango"]["full_text"] = new_value
    return value


class Theme(object):
    def __init__(self, name="default", iconset="auto", raw_data=None):
        self.name = name
        self.__widget_count = 0
        self.__previous = {}
        self.__current = {}
        self.__keywords = {}
        self.__value_idx = {}
        self.__data = raw_data if raw_data else self.load(name)

        for icons in self.__data.get("icons", []):
            self.__data = util.algorithm.merge(self.__data, self.load(icons, "icons"))
        if iconset != "auto":
            self.__data = util.algorithm.merge(self.load(iconset, "icons"), self.__data)
        for colors in self.__data.get("colors", []):
            util.algorithm.merge(self.__keywords, self.load_keywords(colors))

        core.event.register("draw", self.__start)
        core.event.register("next-widget", self.__next_widget)

    def keywords(self):
        return self.__keywords

    def color(self, name, default=None):
        return self.keywords().get(name, default)

    def load(self, name, subdir=""):
        if isinstance(name, dict):
            return name  # support plain data
        for path in PATHS:
            theme_file = os.path.join(path, subdir, "{}.json".format(name))
            result = self.__load_json(theme_file)
            if result != {}:
                return result
        raise RuntimeError("unable to find theme {}".format(name))

    def __load_json(self, filename):
        filename = os.path.expanduser(filename)
        if not os.path.isfile(filename):
            return {}
        with io.open(filename) as data:
            return json.load(data)

    def load_keywords(self, name):
        try:
            if isinstance(name, dict):
                return name

            result = {}
            if name.lower() == "wal":
                wal = self.__load_json("~/.cache/wal/colors.json")
                for field in ["special", "colors"]:
                    for key in wal.get(field, {}):
                        result[key] = wal[field][key]
            if name.lower() == "xresources":
                for key in ("background", "foreground"):
                    result[key] = xresources.query(key)
                for i in range(16):
                    key = color + str(i)
                    result[key] = xresources.query(key)

            return result
        except Exception as e:
            log.error("failed to load colors: {}", e)

    def __start(self):
        self.__widget_count = 0
        self.__current.clear()
        self.__previous.clear()

        for key, value in self.__value_idx.items():
            self.__value_idx[key] = value + 1

    def __next_widget(self):
        self.__widget_count = self.__widget_count + 1
        self.__previous = dict(self.__current)
        self.__current.clear()

    def get(self, key, widget=None, default=None):
        if not widget:
            widget = core.widget.Widget("")
        # special handling
        if widget == "previous":
            return self.__previous.get(key, None)

        value = default

        for option in ["defaults", "cycle"]:
            if option in self.__data:
                tmp = self.__data[option]
                if isinstance(tmp, list):
                    tmp = tmp[self.__widget_count % len(tmp)]
                value = merge_replace(value, tmp.get(key, value), key)

        if isinstance(value, dict):
            value = copy.deepcopy(value)

        value = merge_replace(value, self.__data.get(key, value), key)

        if widget.module:
            value = merge_replace(
                value, self.get(widget.module.name, None, {}).get(key, value), key
            )
            value = merge_replace(
                value, self.get(widget.module.id, None, {}).get(key, value), key
            )

        if not key in widget.state():
            for state in widget.state():
                theme = self.get(state, widget, {})
                value = merge_replace(value, theme.get(key, value), key)

        if not type(value) in (list, dict):
            value = self.__keywords.get(value, value)

        if isinstance(value, list):
            idx = self.__value_idx.get("{}::{}".format(widget.id, key), 0) % len(value)
            self.__value_idx["{}::{}".format(widget.id, key)] = idx
            widget.set(key, idx)
            value = value[idx]
        self.__current[key] = value
        return value


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
