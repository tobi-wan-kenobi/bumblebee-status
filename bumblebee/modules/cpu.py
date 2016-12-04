# pylint: disable=C0111,R0903

"""Displays CPU utilization across all CPUs."""

import psutil
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine):
        super(Module, self).__init__(engine)
        self._utilization = psutil.cpu_percent(percpu=False)

    def widgets(self):
        self._utilization = psutil.cpu_percent(percpu=False)

        return bumblebee.output.Widget(full_text="{:05.02f}%".format(self._utilization))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
