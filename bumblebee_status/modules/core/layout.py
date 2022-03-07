# pylint: disable=C0111,R0903

"""Displays the current keyboard layout

Parameters:
    * layout.device: The device ID of the keyboard (as reported by `xinput -list`), defaults to the core device
"""

import re

import core.widget
import core.module

import util.cli

from bumblebee_status.discover import utility

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config=config, theme=theme, widgets=core.widget.Widget(self.get_layout))

        self._cmd = utility("get-kbd-layout")
        keyboard = self.parameter("device", None)
        if keyboard:
            self._cmd += " {}".format(keyboard)

    def get_layout(self, widget):
        result = util.cli.execute(self._cmd, ignore_errors=True)

        m = re.search("([a-zA-Z]+_)?([a-zA-Z]+)(\(([\w-]+)\))?", result)

        if m:
            layout = m.group(2)
            variant = m.group(3)
            return layout if not variant else "{} {}".format(layout, variant)

        return "n/a"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
