# pylint: disable=C0111,R0903

"""Displays the status of watson (time-tracking tool)

Requires the following executable:
    * watson

Parameters:
    * watson.format: Output format, defaults to "{project} [{tags}]"
      Supported fields are: {project}, {tags}, {relative_start}, {absolute_start}

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
        self.__info = {}
        self.__format = self.parameter("format", "{project} [{tags}]")
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle)

    def toggle(self, widget):
        if self.__tracking:
            util.cli.execute("watson stop")
        else:
            util.cli.execute("watson restart")
        self.__tracking = not self.__tracking

    def text(self, widget):
        if self.__tracking:
            return self.__format.format(**self.__info)
        else:
            return "Paused"

    def update(self):
        output = util.cli.execute("watson status")

        m = re.search(r"Project ([^\[\]]+)(?: \[(.+)\])? started (.+) \((.+)\)", output)

        if m:
            self.__tracking = True
            self.__info = {
                "project": m.group(1),
                "tags": m.group(2) or "",
                "relative_start": m.group(3),
                "absolute_start": m.group(4),
            }
        else:
            self.__tracking = False
            return

    def state(self, widget):
        return "on" if self.__tracking else "off"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
