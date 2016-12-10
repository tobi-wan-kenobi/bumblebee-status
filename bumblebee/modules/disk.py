# pylint: disable=C0111,R0903

"""Shows free diskspace, total diskspace and the percentage of free disk space.

Parameters:
    * disk.warning: Warning threshold in % of disk space (defaults to 80%)
    * disk.critical: Critical threshold in % of disk space (defaults ot 90%)
    * disk.path: Path to calculate disk usage from (defaults to /)
"""

import os

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.diskspace)
        )
        self._path = self.parameter("path", "/")
        self._perc = 0

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="nautilus {}".format(self._path))

    def diskspace(self):
        st = os.statvfs(self._path)
        size = st.f_frsize*st.f_blocks
        used = size - st.f_frsize*st.f_bavail
        self._perc = 100.0*used/size

        return "{} {}/{} ({:05.02f}%)".format(self._path,
            bumblebee.util.bytefmt(used),
            bumblebee.util.bytefmt(size), self._perc
        )

    def update(self, widgets):
        pass

    def state(self, widget):
        pass
    def warning(self, widget):
        return self._perc > self._config.parameter("warning", 80)

    def critical(self, widget):
        return self._perc > self._config.parameter("critical", 90)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
