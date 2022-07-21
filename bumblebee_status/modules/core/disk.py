# pylint: disable=C0111,R0903

"""Shows free diskspace, total diskspace and the percentage of free disk space.

Parameters:
    * disk.warning: Warning threshold in % of disk space (defaults to 80%)
    * disk.critical: Critical threshold in % of disk space (defaults to 90%)
    * disk.path: Path to calculate disk usage from (defaults to /)
    * disk.open: Which application / file manager to launch (default xdg-open)
    * disk.format: Format string, tags {path}, {used}, {left}, {size} and {percent} (defaults to '{path} {used}/{size} ({percent:05.02f}%)')
    * disk.system: Unit system to use - SI (KB, MB, ...) or IEC (KiB, MiB, ...) (defaults to 'IEC')
"""

import os

import core.module
import core.widget
import core.input

import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.diskspace))

        self._path = self.parameter("path", "/")
        self._format = self.parameter("format", "{used}/{size} ({percent:05.02f}%)")
        self._system = self.parameter("system", "IEC")

        self._used = 0
        self._left = 0
        self._size = 0
        self._percent = 0

        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd="{} {}".format(self.parameter("open", "xdg-open"), self._path),
        )

    def diskspace(self, widget):
        used_str = util.format.byte(self._used, sys=self._system)
        size_str = util.format.byte(self._size, sys=self._system)
        left_str = util.format.byte(self._left, sys=self._system)
        percent_str = self._percent

        return self._format.format(
            path=self._path,
            used=used_str,
            left=left_str,
            size=size_str,
            percent=percent_str,
        )

    def update(self):
        st = os.statvfs(self._path)
        self._size = st.f_blocks * st.f_frsize
        self._used = (st.f_blocks - st.f_bfree) * st.f_frsize
        self._left = self._size - self._used
        self._percent = 100.0 * self._used / self._size

    def state(self, widget):
        return self.threshold_state(self._percent, 80, 90)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
