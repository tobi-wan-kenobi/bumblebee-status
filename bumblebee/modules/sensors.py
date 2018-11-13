# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays sensor temperature

Parameters:
    * sensors.path: path to temperature file (default /sys/class/thermal/thermal_zone0/temp).
    * sensors.json: if set to "true", interpret sensors.path as JSON "path" in the output
                    of "sensors -j" (i.e. <key1>/<key2>/.../<value>), for example, path could
                    be: "coretemp-isa-00000/Core 0/temp1_input" (defaults to "false")
    * sensors.match: (fallback) Line to match against output of 'sensors -u' (default: temp1_input)
    * sensors.match_pattern: (fallback) Line to match against before temperature is read (no default)
    * sensors.match_number: (fallback) which of the matches you want (default -1: last match).
￼
"""

import re
import json
import logging

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

log = logging.getLogger(__name__)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.temperature))
        self._temperature = "unknown"
        self._mhz = "n/a"
        self._match_number = int(self.parameter("match_number", "-1"))
        self._match_pattern = self.parameter("match_pattern", None)
        self._pattern = re.compile(r"^\s*{}:\s*([\d.]+)$".format(self.parameter("match", "temp1_input")), re.MULTILINE)
        self._json = bumblebee.util.asbool(self.parameter("json", "false"))
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd="xsensors")
        self.determine_method()

    def determine_method(self):
        if self.parameter("path") != None and self._json == False:
            self.use_sensors = False # use thermal zone
        else:
            # try to use output of sensors -u
            try:
                output = bumblebee.util.execute("sensors -u")
                self.use_sensors = True
                log.debug("Sensors command available")
            except FileNotFoundError as e:
                log.info("Sensors command not available, using /sys/class/thermal/thermal_zone*/")
                self.use_sensors = False

    def _get_temp_from_sensors(self):
        if self._json == True:
            try:
                output = json.loads(bumblebee.util.execute("sensors -j"))
                for key in self.parameter("path").split("/"):
                    output = output[key]
                return int(float(output))
            except Exception as e:
                logging.error("unable to read sensors: {}".format(str(e)))
                return "unknown"
        else:
            output = bumblebee.util.execute("sensors -u")
            if self._match_pattern:
                temp_pattern = self.parameter("match", "temp1_input")
                match = re.search(r"{}.+{}:\s*([\d.]+)$".format(self._match_pattern, temp_pattern), output.replace("\n", ""))
                if match:
                    return int(float(match.group(1)))
                else:
                    return "unknown"
            match = self._pattern.findall(output)
            if match:
                return int(float(match[self._match_number]))
        return "unknown"

    def get_temp(self):
        if self.use_sensors:
            temperature = self._get_temp_from_sensors()
            log.debug("Retrieve temperature from sensors -u")
        else:
            try:
                temperature = open(self.parameter("path", "/sys/class/thermal/thermal_zone0/temp")).read()[:2]
                log.debug("retrieved temperature from /sys/class/")
                # TODO: Iterate through all thermal zones to determine the correct one and use its value
                # https://unix.stackexchange.com/questions/304845/discrepancy-between-number-of-cores-and-thermal-zones-in-sys-class-thermal

            except IOError:
                temperature = "unknown"
                log.info("Can not determine temperature, please install lm-sensors")

        return temperature

    def get_mhz(self):
        try:
            output = open("/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq").read()
            mhz = int(float(output)/1000.0)
        except:
            output = open("/proc/cpuinfo").read()
            m = re.search(r"cpu MHz\s+:\s+(\d+)", output)
            mhz = int(m.group(1))

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
