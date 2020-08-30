# pylint: disable=C0111,R0903

"""Displays available RAM, total amount of RAM and percentage available.

By default, opens `gnome-system-monitor` on left mouse click.

Requirements:
    * gnome-system-monitor for default mouse click action

Parameters:
    * memory.warning : Warning threshold in % of memory used (defaults to 80%)
    * memory.critical: Critical threshold in % of memory used (defaults to 90%)
    * memory.format: Format string (defaults to '{used}/{total} ({percent:05.02f}%)')
    * memory.usedonly: Only show the amount of RAM in use (defaults to False). Same as memory.format='{used}'
"""

import re

import core.module
import core.widget
import core.input

import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.memory_usage))
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="gnome-system-monitor"
        )

    @property
    def _format(self):
        if util.format.asbool(self.parameter("usedonly", False)):
            return "{used}"
        else:
            return self.parameter("format", "{used}/{total} ({percent:05.02f}%)")

    def memory_usage(self, widget):
        return self._format.format(**self._mem)

    def update(self):
        data = self.__parse_meminfo()

        if "MemAvailable" in data:
            used = data["MemTotal"] - data["MemAvailable"]
        else:
            used = (
                data["MemTotal"]
                - data["MemFree"]
                - data["Buffers"]
                - data["Cached"]
                - data["Slab"]
            )
        self._mem = {
            "total": util.format.byte(data["MemTotal"]),
            "available": util.format.byte(data["MemAvailable"]),
            "free": util.format.byte(data["MemFree"]),
            "used": util.format.byte(used),
            "percent": float(used) / float(data["MemTotal"]) * 100.0,
        }

    def state(self, widget):
        if self._mem["percent"] > float(self.parameter("critical", 90)):
            return "critical"
        if self._mem["percent"] > float(self.parameter("warning", 80)):
            return "warning"
        return None

    def __parse_meminfo(self):
        data = {}
        with open("/proc/meminfo", "r") as f:
            # https://bugs.python.org/issue32933
            for line in f.readlines():
                tmp = re.split(r"[:\s]+", line)
                value = self.__parse_value(tmp)

                data[tmp[0]] = value

        return data

    def __parse_value(self, data):
        value = int(data[1])

        if data[2] == "kB":
            value = value * 1024
        if data[2] == "mB":
            value = value * 1024 * 1024
        if data[2] == "gB":
            value = value * 1024 * 1024 * 1024

        return value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
