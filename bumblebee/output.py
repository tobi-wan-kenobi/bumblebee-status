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
BRAILLE = {
    (0, 0): u" ",
    (1, 0): u"\u2840",
    (2, 0): u"\u2844",
    (3, 0): u"\u2846",
    (4, 0): u"\u2847",
    (0, 1): u"\u2880",
    (0, 2): u"\u28a0",
    (0, 3): u"\u28b0",
    (0, 4): u"\u28b8",
    (1, 1): u"\u28c0",
    (2, 1): u"\u28c4",
    (3, 1): u"\u28c6",
    (4, 1): u"\u28c7",
    (1, 2): u"\u28e0",
    (2, 2): u"\u28e4",
    (3, 2): u"\u28e6",
    (4, 2): u"\u28e7",
    (1, 3): u"\u28f0",
    (2, 3): u"\u28f4",
    (3, 3): u"\u28f6",
    (4, 3): u"\u28f7",
    (1, 4): u"\u28f8",
    (2, 4): u"\u28fc",
    (3, 4): u"\u28fe",
    (4, 4): u"\u28ff"
}

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


class BrailleGraph(object):
    """
        graph using Braille chars
        scaled to passed values
    """
    def __init__(self, values):
        """
            Args:

                values (list): list of values
        """
        self.values = values
        # length of values list must be even
        # because one Braille char displays two values
        if len(self.values) % 2 == 1:
            self.values.append(0)
        self.steps = self.get_steps()
        self.parts = [tuple(self.steps[i:i+2])
                      for i in range(len(self.steps))[::2]]

    @staticmethod
    def get_height(value, unit):
        """
            Compute height of a value relative to unit

            Args:

                value (number): value

                unit (number): unit
        """
        if value < unit / 10.:
            return 0
        elif value <= unit:
            return 1
        elif value <= unit * 2:
            return 2
        elif value <= unit * 3:
            return 3
        else:
            return 4

    def get_steps(self):
        """
            Convert the list of values to a list of steps

            Return: list
        """
        maxval = max(self.values)
        unit = maxval / 4.
        if unit == 0:
            return [0] * len(self.values)
        stepslist = []
        for value in self.values:
            stepslist.append(self.get_height(value, unit))
        return stepslist

    def get_chars(self):
        """
            Decide which chars to draw

            Return: str
        """
        chars = []
        for part in self.parts:
            chars.append(BRAILLE[part])
        return "".join(chars)


def bgraph(values):
    """wrapper function"""
    return BrailleGraph(values).get_chars()


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

        if self._config.markup() == "pango":
            # add prefix/suffix colors
            fg = self._theme.prefix_fg(widget)
            bg = self._theme.prefix_bg(widget)
            prefix = "<span {} {}>{}</span>".format(
                "foreground='{}'".format(fg) if fg else "",
                "background='{}'".format(bg) if bg else "",
                prefix
            )

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
