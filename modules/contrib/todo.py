# pylint: disable=C0111,R0903

"""Displays the number of todo items from a text file

Parameters:
    * todo.file: File to read TODOs from (defaults to ~/Documents/todo.txt)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import os.path


class Module(bumblebee.engine.Module):


    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._doc = os.path.expanduser(self.parameter("file", "~/Documents/todo.txt"))
        self._todos = self.count_items()


    def output(self, widget):
       self._todos = self.count_items()
       return str(self._todos)


    def state(self, widgets):
        if self._todos == 0:
            return "empty"
        return "items"


    def count_items(self):
        try:
            i = -1
            with open(self._doc) as f:
                for i, l in enumerate(f):
                    pass
            return i+1
        except Exception:
            return 0
