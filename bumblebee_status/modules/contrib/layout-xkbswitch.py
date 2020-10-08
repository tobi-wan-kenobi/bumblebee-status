"""Displays and changes the current keyboard layout

Requires the following executable:
    * xkb-switch

contributed by `somospocos <https://github.com/somospocos>`_ - many thanks!
"""

import core.module
import core.widget
import core.decorators
import core.input

import util.cli


class Module(core.module.Module):
    @core.decorators.every(seconds=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.current_layout))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.next_keymap)
        self.__current_layout = self.__get_current_layout()

    def current_layout(self, _):
        return self.__current_layout

    def next_keymap(self, event):
        util.cli.execute("xkb-switch -n", ignore_errors=True)

    def __get_current_layout(self):
        try:
            res = util.cli.execute("xkb-switch")
            return res.split("\n")[0]
        except RuntimeError:
            return ["n/a"]

    def update(self):
        self.__current_layout = self.__get_current_layout()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
