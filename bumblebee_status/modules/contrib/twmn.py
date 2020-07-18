# pylint: disable=C0111,R0903

"""Toggle twmn notifications.

Requires the following executable:
    * systemctl

contributed by `Pseudonick47 <https://github.com/Pseudonick47>`_ - many thanks!
"""

import core.module
import core.widget
import core.input
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(""))

        self.__paused = False
        # Make sure that twmn is currently not paused
        util.cli.execute("killall -SIGUSR2 twmnd", ignore_errors=True)
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle_status)

    def toggle_status(self, event):
        self.__paused = not self.__paused

        try:
            if self.__paused:
                util.cli.execute("systemctl --user start twmnd")
            else:
                util.cli.execute("systemctl --user stop twmnd")
        except:
            self.__paused = not self.__paused  # toggling failed

    def state(self, widget):
        if self.__paused:
            return ["muted"]
        return ["unmuted"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
