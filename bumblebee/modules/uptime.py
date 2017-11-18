# pylint: disable=C0111,R0903

"""Displays the system uptime."""

# Use absolute_import because there's already a datatime module
# in the same directory
from __future__ import absolute_import

import bumblebee.input
import bumblebee.output
import bumblebee.engine

from datetime import timedelta

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._uptime = ""

    def output(self, _):
        return "{}".format(self._uptime)

    def update(self, widgets):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = int(float(f.readline().split()[0]))
            self._uptime = timedelta(seconds = uptime_seconds)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
