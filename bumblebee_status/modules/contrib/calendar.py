"""Displays date, opens a gnome-calendar on click

Parameters:
    * calendar.format: strftime()-compatible formatting string
    * calendar.locale: locale to use rather than the system default
"""

import core.decorators
from ..core.datetime import Module

import core.input


class Module(Module):
    @core.decorators.every(hours=1)
    def __init__(self, config, theme):
        super().__init__(config, theme)
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd="gnome-calendar")

    def default_format(self):
        return "%x"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
