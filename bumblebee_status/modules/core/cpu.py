# pylint: disable=C0111,R0903

"""Displays CPU utilization across all CPUs.

Requirements:
    * the psutil Python module for the first three items from the list above

Parameters:
    * cpu.warning : Warning threshold in % of CPU usage (defaults to 70%)
    * cpu.critical: Critical threshold in % of CPU usage (defaults to 80%)
    * cpu.format  : Format string (defaults to '{:.01f}%')
"""

import psutil

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.utilization))
        self.widget().set("theme.minwidth", self._format.format(100.0 - 10e-20))
        self._utilization = psutil.cpu_percent(percpu=False)
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="gnome-system-monitor"
        )

    @property
    def _format(self):
        return self.parameter("format", "{:.01f}%")

    def utilization(self, _):
        return self._format.format(self._utilization)

    def update(self):
        self._utilization = psutil.cpu_percent(percpu=False)

    def state(self, _):
        return self.threshold_state(self._utilization, 70, 80)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
