# pylint: disable=C0111,R0903

"""Displays the system hostname.

contributed by `varkokonyi <https://github.com/varkokonyi>`_ - many thanks!
"""

import platform

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))
        self.__hname = ""

    def output(self, _):
        return self.__hname + " " + "\uf233"

    def update(self):
        self.__hname = platform.node()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
