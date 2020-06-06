# pylint: disable=C0111,R0903

"""Displays information about the current song in vlc, audacious, bmp, xmms2, spotify and others

Requires the following executable:
    * playerctl

contributed by `smitajit <https://github.com/smitajit>`_ - many thanks!

"""

import core.module
import core.widget
import core.input
import util.cli

class Module(core.module.Module):
    def __init__(self,config , theme):
        widgets = [
            core.widget.Widget(name="playerctl.prev"),
            core.widget.Widget(name="playerctl.main", full_text=self.description),
            core.widget.Widget(name="playerctl.next"),
        ]
        super(Module, self).__init__(config, theme ,  widgets)

        core.input.register(widgets[0], button=core.input.LEFT_MOUSE,
            cmd="playerctl previous")
        core.input.register(widgets[1], button=core.input.LEFT_MOUSE,
             cmd="playerctl play-pause")
        core.input.register(widgets[2], button=core.input.LEFT_MOUSE,
             cmd="playerctl next")

        self._status = None
        self._tags = None

    def description(self, widget):
        return self._tags if self._tags else "..."

    def update(self):
        self._load_song()

    def state(self, widget):
        if widget.name == "playerctl.prev":
            return "prev"
        if widget.name == "playerctl.next":
            return "next"
        return self._status

    def _load_song(self):
        info = ""
        try:
            status = util.cli.execute("playerctl status").lower()
            info = util.cli.execute("playerctl metadata xesam:title")
        except :
            self._status = None
            self._tags = None
            return
        self._status = status.split("\n")[0].lower()
        self._tags = info.split("\n")[0][:20]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
