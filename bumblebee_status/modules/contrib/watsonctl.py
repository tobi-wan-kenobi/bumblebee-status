# pylint: disable=C0111,R0903

"""Displays the status of watson (time-tracking tool)
Requires the following executable:
    * watson
origional module contributed by `bendardenne <https://github.com/bendardenne>`_ - many thanks!
extended by `dale-muccignat <https://github.com/dale-muccignat>`_
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
    # @core.decorators.every(minutes=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))

        self.__tracking = False
        self.__status = ""
        self.__project = "Select Project"

        self.__project_key = {}
        self.__project_list = []
        self.get_list()

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle)
        core.input.register(self, button=core.input.WHEEL_UP, cmd=self.change_project)
        core.input.register(self, button=core.input.WHEEL_DOWN, cmd=self.change_project)

    def get_list(self):
        # updates the list of current projects and creats a key dictionary
        self.__project_list = util.cli.execute("watson projects").split()
        for n in range(len(self.__project_list)):
            self.__project_key[self.__project_list[n]] = n

    def toggle(self, widget):
        # on click, starts the timer if the project is slected
        if self.__project != "Select Project":
            if self.__tracking:
                util.cli.execute("watson stop")
                self.__status = "Paused"
            else:
                util.cli.execute("watson start " + self.__project)
                self.__status = "Play"
            self.__tracking = not self.__tracking

    def change_project(self, event):
        # on scroll, cycles the currently selected project
        if self.__tracking:
            return
        if self.__project == "Select Project":
            self.__project = self.__project_list[0]
        else:
            n = self.__project_key[self.__project]
            if n < len(self.__project_list) - 1:
                self.__project = self.__project_list[n + 1]
            else:
                self.__project = self.__project_list[0]

    def text(self, widget):
        if self.__tracking:
            return self.__project + ": " + self.__status
        else:
            return self.__project + ": " + self.__status

    def update(self):
        output = util.cli.execute("watson status")
        if re.match(r"No project started", output):
            self.__tracking = False
            self.__status = "Paused"
            return

        self.__tracking = True
        m = re.search(r"Project (.+) started", output)
        self.__project = m.group(1)
        self.__status = "Play"
        self.get_list()

    def state(self, widget):
        return "on" if self.__tracking else "off"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
