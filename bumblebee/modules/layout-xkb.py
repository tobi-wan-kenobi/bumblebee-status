# pylint: disable=C0111,R0903

import bumblebee.input
import bumblebee.output
import bumblebee.engine

from thirdparty.xkbgroup import *

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
        pass

    def current_layout(self, widget):
        xkb = XKeyboard()
        log.debug("group num: {}".format(xkb.group_num))
        return "{} ({})".format(xkb.group_symbol, xkb.group_variant) if xkb.group_variant else xkb.group_symbol

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
