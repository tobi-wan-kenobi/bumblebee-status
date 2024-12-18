# pylint: disable=C0111,R0903

"""Displays the current keyboard layout using libX11

Requires the following library:
    * libX11.so.6
and python module:
    * xkbgroup

Parameters:
    * layout.showname: Boolean that indicate whether the full name should be displayed. Defaults to false (only the symbol will be displayed)
    * layout.show_variant: Boolean that indecates whether the variant name should be displayed. Defaults to true.
    * layout.highlight_if_not: String that indicates the highlight_if_not layout. Widget goes into "warning" state if not on the highlight_if_not layout. If not set, the widget never indicates a "warning"
"""

from xkbgroup import *

import logging

log = logging.getLogger(__name__)

import core.module
import core.widget
import core.input

import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.current_layout))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__next_keymap)
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.__prev_keymap)
        self.__show_variant = util.format.asbool(self.parameter("show_variant", True))
        self.__highlight_if_not = self.parameter("highlight_if_not", None)

        self.__value = "n/a"

    def __next_keymap(self, event):
        self.__set_keymap(1)

    def __prev_keymap(self, event):
        self.__set_keymap(-1)

    def __set_keymap(self, rotation):
        xkb = XKeyboard()
        if xkb.groups_count < 2:
            return  # nothing to do
        layouts = xkb.groups_symbols
        idx = layouts.index(xkb.group_symbol)
        xkb.group_symbol = str(layouts[(idx + rotation) % len(layouts)])

    def current_layout(self, widget):
        try:
            xkb = XKeyboard()
            log.debug("group num: {}".format(xkb.group_num))
            name = (
                xkb.group_name
                if util.format.asbool(self.parameter("showname", False))
                else xkb.group_symbol
            )
            if self.__show_variant:
                self.__value = (
                    "{} ({})".format(name, xkb.group_variant)
                    if xkb.group_variant
                    else name
                )
            self.__value = name
        except Exception as e:
            print("got exception: {}".format(e))
            self.__value = "n/a"
        return self.__value

    def state(self, widget):
        if self.__highlight_if_not == None:
            return []
        if self.__highlight_if_not != self.__value:
            print("warning")
            return ["warning"]
        return []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
