import sys
import json
import time
import threading

import core.theme
import core.event

import util.format


def dump_json(obj):
    return obj.dict()


def assign(src, dst, key, src_key=None, default=None):
    if not src_key:
        if key.startswith("_"):
            src_key = key
        else:
            src_key = key.replace("_", "-")  # automagically replace _ with -

    for k in src_key if isinstance(src_key, list) else [src_key]:
        if k in src:
            dst[key] = src[k]
            return
    if default is not None:
        dst[key] = default


class block(object):
    __COMMON_THEME_FIELDS = [
        "separator",
        "separator-block-width",
        "default-separators",
        "border-top",
        "border-left",
        "border-right",
        "border-bottom",
        "fg",
        "bg",
        "padding",
        "prefix",
        "suffix",
    ]

    def __init__(self, theme, module, widget):
        self.__attributes = {}
        for key in self.__COMMON_THEME_FIELDS:
            tmp = theme.get(key, widget)
            if tmp is not None:
                self.__attributes[key] = tmp

        self.__attributes["name"] = module.id
        self.__attributes["instance"] = widget.id
        self.__attributes["prev-bg"] = theme.get("bg", "previous")

    def set(self, key, value):
        self.__attributes[key] = value

    def get(self, key, default=None):
        return self.__attributes.get(key, default)

    def is_pango(self, attr):
        if isinstance(attr, dict) and "pango" in attr:
            return True
        return False

    def pangoize(self, text):
        if not self.is_pango(text):
            return text
        self.__attributes["markup"] = "pango"
        attr = dict(text["pango"])
        text = attr.get("full_text", "")
        if "full_text" in attr:
            del attr["full_text"]
        result = "<span"
        for key, value in attr.items():
            result = '{} {}="{}"'.format(result, key, value)
        result = "{}>{}</span>".format(result, text)
        return result

    def dict(self):
        result = {}

        assign(self.__attributes, result, "full_text", ["full_text", "separator"])
        assign(self.__attributes, result, "separator", "default-separators")

        if "_decorator" in self.__attributes:
            assign(self.__attributes, result, "color", "bg")
            assign(self.__attributes, result, "background", "prev-bg")
            result["_decorator"] = True
        else:
            assign(self.__attributes, result, "color", "fg")
            assign(self.__attributes, result, "background", "bg")

        if "full_text" in self.__attributes:
            prefix = self.__pad(self.pangoize(self.__attributes.get("prefix")))
            suffix = self.__pad(self.pangoize(self.__attributes.get("suffix")))
            self.set("_prefix", prefix)
            self.set("_suffix", suffix)
            self.set("_raw", self.get("full_text"))
            result["full_text"] = self.pangoize(result["full_text"])
            result["full_text"] = self.__format(self.__attributes["full_text"])

        if "min-width" in self.__attributes and "padding" in self.__attributes:
            self.set("min-width", self.__format(self.get("min-width")))

        for k in [
            "name",
            "instance",
            "separator_block_width",
            "border",
            "border_top",
            "border_bottom",
            "border_left",
            "border_right",
            "markup",
            "_raw",
            "_suffix",
            "_prefix",
            "min_width",
            "align",
        ]:
            assign(self.__attributes, result, k)

        return result

    def __pad(self, text):
        padding = self.__attributes.get("padding", "")
        if not text:
            return padding
        return "{}{}{}".format(padding, text, padding)

    def __format(self, text):
        if text is None:
            return None
        prefix = self.get("_prefix")
        suffix = self.get("_suffix")
        return "{}{}{}".format(prefix, text, suffix)


class i3(object):
    def __init__(self, theme=core.theme.Theme(), config=core.config.Config([])):
        self.__modules = []
        self.__content = {}
        self.__theme = theme
        self.__config = config
        self.__offset = 0
        self.__lock = threading.Lock()
        core.event.register("update", self.update)
        core.event.register("start", self.draw, "start")
        core.event.register("draw", self.draw, "statusline")
        core.event.register("stop", self.draw, "stop")
        core.event.register("output.scroll-left", self.scroll_left)
        core.event.register("output.scroll-right", self.scroll_right)

    def content(self):
        return self.__content

    def theme(self, new_theme=None):
        if new_theme:
            self.__theme = new_theme
        return self.__theme

    def modules(self, modules=None):
        if not modules:
            return self.__modules
        self.__modules = modules if isinstance(modules, list) else [modules]

    def toggle_minimize(self, event):
        widget_id = event["instance"]

        for module in self.__modules:
            if module.widget(widget_id=widget_id) and util.format.asbool(module.parameter("minimize", False)) == True:
                # this module can customly minimize
                module.minimized = not module.minimized
                return

        if widget_id in self.__content:
            self.__content[widget_id]["minimized"] = not self.__content[widget_id]["minimized"]

    def draw(self, what, args=None):
        with self.__lock:
            cb = getattr(self, what)
            data = cb(args) if args else cb()
            if "blocks" in data:
                sys.stdout.write(json.dumps(data["blocks"], default=dump_json))
            if "suffix" in data:
                sys.stdout.write(data["suffix"])
            sys.stdout.write("\n")
            sys.stdout.flush()

    def start(self):
        return {
            "blocks": {"version": 1, "click_events": True},
            "suffix": "\n[",
        }

    def stop(self):
        return {"suffix": "\n]"}

    def separator_block(self, module, widget):
        if not self.__theme.get("separator"):
            return []
        blk = block(self.__theme, module, widget)
        blk.set("_decorator", True)
        return [blk]

    def __content_block(self, module, widget):
        blk = block(self.__theme, module, widget)
        minwidth = widget.theme("minwidth")
        if minwidth is not None:
            try:
                blk.set("min-width", "-" * int(minwidth))
            except:
                blk.set("min-width", minwidth)
        blk.set("align", widget.theme("align"))
        blk.set("full_text", "\u2026" if self.__content[widget.id]["minimized"] else self.__content[widget.id]["text"])
        if widget.get("pango", False):
            blk.set("markup", "pango")
        if self.__config.debug():
            state = module.state(widget)
            if isinstance(state, list):
                state = ", ".join(state)
            blk.set("__state", state)
        return blk

    def scroll_left(self):
        if self.__offset > 0:
            self.__offset -= 1

    def scroll_right(self):
        self.__offset += 1

    def blocks(self, module):
        blocks = []
        if module.minimized:
            blocks.extend(self.separator_block(module, module.widgets()[0]))
            blocks.append(self.__content_block(module, module.widgets()[0]))
            self.__widgetcount += 1
            return blocks

        width = self.__config.get("output.width", 0)
        for widget in module.widgets():
            if module.scroll() == True and width > 0:
                self.__widgetcount += 1
                if self.__widgetcount-1 < self.__offset:
                    continue
                if self.__widgetcount-1 >= self.__offset + width:
                    continue
            if widget.module and self.__config.autohide(widget.module.name):
                if not any(
                    state in widget.state() for state in ["warning", "critical", "no-autohide"]
                ):
                    continue
            if module.hidden():
                continue
            if widget.hidden:
                continue
            if "critical" in widget.state() and self.__config.errorhide(widget.module.name):
                continue
            blocks.extend(self.separator_block(module, widget))
            blocks.append(self.__content_block(module, widget))
            core.event.trigger("next-widget")
        core.event.trigger("output.done", self.__offset, self.__widgetcount)
        return blocks

    def update(self, affected_modules=None, redraw_only=False, force=False):
        with self.__lock:
            self.update2(affected_modules, redraw_only, force)

    def update2(self, affected_modules=None, redraw_only=False, force=False):
        now = time.time()
        for module in self.__modules:
            if affected_modules and not module.id in affected_modules:
                continue
            if not affected_modules and module.next_update:
                if now < module.next_update and not force:
                    continue

            if not redraw_only:
                module.update_wrapper()
                if module.parameter("interval", "") != "never":
                    module.next_update = now + util.format.seconds(
                        module.parameter("interval", self.__config.interval())
                    )
                else:
                    module.next_update = sys.maxsize
            for widget in module.widgets():
                if not widget.id in self.__content:
                    self.__content[widget.id] = { "minimized": False }
                self.__content[widget.id]["text"] = widget.full_text()

    def statusline(self):
        blocks = []
        self.__widgetcount = 0
        for module in self.__modules:
            blocks.extend(self.blocks(module))
        return {"blocks": blocks, "suffix": ","}

    def wait(self, interval):
        time.sleep(interval)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
