# pylint: disable=C0111,R0903

"""Displays APT package update information (<to upgrade>/<to remove>/<kept back>)

Requires the following packages:
    * apt

Optional (for instant refresh when packages are installed/removed):
    * inotify-tools (inotifywait) — falls back to mtime polling if unavailable

Parameters:
    * apt.format:
        Format string for the output. May contain any combination of the
        following named placeholders:
            * {to_upgrade}
            * {to_remove}
            * {kept_back}

        All placeholders are optional.

        Default:
            "{to_upgrade} to upgrade, {to_remove} to remove".

        Notes:
            * With the default format, "kept back" is only shown when
              kept_back > 0.
            * Custom format strings are rendered as-is and do not include
              conditional logic.
    * apt.warning: Integer to set the threshold for warning state (defaults to 0)
    * apt.critical: Integer to set the threshold for critical state (defaults to 50)

contributed by `qba10 <https://github.com/qba10>`_ - many thanks!
"""

import os
import re
import shutil
import subprocess
import threading
import time

import core.event
import core.module
import core.widget
import core.decorators
import core.input
import util.cli
import util.format


class Module(core.module.Module):
    @core.decorators.every(minutes=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.updates))
        self.__default_format = "{to_upgrade} to upgrade, {to_remove} to remove"
        self.__format = self.parameter("format", self.__default_format)
        self.__threshold_warning = util.format.asint(self.parameter("warning", 0))
        self.__threshold_critical = util.format.asint(self.parameter("critical", 50))
        self.background = True
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=lambda event: self.update_wrapper())

        monitor = threading.Thread(target=self._watch_dpkg, daemon=True)
        monitor.start()

    def updates(self, widget):
        if widget.get("error"):
            return widget.get("error")

        up = widget.get("to_upgrade", 0)
        rm = widget.get("to_remove", 0)
        kept = widget.get("not_upgraded", 0)

        if self.__format == self.__default_format:
            result = self.__format.format(
                to_upgrade=up, to_remove=rm, kept_back=kept
            )
            if kept > 0:
                result = "{}, {} kept back".format(result, kept)
        else:
            try:
                result = self.__format.format(
                    to_upgrade=up, to_remove=rm, kept_back=kept
                )
            except KeyError as e:
                return "Format error: unknown placeholder {}".format(e)

        return result

    def update(self):
        widget = self.widget()
        try:
            res = util.cli.execute("apt-get -s dist-upgrade")
            up, _new, rm, kept = self._parse_result(res)
            widget.set("error", None)
            widget.set("to_upgrade", up)
            widget.set("to_remove", rm)
            widget.set("not_upgraded", kept)
        except Exception as e:
            widget.set("error", "APT error: {}".format(e))

    def state(self, widget):
        if widget.get("error"):
            return "critical"
        total = sum([widget.get(t, 0) for t in ["to_upgrade", "to_remove", "not_upgraded"]])
        if total > self.__threshold_critical:
            return "critical"
        if total > self.__threshold_warning:
            return "warning"
        return "good"

    def _parse_result(self, to_parse):
        pattern = r"(\d+) upgraded, (\d+) newly installed, (\d+) to remove(?: and (\d+) not upgraded)?"
        for line in reversed(to_parse.splitlines()):
            match = re.search(pattern, line)
            if match:
                vals = [int(x) if x else 0 for x in match.groups()]
                return tuple(vals)
        return 0, 0, 0, 0

    def _watch_dpkg(self):
        dpkg_status = "/var/lib/dpkg/status"
        if shutil.which("inotifywait"):
            self._watch_inotify(dpkg_status)
        else:
            self._watch_mtime(dpkg_status)

    def _watch_inotify(self, path):
        # Watch the directory, not the file — dpkg atomically replaces
        # status via rename, which fires on the directory inode, not the file's
        watch_dir = os.path.dirname(path)
        watch_file = os.path.basename(path)
        try:
            proc = subprocess.Popen(
                ["inotifywait", "-m", "-e", "close_write,moved_to", watch_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            for line in proc.stdout:
                if not threading.main_thread().is_alive():
                    proc.terminate()
                    return
                # output format: "<dir>/ <EVENTS> <filename>"
                parts = line.decode().strip().split()
                if len(parts) >= 3 and parts[2] == watch_file:
                    self.update_wrapper()
        except Exception:
            self._watch_mtime(path)

    def _watch_mtime(self, path):
        try:
            last_mtime = os.stat(path).st_mtime
        except OSError:
            last_mtime = None

        while threading.main_thread().is_alive():
            time.sleep(30)
            try:
                mtime = os.stat(path).st_mtime
                if last_mtime is not None and mtime != last_mtime:
                    self.update_wrapper()
                last_mtime = mtime
            except OSError:
                pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
