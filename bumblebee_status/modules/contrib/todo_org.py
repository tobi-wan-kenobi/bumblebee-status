# pylint: disable=C0111,R0903
"""Displays the number of todo items from an org-mode file
Parameters:
    * todo_org.file:      File to read TODOs from (defaults to ~/org/todo.org)
    * todo_org.remaining: False by default. When true, will output the number of remaining todos instead of the number completed (i.e. 1/4 means 1 of 4 todos remaining, rather than 1 of 4 todos completed)
Based on the todo module by `codingo <https://github.com/codingo>`
"""

import re
import os.path

import core.module
import core.widget
import core.input
from util.format import asbool

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__todo_regex = re.compile("^\\s*\\*+\\s*TODO")
        self.__done_regex = re.compile("^\\s*\\*+\\s*DONE")

        self.__doc = os.path.expanduser(
            self.parameter("file", "~/org/todo.org")
        )
        self.__remaining = asbool(self.parameter("remaining", "False"))
        self.__todo, self.__total = self.count_items()
        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd="emacs {}".format(self.__doc)
        )

    def output(self, widget):
        if self.__remaining:
            return "TODO: {}/{}".format(self.__todo, self.__total)
        return "TODO: {}/{}".format(self.__total-self.__todo, self.__total)

    def update(self):
        self.__todo, self.__total = self.count_items()

    def count_items(self):
        todo, total = 0, 0
        try:
            with open(self.__doc, "r") as f:
                for line in f:
                    if self.__todo_regex.match(line.upper()) is not None:
                        todo += 1
                        total += 1
                    elif self.__done_regex.match(line.upper()) is not None:
                        total += 1
            return todo, total
        except OSError:
            return -1, -1

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
