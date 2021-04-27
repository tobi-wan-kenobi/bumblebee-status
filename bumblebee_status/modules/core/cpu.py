# pylint: disable=C0111,R0903

"""Displays CPU utilization across all CPUs.

By default, opens `gnome-system-monitor` on left mouse click.

Requirements:
    * the psutil Python module for the first three items from the list above
    * gnome-system-monitor for default mouse click action

Parameters:
    * cpu.warning : Warning threshold in % of CPU usage (defaults to 70%)
    * cpu.critical: Critical threshold in % of CPU usage (defaults to 80%)
    * cpu.format  : Format string (defaults to '{:.01f}%')
    * cpu.percpu  : If set to true, show each individual cpu (defaults to false)
"""

import psutil

import core.module
import core.widget
import core.input

import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.utilization))
        self._percpu = util.format.asbool(self.parameter("percpu", False))
        self.update()
        self.widget().set("theme.minwidth", self._format.format(*[100.0 - 10e-20]*len(self._utilization)))
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="gnome-system-monitor"
        )

    @property
    def _format(self):
        fmt = self.parameter("format", "{:.01f}%")
        if self._percpu:
            fmt = [fmt]*len(self._utilization)
            fmt = " ".join(fmt)
        return fmt

    def utilization(self, _):
        return self._format.format(*self._utilization)

    def update(self):
        self._utilization = psutil.cpu_percent(percpu=self._percpu)
        if not self._percpu:
            self._utilization = [self._utilization]

    def state(self, _):
        return self.threshold_state(sum(self._utilization)/len(self._utilization), 70, 80)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
