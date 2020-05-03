# pylint: disable=C0111,R0903

"""Shows that debug is enabled"""

import platform

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))

    def full_text(self, widgets):
        return "debug"

    def state(self, widget):
        return "warning"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
