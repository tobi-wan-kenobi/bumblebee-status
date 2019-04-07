# pylint: disable=C0111,R0903

"""Displays the system hostname."""

import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._hname = ""

    def output(self, _):
        return self._hname+" "+u"\uf233"

    def update(self, widgets):
        with open('/proc/sys/kernel/hostname', 'r') as f:
            self._hname = f.readline().split()[0]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
