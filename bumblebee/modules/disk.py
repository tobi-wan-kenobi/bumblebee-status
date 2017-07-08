# pylint: disable=C0111,R0903

"""Shows free diskspace, total diskspace and the percentage of free disk space.

Parameters:
    * disk.warning: Warning threshold in % of disk space (defaults to 80%)
    * disk.critical: Critical threshold in % of disk space (defaults ot 90%)
    * disk.path: Path to calculate disk usage from (defaults to /)
    * disk.open: Which application / file manager to launch (default xdg-open)
    * disk.showUsed: Show used space (defaults to yes)
    * disk.showSize: Show total size (defaults to yes)
    * disk.showPercent: Show usage percentage (defaults to yes)
"""

import os

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.diskspace)
        )
        self._path = self.parameter("path", "/")
        self._sused = bumblebee.util.asbool(self.parameter("showUsed", True))
        self._ssize = bumblebee.util.asbool(self.parameter("showSize", True))
        self._spercent = bumblebee.util.asbool(self.parameter("showPercent", True))
        self._app = self.parameter("open", "xdg-open")
        self._perc = 0
        self._used = 0
        self._size = 0

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd="{} {}".format(self._app,
                                                          self._path))

    def diskspace(self, widget):
        if self._sused:
            used_str = bumblebee.util.bytefmt(self._used)
        else:
            used_str = ""
        if self._ssize:
            size_str = bumblebee.util.bytefmt(self._size)
        else:
            size_str = ""
        if self._spercent:
            percent_str = self._perc
        else:
            percent_str = ""
        if not self._sused or not self._ssize:
            separator = ""
        else:
            separator = "/"

        return "{} {}{}{} ({:05.02f}%)".format(self._path,
                                               used_str,
                                               separator,
                                               size_str,
                                               percent_str)

    def update(self, widgets):
        st = os.statvfs(self._path)
        self._size = st.f_blocks * st.f_frsize
        self._used = (st.f_blocks - st.f_bfree) * st.f_frsize
        self._perc = 100.0*self._used/self._size

    def state(self, widget):
        return self.threshold_state(self._perc, 80, 90)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
