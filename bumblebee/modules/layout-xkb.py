# pylint: disable=C0111,R0903

"""Displays the current keyboard layout using libX11

Requires the following library:
    * libX11.so.6
and python module:
    * xkbgroup

Parameters:
    * layout-xkb.showname: Boolean that indicate whether the full name should be displayed. Defaults to false (only the symbol will be displayed)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

has_xkb = True
try:
    from xkbgroup import *
except ImportError:
    has_xkb = False

import logging
log = logging.getLogger(__name__)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.current_layout)
        )
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._next_keymap)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd=self._prev_keymap)

    def _next_keymap(self, event):
        self._set_keymap(1)

    def _prev_keymap(self, event):
        self._set_keymap(-1)

    def _set_keymap(self, rotation):
        if not has_xkb: return

        xkb = XKeyboard()
        if xkb.groups_count < 2: return # nothing to doA
        layouts = xkb.groups_symbols
        idx = layouts.index(xkb.group_symbol)
        xkb.group_symbol = str(layouts[(idx + rotation) % len(layouts)])

    def current_layout(self, widget):
        try:
            xkb = XKeyboard()
            log.debug("group num: {}".format(xkb.group_num))
            name = xkb.group_name if bumblebee.util.asbool(self.parameter("showname")) else xkb.group_symbol
            return "{} ({})".format(name, xkb.group_variant) if xkb.group_variant else name
        except Exception:
            return "n/a"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
