#pylint: disable=C0111,R0903

"""Enable/disable automatic screen locking.

Requires the following executables:
    * xdg-screensaver
    * notify-send
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text="")
        )
        self._active = False
        self.interval(1)
        
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
                bumblebee.util.execute("xdg-screensaver reset")
                bumblebee.util.execute("notify-send \"Consuming caffeine\"")
            else:
                bumblebee.util.execute("notify-send \"Out of coffee\"")
        except:
            self._active = not self._active

    def update(self, widgets):
        if self._active:
            bumblebee.util.execute("xdg-screensaver reset")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
