# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays sensor temperature

Parameters:
    * sensors.path: path to temperature file (default /sys/class/thermal/thermal_zone0/temp).
"""

import re

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.temperature))
        self._temperature = "unknown"
        self._mhz = "n/a"
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd="xsensors")

    def get_temp(self):
        try:
            temperature = open(self.parameter("path", "/sys/class/thermal/thermal_zone0/temp")).read()[:2]
        except IOError:
            temperature = "unknown"
        return temperature

    def get_mhz( self ):
        output = open("/proc/cpuinfo").read()
        m      = re.search(r"cpu MHz\s+:\s+(\d+)", output)
        mhz    = int(m.group(1))

        if mhz < 1000:
            return "{} MHz".format(mhz)
        else:
            return "{:0.01f} GHz".format(float(mhz)/1000.0)

    def temperature(self, _):
        return u"{}°c @ {}".format(self._temperature, self._mhz)

    def update(self, widgets):
        self._temperature = self.get_temp()
        self._mhz = self.get_mhz()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
