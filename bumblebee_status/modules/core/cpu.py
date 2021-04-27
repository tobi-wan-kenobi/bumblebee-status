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
        super().__init__(config, theme, [])
        self._percpu = util.format.asbool(self.parameter("percpu", False))

        for idx, cpu_perc in enumerate(self.cpu_utilization()):
            widget = self.add_widget(name="cpu#{}".format(idx), full_text=self.utilization)
            widget.set("utilization", cpu_perc)
            widget.set("theme.minwidth", self._format.format(100.0 - 10e-20))

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="gnome-system-monitor"
        )

    @property
    def _format(self):
        return self.parameter("format", "{:.01f}%")

    def utilization(self, widget):
        return self._format.format(widget.get("utilization", 0.0))

    def cpu_utilization(self):
        tmp = psutil.cpu_percent(percpu=self._percpu)
        return tmp if self._percpu else [tmp]

    def update(self):
        for idx, cpu_perc in enumerate(self.cpu_utilization()):
            self.widgets()[idx].set("utilization", cpu_perc)

    def state(self, widget):
        return self.threshold_state(widget.get("utilization", 0.0), 70, 80)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
