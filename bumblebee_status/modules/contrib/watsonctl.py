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

from easygui import *


class Module(core.module.Module):
    # @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))

        self.__tracking = False
        self.__status = ""
        self.__project = "Select Project"

        self.__project_key = {}
        self.__project_list = []

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle)
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.new_project)
        core.input.register(self, button=core.input.WHEEL_UP, cmd=self.change_project_up)
        core.input.register(self, button=core.input.WHEEL_DOWN, cmd=self.change_project_down)

    def new_project(self, widget):
        # on right-click, open dialog to enter the name of a new project
        # TODO: enable entering a new tag in a second dialog box
        if self.__tracking:
            return
        text = "Enter the name of a new project to start"
        title = "Watson"
        output = enterbox(text,title,self.__project)
        if output:
            self.__project = output
            util.cli.execute("watson start " + self.__project)

    def toggle(self, widget):
        # on click, starts the timer if the project is slected
        if self.__project != "Select Project":
            if self.__tracking:
                util.cli.execute("watson stop")
                self.__status = "Paused"
            else:
                util.cli.execute("watson start " + self.__project)
                self.__status = "Tracking"
            self.__tracking = not self.__tracking
            self.update()

    def change_project_up(self, event):
        # on scroll up, cycles the currently selected project up
        if self.__tracking:
            return
        if self.__project == "Select Project":
            return
        n = self.__project_key[self.__project]
        if n < len(self.__project_list) - 1:
            self.__project = self.__project_list[n + 1]
        else:
            self.__project = self.__project_list[0]
        self.update()

    def change_project_down(self, event):
        # on scroll down, cycles the currently selected project down
        if self.__tracking:
            return
        if self.__project == "Select Project":
            return
        n = self.__project_key[self.__project]
        if n > 0:
            self.__project = self.__project_list[n - 1]
        else:
            self.__project = self.__project_list[-1]
        self.update()

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
        else:
            self.__tracking = True
            m = re.search(r"Project (.+) started", output)
            self.__project = m.group(1)
            self.__status = "Tracking"

        # updates the list of current projects and creats a key dictionary
        self.__project_list = util.cli.execute("watson projects").split()
        for n in range(len(self.__project_list)):
            if n == 0 and self.__project == "Select Project":
                self.__project = self.__project_list[n]
            self.__project_key[self.__project_list[n]] = n

    def state(self, widget):
        return "on" if self.__tracking else "off"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
