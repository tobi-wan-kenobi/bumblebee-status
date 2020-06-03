# pylint: disable=C0111,R0903

"""Displays information about the current song in vlc, audacious, bmp, xmms2, spotify and others

Requires the following executable:
    * playerctl

contributed by `smitajit <https://github.com/smitajit>`_ - many thanks!

"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = [
            bumblebee.output.Widget(name="playerctl.prev"),
            bumblebee.output.Widget(name="playerctl.main", full_text=self.description),
            bumblebee.output.Widget(name="playerctl.next"),
        ]
        super(Module, self).__init__(engine, config, widgets)

        engine.input.register_callback(widgets[0], button=bumblebee.input.LEFT_MOUSE,
            cmd="playerctl previous")
        engine.input.register_callback(widgets[1], button=bumblebee.input.LEFT_MOUSE,
             cmd="playerctl play-pause")
        engine.input.register_callback(widgets[2], button=bumblebee.input.LEFT_MOUSE,
             cmd="playerctl next")

        self._status = None
        self._tags = None

    def description(self, widget):
        return self._tags if self._tags else "..."

    def update(self, widgets):
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
            status = bumblebee.util.execute("playerctl status")
            info = bumblebee.util.execute("playerctl metadata xesam:title")
        except :
            self._status = None
            self._tags = None
            return
        self._status = status.split("\n")[0].lower()
        self._tags = info.split("\n")[0][:20]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
