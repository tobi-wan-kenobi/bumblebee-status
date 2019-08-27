#pylint: disable=C0111,R0903

"""Enable/disable automatic screen locking.

Requires the following executables:
    * xdg-screensaver
    * xdotool
    * notify-send
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import psutil
import os

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text="")
        )
        self._active = False
        self._xid = 0
        
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._toggle
        )

    def state(self, widget):
        if self._active:
            return "activated"
        return "deactivated"

    def _toggle(self, event):
        self._active = not self._active
        try:
            if self._active:
                self._xid = bumblebee.util.execute("xdotool search --class \"i3bar\"").strip()
                bumblebee.util.execute("xdg-screensaver suspend {}".format(self._xid))
                bumblebee.util.execute("notify-send \"Consuming caffeine\"")
            else:
                for process in psutil.process_iter():
                    if process.cmdline() == ['/usr/bin/xprop','-id',str(self._xid),'-spy']:
                        pid = process.pid
                os.kill(pid,9)
                bumblebee.util.execute("notify-send \"Out of coffee\"")
        except:
            self._active = not self._active

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
