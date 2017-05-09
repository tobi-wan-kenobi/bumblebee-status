# pylint: disable=C0111,R0903
# -*- coding: utf-8 -*-

"""Displays information about the current song in moc.

Requires the following executable:
    * mocp

Parameters:
    * mocp.format: Format string for the song information. Tag values can be put in curly brackets (i.e. {artist})
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
            bumblebee.output.Widget(name="moc.prev"),
            bumblebee.output.Widget(name="moc.main", full_text=self.description),
            bumblebee.output.Widget(name="moc.next"),
            bumblebee.output.Widget(name="moc.shuffle"),
            bumblebee.output.Widget(name="moc.repeat"),
        ]
        super(Module, self).__init__(engine, config, widgets)

        engine.input.register_callback(widgets[0], button=bumblebee.input.LEFT_MOUSE,
            cmd="mocp -r")
        engine.input.register_callback(widgets[1], button=bumblebee.input.LEFT_MOUSE,
            cmd="mocp -G")
        engine.input.register_callback(widgets[2], button=bumblebee.input.LEFT_MOUSE,
            cmd="mocp -f")
        engine.input.register_callback(widgets[3], button=bumblebee.input.LEFT_MOUSE,
            cmd=self._toggle_shuffle)
        engine.input.register_callback(widgets[4], button=bumblebee.input.LEFT_MOUSE,
            cmd=self._toggle_repeat)

        self._fmt = self.parameter("format", "{artist} - {title} {position}/{duration}")
        self._status = None
        self._shuffle = False
        self._repeat = False
        self._tags = defaultdict(lambda: '')

    @scrollable
    def description(self, widget):
        return string.Formatter().vformat(self._fmt, (), self._tags)

    def update(self, widgets):
        self._load_song()

    def state(self, widget):
        if widget.name == "moc.shuffle":
            return "shuffle-on" if self._shuffle else "shuffle-off"
        if widget.name == "moc.repeat":
            return "repeat-on" if self._repeat else "repeat-off"
        if widget.name == "moc.prev":
            return "prev"
        if widget.name == "moc.next":
            return "next"
        return self._status

    def _load_song(self):
        info = ""
        try:
            info = bumblebee.util.execute("mocp -i")
        except RuntimeError:
            pass
        self._tags = defaultdict(lambda: '')
        for line in info.split("\n"):
            if line.startswith("State"):
                status = line.split(" ", 2)[1]
                if status == "PAUSE":
                    self._status = "paused"
                if status == "PLAY":
                    self._status = "playing"
            if line.startswith("Title"):
                value = line.split(" ", 2)[1:]
                self._tags.update({ "title": value })
            if line.startswith("Artist"):
                value = line.split(" ", 2)[1:]
                self._tags.update({ "artist": value })
            for key in  ["TotalSec", "CurrentSec"]:
                if line.startswith(key):
                    dur = int(line.split(" ")[1])
                    self._tags.update({key:bumblebee.util.durationfmt(dur)})

    def _toggle_shuffle(self, widget):
        bumblebee.util.execute("mocp -t shuffle")
        self._shuffle = False if self._shuffle else True

    def _toggle_repeat(self, widget):
        bumblebee.util.execute("mocp -t repeat")
        self._repeat = False if self._repeat else True

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
