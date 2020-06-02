# pylint: disable=C0111,R0903

"""Displays the status of watson (time-tracking tool)

Requires the following executable:
    * watson

contributed by `bendardenne <https://github.com/bendardenne>`_ - many thanks!
"""

import logging
import re
import functools

import core.module
import core.widget
import core.input
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))

        self.__tracking = False
        self.__project = ""
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle)

    def toggle(self, widget):
        self.__project = "hit"
        if self.__tracking:
            util.cli.execute("watson stop")
        else:
            util.cli.execute("watson restart")
        self.__tracking = not self.__tracking

    def text(self, widget):
        if self.__tracking:
            return self.__project
        else:
            return "Paused"

    def update(self):
        output = util.cli.execute("watson status")
        if re.match(r"No project started", output):
            self.__tracking = False
            return

        self.__tracking = True
        m = re.search(r"Project (.+) started", output)
        self.__project = m.group(1)

    def state(self, widget):
        return "on" if self.__tracking else "off"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
