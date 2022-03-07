# pylint: disable=C0111,R0903

"""Toggle dunst notifications using dunstctl.

When notifications are paused using this module dunst doesn't get killed and
you'll keep getting notifications on the background that will be displayed when
unpausing. This is specially useful if you're using dunst's scripting
(https://wiki.archlinux.org/index.php/Dunst#Scripting), which requires dunst to
be running. Scripts will be executed when dunst gets unpaused.

Requires:
    * dunst v1.5.0+

contributed by `cristianmiranda <https://github.com/cristianmiranda>`_ - many thanks!
contributed by `joachimmathes <https://github.com/joachimmathes>`_ - many thanks!
"""

import core.module
import core.widget
import core.input
import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(""))
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.toggle_state)
        self.__states = {"unknown": ["unknown", "critical"],
                         "true": ["muted", "warning"],
                         "false": ["unmuted"]}

    def toggle_state(self, event):
        util.cli.execute("dunstctl set-paused toggle", ignore_errors=True)

    def state(self, widget):
        return self.__states[self.__is_dunst_paused()]

    def __is_dunst_paused(self):
        result = util.cli.execute("dunstctl is-paused",
                                  return_exitcode=True,
                                  ignore_errors=True)
        return result[1].rstrip() if result[0] == 0 else "unknown"
