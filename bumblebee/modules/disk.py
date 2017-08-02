# pylint: disable=C0111,R0903

"""Shows free diskspace, total diskspace and the percentage of free disk space.

Parameters:
    * disk.warning: Warning threshold in % of disk space (defaults to 80%)
    * disk.critical: Critical threshold in % of disk space (defaults ot 90%)
    * disk.path: Path to calculate disk usage from (defaults to /)
    * disk.open: Which application / file manager to launch (default xdg-open)
    * disk.format: Format string, tags {path}, {used}, {left}, {size} and {percent} (defaults to "{path} {used}/{size} ({percent:05.02f}%)")
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
        self._format = self.parameter("format", "{used}/{size} ({percent:05.02f}%)")
        self._app = self.parameter("open", "xdg-open")

        self._used = 0
        self._left = 0
        self._size = 0
        self._percent = 0

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd="{} {}".format(self._app,
                                                          self._path))


    def diskspace(self, widget):
        used_str = bumblebee.util.bytefmt(self._used)
        size_str = bumblebee.util.bytefmt(self._size)
        left_str = bumblebee.util.bytefmt(self._left)
        percent_str = self._percent

        return self._format.format(path = self._path,
                                   used = used_str,
                                   left = left_str,
                                   size = size_str,
                                   percent = percent_str)


    def update(self, widgets):
        st = os.statvfs(self._path)
        self._size = st.f_blocks * st.f_frsize
        self._used = (st.f_blocks - st.f_bfree) * st.f_frsize
        self._left = self._size - self._used;
        self._percent = 100.0 * self._used/self._size

    def state(self, widget):
        return self.threshold_state(self._percent, 80, 90)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
