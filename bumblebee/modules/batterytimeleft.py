"""Displays how much battery time is left.

Requires the following library:
    * power
"""

import os
import glob
import functools

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

try:
    import power
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.estimate)
                                     )
        self._estimate = "n/a"
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-power-statistics")
        immediate_update = functools.partial(self.update)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
                                       cmd=immediate_update)

    def estimate(self, _):
        return str(self._estimate)

    def state(self, widget):
        if self._estimate == "Unlimited":
            return "unlimited"
        return "estimate"

    def update(self, _):
        try:
            type = power.PowerManagement().get_providing_power_source_type()
            estimate = power.PowerManagement().get_time_remaining_estimate()

            if type == power.POWER_TYPE_AC and estimate == -2.0:
                self._estimate = "Unlimited"
            elif estimate == -1.0:
                self._estimate = "Unknown"
            else:
                self._estimate = str(round(estimate / 60, 1)) + ' h'

        except Exception as e:
            print (e)
            self._estimate = "n/a"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
