# pylint: disable=C0111,R0903

"""Displays information about the current song in Google Play music player.

Requires the following executable:
    * gpmdp-remote

contributed by `TheEdgeOfRage <https://github.com/TheEdgeOfRage>`_ - many thanks!
"""

import core.module
import core.widget
import core.input

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        widgets = [
            core.widget.Widget(name="gpmdp.prev"),
            core.widget.Widget(name="gpmdp.main", full_text=self.description),
            core.widget.Widget(name="gpmdp.next"),
        ]
        super().__init__(config, theme, widgets)

        core.input.register(
            widgets[0], button=core.input.LEFT_MOUSE, cmd="playerctl previous"
        )
        core.input.register(
            widgets[1], button=core.input.LEFT_MOUSE, cmd="playerctl play-pause"
        )
        core.input.register(
            widgets[2], button=core.input.LEFT_MOUSE, cmd="playerctl next"
        )

        self.__status = None
        self.__tags = None

    def description(self, widget):
        return self.__tags if self.__tags else "n/a"

    def update(self):
        self.__load_song()

    def state(self, widget):
        if widget.name == "gpmdp.prev":
            return "prev"
        if widget.name == "gpmdp.next":
            return "next"
        return self.__status

    def __load_song(self):
        info = util.cli.execute("gpmdp-remote current", ignore_errors=True)
        status = util.cli.execute("gpmdp-remote status", ignore_errors=True)
        self.__status = status.split("\n")[0].lower()
        self.__tags = info.split("\n")[0]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
