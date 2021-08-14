# pylint: disable=C0111,R0903

"""Displays the number of todo items from a text file

Parameters:
    * todo.file: File to read TODOs from (defaults to ~/Documents/todo.txt)


contributed by `codingo <https://github.com/codingo>`_ - many thanks!
"""

import os.path

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__doc = os.path.expanduser(self.parameter("file", "~/Documents/todo.txt"))
        self.__editor = self.parameter("editor", "xdg-open")
        self.__todos = self.count_items()
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="{} {}".format(self.__editor, self.__doc)
        )

    def output(self, widget):
        return str(self.__todos)

    def update(self):
        self.__todos = self.count_items()

    def state(self, widgets):
        if self.__todos == 0:
            return "empty"
        return "items"

    def count_items(self):
        try:
            i = 0
            with open(self.__doc) as f:
                for l in f.readlines():
                    if l.strip() != '':
                        i += 1
            return i
        except Exception:
            return 0


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
