# pylint: disable=C0111,R0903

"""
Toggle dunst notifications using dunstctl.

When notifications are paused using this module dunst doesn't get killed and you'll keep getting notifications on the background that will be displayed when unpausing.
This is specially useful if you're using dunst's scripting (https://wiki.archlinux.org/index.php/Dunst#Scripting), which requires dunst to be running. Scripts will be executed when dunst gets unpaused.

Requires:
    * dunst v1.5.0+

contributed by `cristianmiranda <https://github.com/cristianmiranda>`_ - many thanks!
"""

import core.module
import core.widget
import core.input

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(""))
        self._paused = self.__isPaused()
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle_status)

    def toggle_status(self, event):
        self._paused = self.__isPaused()
        if self._paused:
            util.cli.execute("dunstctl set-paused false")
        else:
            util.cli.execute("dunstctl set-paused true")
        self._paused = not self._paused

    def __isPaused(self):
        return util.cli.execute("dunstctl is-paused").strip() == "true"

    def state(self, widget):
        if self._paused:
            return ["muted", "warning"]
        return ["unmuted"]
