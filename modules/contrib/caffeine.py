# pylint: disable=C0111,R0903,W0212

"""Enable/disable automatic screen locking.

Requires the following executables:
    * xdg-screensaver
    * xdotool
    * xprop (as dependency for xdotool)
    * notify-send

contributed by `TheEdgeOfRage <https://github.com/TheEdgeOfRage>`_ - many thanks!
"""

import logging
import os
import shutil
import psutil

import core.module
import core.widget
import core.input
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(minutes=10)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(""))

        self.__active = False
        self.__xid = None

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__toggle)

    def __check_requirements(self):
        requirements = ["xdotool", "xprop", "xdg-screensaver"]
        missing = []
        for tool in requirements:
            if not shutil.which(tool):
                missing.append(tool)
        return missing

    def __get_i3bar_xid(self):
        xid = (
            util.cli.execute("xdotool search --class 'i3bar'")
            .partition("\n")[0]
            .strip()
        )
        if xid.isdigit():
            return xid
        logging.warning("Module caffeine: xdotool couldn't get X window ID of 'i3bar'.")
        return None

    def __notify(self):
        if not shutil.which("notify-send"):
            return

        if self.__active:
            util.cli.execute("notify-send 'Consuming caffeine'")
        else:
            util.cli.execute("notify-send 'Out of coffee'")

    def _suspend_screensaver(self):
        self.__xid = self.__get_i3bar_xid()
        if self.__xid is None:
            return False

        pid = os.fork()
        if pid == 0:
            os.setsid()
            util.cli.execute("xdg-screensaver suspend {}".format(self.__xid))
            os._exit(0)
        else:
            os.waitpid(pid, 0)
        return True

    def __resume_screensaver(self):
        success = True
        xprop_path = shutil.which("xprop")
        pids = [
            p.pid
            for p in psutil.process_iter()
            if p.cmdline() == [xprop_path, "-id", str(self.__xid), "-spy"]
        ]
        for pid in pids:
            try:
                os.kill(pid, 9)
            except OSError:
                success = False
        return success

    def state(self, _):
        if self.__active:
            return "activated"
        return "deactivated"

    def __toggle(self, _):
        missing = self.__check_requirements()
        if missing:
            logging.warning("Could not run caffeine - missing %s!", ", ".join(missing))
            return

        self.__active = not self.__active
        if self.__active:
            success = self._suspend_screensaver()
        else:
            success = self.__resume_screensaver()

        if success:
            self.__notify()
        else:
            self.__active = not self.__active


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
