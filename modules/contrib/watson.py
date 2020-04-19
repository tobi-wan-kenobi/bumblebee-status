# pylint: disable=C0111,R0903

"""Displays the status of watson (time-tracking tool)

Requires the following executable:
    * watson
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util
import bumblebee.popup_v2

import logging
import re
import functools

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.text))
        self._tracking = False
        self._project = ""
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                        cmd=self.toggle)

    def toggle(self, widget):
        self._project = "hit"
        if self._tracking:
            bumblebee.util.execute("watson stop")
        else:
            bumblebee.util.execute("watson restart")
        self._tracking = not self._tracking

    def text(self, widget):
        if self._tracking:
            return self._project
        else:
            return "Paused"

    def update(self, widgets):
        output = bumblebee.util.execute("watson status")
        if re.match('No project started', output):
            self._tracking = False
            return

        self._tracking = True
        m = re.search(r'Project (.+) started', output)
        self._project = m.group(1)

    #
    def state(self, widget):
        return "on" if self._tracking else "off"
    #     return [widget.get("status", None), widget.get("period", None)]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
