# pylint: disable=C0111,R0903
# -*- coding: utf-8 -*-

"""Displays information about the current song in mpd.

Requires the following executable:
    * mpc

Parameters:
    * mpd.format: Format string for the song information. Tag values can be put in curly brackets (i.e. {artist})
"""

from collections import defaultdict

import string

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

from bumblebee.output import scrollable

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = [
            bumblebee.output.Widget(name="mpd.prev"),
            bumblebee.output.Widget(name="mpd.main", full_text=self.description),
            bumblebee.output.Widget(name="mpd.next"),
            bumblebee.output.Widget(name="mpd.shuffle"),
            bumblebee.output.Widget(name="mpd.repeat"),
        ]
        super(Module, self).__init__(engine, config, widgets)

        engine.input.register_callback(widgets[0], button=bumblebee.input.LEFT_MOUSE,
            cmd="mpc prev")
        engine.input.register_callback(widgets[1], button=bumblebee.input.LEFT_MOUSE,
            cmd="mpc toggle")
        engine.input.register_callback(widgets[2], button=bumblebee.input.LEFT_MOUSE,
            cmd="mpc next")
        engine.input.register_callback(widgets[3], button=bumblebee.input.LEFT_MOUSE,
            cmd="mpc random")
        engine.input.register_callback(widgets[4], button=bumblebee.input.LEFT_MOUSE,
            cmd="mpc repeat")

        self._fmt = self.parameter("format", "{artist} - {title} {position}/{duration}")
        self._status = None
        self._shuffle = False
        self._repeat = False
        self._tags = defaultdict(lambda: '')

    def description(self, widget):
        return string.Formatter().vformat(self._fmt, (), self._tags)

    def update(self, widgets):
        self._load_song()

    def state(self, widget):
        if widget.name == "mpd.shuffle":
            return "shuffle-on" if self._shuffle else "shuffle-off"
        if widget.name == "mpd.repeat":
            return "repeat-on" if self._repeat else "repeat-off"
        if widget.name == "mpd.prev":
            return "prev"
        if widget.name == "mpd.next":
            return "next"
        return self._status

    def _load_song(self):
        info = ""
        try:
            info = bumblebee.util.execute('mpc -f "tag artist %artist%\ntag title %title%"')
        except RuntimeError:
            pass
        self._tags = defaultdict(lambda: '')
        for line in info.split("\n"):
            if line.startswith("[playing]"):
                self._status = "playing"
            elif line.startswith("[paused]"):
                self._status = "paused"

            if line.startswith("["):
                timer = line.split("   ")[1]
                position = timer.split("/")[0]
                dur = timer.split("/")[1]
                duration = dur.split(" ")[0]
                self._tags.update({'position': position})
                self._tags.update({'duration': duration})

            if line.startswith("volume"):
                value = line.split("   ", 2)[1:]
                for option in value:
                    if option.startswith("repeat: on"):
                        self._repeat = True
                    elif option.startswith("repeat: off"):
                        self._repeat = False
                    elif option.startswith("random: on"):
                        self._shuffle = True
                    elif option.startswith("random: off"):
                        self._shuffle = False
            if line.startswith("tag"):
                key, value = line.split(" ", 2)[1:]
                self._tags.update({ key: value })

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
