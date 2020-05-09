# pylint: disable=C0111,R0903

"""Toggle dunst notifications.

contributed by `eknoes <https://github.com/eknoes>`_ - many thanks!
"""

import core.module
import core.widget
import core.input

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(""))
        self._paused = False
        # Make sure that dunst is currently not paused
        util.cli.execute("killall -s SIGUSR2 dunst", ignore_errors=True)
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle_status)

    def toggle_status(self, event):
        self._paused = not self._paused

        try:
            if self._paused:
                util.cli.execute("killall -s SIGUSR1 dunst")
            else:
                util.cli.execute("killall -s SIGUSR2 dunst")
        except:
            self._paused = not self._paused  # toggling failed

    def state(self, widget):
        if self._paused:
            return ["muted", "warning"]
        return ["unmuted"]
