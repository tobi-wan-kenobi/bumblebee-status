# pylint: disable=C0111,R0903

"""Displays available RAM, total amount of RAM and percentage available.

Parameters:
    * memory.warning : Warning threshold in % of memory used (defaults to 80%)
    * memory.critical: Critical threshold in % of memory used (defaults to 90%)
    * memory.format: Format string (defaults to "{used}/{total} ({percent:05.02f}%)")
    * memory.usedonly: Only show the amount of RAM in use (defaults to False). Same as memory.format="{used}"
"""

import re

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Container(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.memory_usage)
        )
        self.update(None)

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-system-monitor")

    @property
    def _format(self):
        if bumblebee.util.asbool(self.parameter("usedonly", False)):
            return "{used}"
        else:
            return self.parameter("format", "{used}/{total} ({percent:05.02f}%)")

    def memory_usage(self, widget):
        return self._format.format(**self._mem)

    def update(self, widgets):
        data = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                tmp = re.split(r"[:\s]+", line)
                value = int(tmp[1])
                if tmp[2] == "kB": value = value*1024
                if tmp[2] == "mB": value = value*1024*1024
                if tmp[2] == "gB": value = value*1024*1024*1024
                data[tmp[0]] = value
        if "MemAvailable" in data:
            used = data["MemTotal"] - data["MemAvailable"]
        else:
            used = data["MemTotal"] - data["MemFree"] - data["Buffers"] - data["Cached"] - data["Slab"]
        self._mem = {
            "total": bumblebee.util.bytefmt(data["MemTotal"]),
            "available": bumblebee.util.bytefmt(data["MemAvailable"]),
            "free": bumblebee.util.bytefmt(data["MemFree"]),
            "used": bumblebee.util.bytefmt(used),
            "percent": float(used)/float(data["MemTotal"])*100.0
        }

    def state(self, widget):
        if self._mem["percent"] > float(self.parameter("critical", 90)):
            return "critical"
        if self._mem["percent"] > float(self.parameter("warning", 80)):
            return "warning"
        return None

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
