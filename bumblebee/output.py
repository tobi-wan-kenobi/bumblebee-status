# pylint: disable=R0201

"""Output classes"""

import sys
import json
import uuid
import logging

import bumblebee.store
import bumblebee.util

MAX_PERCENTS = 100.
CHARS = 8
HBARS = [
    u"\u2581",
    u"\u2582",
    u"\u2583",
    u"\u2584",
    u"\u2585",
    u"\u2586",
    u"\u2587",
    u"\u2588"]
VBARS = [
    u"\u258f",
    u"\u258e",
    u"\u258d",
    u"\u258c",
    u"\u258b",
    u"\u258a",
    u"\u2589",
    u"\u2588"]

log = logging.getLogger(__name__)

def scrollable(func):
    def wrapper(module, widget):
        text = func(module, widget)
        if not text:
            return text
        width = widget.get("theme.width", int(module.parameter("width", 30)))
        if bumblebee.util.asbool(module.parameter("scrolling.makewide", "true")):
            widget.set("theme.minwidth", "A"*width)
        if width < 0:
            return text
        if len(text) <= width:
            return text
        # we need to shorten

        try:
            bounce = int(module.parameter("scrolling.bounce", 1))
        except ValueError:
            bounce = 1
        try:
            scroll_speed = int(module.parameter("scrolling.speed", 1))
        except ValueError:
            scroll_speed = 1
        start = widget.get("scrolling.start", -1)
        direction = widget.get("scrolling.direction", "right")
        start += scroll_speed if direction == "right" else -(scroll_speed)

        if width + start > len(text) + (scroll_speed -1):
            if bounce:
                widget.set("scrolling.direction", "left")
            else:
                start = 0
        elif start <= 0:
            if bounce:
                widget.set("scrolling.direction", "right")
            else:
                start = len(text)
        widget.set("scrolling.start", start)
        text = text[start:width+start]

        return text
    return wrapper


class Bar(object):
    """superclass"""
    bars = None

    def __init__(self, value):
        """
            Args:

                value (float): value between 0. and 100. meaning percents
        """
        self.value = value


class HBar(Bar):
    """horizontal bar (1 char)"""
    bars = HBARS

    def __init__(self, value):
        """
            Args:

                value (float): value between 0. and 100. meaning percents
        """
        super(HBar, self).__init__(value)
        self.step = MAX_PERCENTS / CHARS

    def get_char(self):
        """
            Decide which char to draw

            Return: str
        """
        for i in range(CHARS):
            left = i * self.step
            right = (i + 1) * self.step
            if left <= self.value < right:
                return self.bars[i]
        return self.bars[-1]


def hbar(value):
    """wrapper function"""
    return HBar(value).get_char()


class VBar(Bar):
    """vertical bar (can be more than 1 char)"""
    bars = VBARS

    def __init__(self, value, width=1):
        """
            Args:

                value (float): value between 0. and 100. meaning percents

                width (int): width
        """
        super(VBar, self).__init__(value)
        self.step = MAX_PERCENTS / (CHARS * width)
        self.width = width

    def get_chars(self):
        """
            Decide which char to draw

            Return: str
        """
        if self.value == 100:
            return self.bars[-1] * self.width
        if self.width == 1:
            for i in range(CHARS):
                left = i * self.step
                right = (i + 1) * self.step
                if left <= self.value < right:
                    return self.bars[i]
        else:
            full_parts = int(self.value // (self.step * CHARS))
            remainder = self.value - full_parts * self.step * CHARS
            empty_parts = self.width - full_parts
            if remainder >= 0:
                empty_parts -= 1
            part_vbar = VBar(remainder * self.width)  # scale to width
            chars = self.bars[-1] * full_parts
            chars += part_vbar.get_chars()
            chars += " " * empty_parts
            return chars


def vbar(value, width):
    """wrapper function"""
    return VBar(value, width).get_chars()


class Widget(bumblebee.store.Store):
    """Represents a single visible block in the status bar"""
    def __init__(self, full_text="", name=""):
        super(Widget, self).__init__()
        self._full_text = full_text
        self.module = None
        self._module = None
        self._minimized = False
        self.name = name
        self.id = str(uuid.uuid4())

    def get_module(self):
        return self._module

    def toggle_minimize(self):
        self._minimized = not self._minimized

    def link_module(self, module):
        """Set the module that spawned this widget

        This is done outside the constructor to avoid having to
        pass in the module name in every concrete module implementation"""
        self.module = module.name
        self._module = module

    def cls(self):
        if not self._module:
            return None
        return self._module.__module__.replace("bumblebee.modules.", "")

    def state(self):
        """Return the widget's state"""
        if self._module and hasattr(self._module, "state"):
            states = self._module.state(self)
            if not isinstance(states, list):
                return [states]
            return states
        return []

    def full_text(self, value=None):
        """Set or retrieve the full text to display in the widget"""
        if value:
            self._full_text = value
        else:
            if self._minimized:
                return u"\u2026"
            if callable(self._full_text):
                return self._full_text(self)
            else:
                return self._full_text

class I3BarOutput(object):
    """Manage output according to the i3bar protocol"""
    def __init__(self, theme, config=None):
        self._theme = theme
        self._widgets = []
        self._started = False
        self._config = config

    def started(self):
        return self._started

    def start(self):
        """Print start preamble for i3bar protocol"""
        self._started = True
        sys.stdout.write(json.dumps({"version": 1, "click_events": True}) + "\n[\n")

    def stop(self):
        """Finish i3bar protocol"""
        sys.stdout.write("]\n")

    def draw(self, widget, module=None, engine=None):
        """Draw a single widget"""
        full_text = widget.full_text()
        if widget.get_module() and widget.get_module().hidden():
            return
        if widget.get_module() and widget.get_module().name in self._config.autohide():
            if not any(state in widget.state() for state in ["warning", "critical"]):
                return
        padding = self._theme.padding(widget)
        prefix = self._theme.prefix(widget, padding)
        suffix = self._theme.suffix(widget, padding)

        if prefix:
            full_text = u"{}{}".format(prefix, full_text)
        if suffix:
            full_text = u"{}{}".format(full_text, suffix)

        separator = self._theme.separator(widget)
        if separator:
            self._widgets.append({
                u"full_text": separator,
                "separator": False,
                "color": self._theme.separator_fg(widget),
                "background": self._theme.separator_bg(widget),
                "separator_block_width": self._theme.separator_block_width(widget),
            })
        width = self._theme.minwidth(widget)

        if width:
            full_text = full_text.ljust(len(width) + len(prefix) + len(suffix))

        markup = "none" if not self._config else self._config.markup()

        if markup == "pango":
            full_text = full_text.replace("&", "&amp;")

        self._widgets.append({
            u"full_text": full_text,
            "color": self._theme.fg(widget),
            "background": self._theme.bg(widget),
            "separator_block_width": self._theme.separator_block_width(widget),
            "separator": True if separator is None else False,
            "min_width": None,
#            "min_width": width + "A"*(len(prefix) + len(suffix)) if width else None,
            "align": self._theme.align(widget),
            "instance": widget.id,
            "name": module.id,
            "markup": markup,
        })

    def begin(self):
        """Start one output iteration"""
        self._widgets = []
        self._theme.reset()

    def flush(self):
        """Flushes output"""
        widgets = self._widgets
        if self._config and self._config.reverse():
            widgets = list(reversed(widgets))
        sys.stdout.write(json.dumps(widgets))
        if len(self._config.unused_keys()) > 0:
            for key in self._config.unused_keys():
                log.warning("unused parameter {} - please check the documentation of the affected module to ensure the parameter exists".format(key))

    def end(self):
        """Finalizes output"""
        sys.stdout.write(",\n")
        sys.stdout.flush()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
