#pylint: disable=C0111,R0903,W0212

"""Enable/disable automatic screen locking.

Requires the following executables:
    * xdg-screensaver
    * xdotool
    * xprop (as dependency for xdotool)
    * notify-send
"""

import logging
import os
import psutil
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text="")
        )
        self._active = False
        self._xid = None

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._toggle
        )

    def _check_requirements(self):
        requirements = ['xdotool', 'xprop', 'xdg-screensaver']
        missing = []
        for tool in requirements:
            if not bumblebee.util.which(tool):
                missing.append(tool)
        return missing

    def _get_i3bar_xid(self):
        xid = bumblebee.util.execute("xdotool search --class \"i3bar\"").partition('\n')[0].strip()
        if xid.isdigit():
            return xid
        logging.warning("Module caffeine: xdotool couldn't get X window ID of \"i3bar\".")
        return None

    def _notify(self):
        if not bumblebee.util.which('notify-send'):
            return

        if self._active:
            bumblebee.util.execute("notify-send \"Consuming caffeine\"")
        else:
            bumblebee.util.execute("notify-send \"Out of coffee\"")

    def _suspend_screensaver(self):
        self._xid = self._get_i3bar_xid()
        if self._xid is None:
            return False

        pid = os.fork()
        if pid == 0:
            os.setsid()
            bumblebee.util.execute("xdg-screensaver suspend {}".format(self._xid))
            os._exit(0)
        else:
            os.waitpid(pid, 0)
        return True

    def _resume_screensaver(self):
        success = True
        xprop_path = bumblebee.util.which('xprop')
        pids = [ p.pid for p in psutil.process_iter() if p.cmdline() == [xprop_path, '-id', str(self._xid), '-spy'] ]
        for pid in pids:
            try:
                os.kill(pid, 9)
            except OSError:
                success = False
        return success

    def state(self, _):
        if self._active:
            return "activated"
        return "deactivated"

    def _toggle(self, _):
        missing = self._check_requirements()
        if missing:
            logging.warning('Could not run caffeine - missing %s!', ", ".join(missing))
            return

        self._active = not self._active
        if self._active:
            success = self._suspend_screensaver()
        else:
            success = self._resume_screensaver()

        if success:
            self._notify()
        else:
            self._active = not self._active

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
