# pylint: disable=C0111,R0903

"""Displays available RAM, total amount of RAM and percentage available.

Parameters:
    * memory.warning : Warning threshold in % of memory used (defaults to 80%)
    * memory.critical: Critical threshold in % of memory used (defaults to 90%)
    * memory.format: Format string (defaults to "{used}/{total} ({percent:05.02f}%)")
    * memory.usedonly: Only show the amount of RAM in use (defaults to False). Same as memory.format="{used}"
"""

try:
    import psutil
except ImportError:
    pass

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.memory_usage)
        )
        self._mem = psutil.virtual_memory()
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-system-monitor")

    @property
    def _format(self):
        if bumblebee.util.asbool(self.parameter("usedonly", False)):
            return "{used}"
        else:
            return self.parameter("format", "{used}/{total} ({percent:05.02f}%)")

    def memory_usage(self, widget):
        used = bumblebee.util.bytefmt(self._mem.total - self._mem.available)
        total = bumblebee.util.bytefmt(self._mem.total)

        return self._format.format(used=used, total=total, percent=self._mem.percent)

    def update(self, widgets):
        self._mem = psutil.virtual_memory()

    def state(self, widget):
        if self._mem.percent > float(self.parameter("critical", 90)):
            return "critical"
        if self._mem.percent > float(self.parameter("warning", 80)):
            return "warning"
        return None

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
