# pylint: disable=C0111,R0903

"""Displays system load.

By default, opens `gnome-system-monitor` on left mouse click.

Requirements:
    * gnome-system-monitor for default mouse click action

Parameters:
    * load.warning : Warning threshold for the one-minute load average (defaults to 70% of the number of CPUs)
    * load.critical: Critical threshold for the one-minute load average (defaults to 80% of the number of CPUs)
"""

import os
import multiprocessing

import core.module
import core.input


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.load))
        self._load = [0, 0, 0]
        try:
            self._cpus = multiprocessing.cpu_count()
        except NotImplementedError as e:
            self._cpus = 1

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="gnome-system-monitor"
        )

    def load(self, widget):
        return "{:.02f}/{:.02f}/{:.02f}".format(
            self._load[0], self._load[1], self._load[2]
        )

    def update(self):
        self._load = os.getloadavg()

    def state(self, widget):
        return self.threshold_state(self._load[0], self._cpus * 0.7, self._cpus * 0.8)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
