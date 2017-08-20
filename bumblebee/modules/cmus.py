# pylint: disable=C0111,R0903
# -*- coding: utf-8 -*-

"""Displays information about the current song in cmus.

Requires the following executable:
    * cmus-remote

Parameters:
    * cmus.format: Format string for the song information. Tag values can be put in curly brackets (i.e. {artist})
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
            bumblebee.output.Widget(name="cmus.prev"),
            bumblebee.output.Widget(name="cmus.main", full_text=self.description),
            bumblebee.output.Widget(name="cmus.next"),
            bumblebee.output.Widget(name="cmus.shuffle"),
            bumblebee.output.Widget(name="cmus.repeat"),
        ]
        super(Module, self).__init__(engine, config, widgets)

        engine.input.register_callback(widgets[0], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -r")
        engine.input.register_callback(widgets[1], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -u")
        engine.input.register_callback(widgets[2], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -n")
        engine.input.register_callback(widgets[3], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -S")
        engine.input.register_callback(widgets[4], button=bumblebee.input.LEFT_MOUSE,
            cmd="cmus-remote -R")

        self._fmt = self.parameter("format", "{artist} - {title} {position}/{duration}")
        self._status = None
        self._shuffle = False
        self._repeat = False
        self._tags = defaultdict(lambda: '')

    def hidden(self):
        return self._status == None

    @scrollable
    def description(self, widget):
        return string.Formatter().vformat(self._fmt, (), self._tags)

    def update(self, widgets):
        self._load_song()

    def state(self, widget):
        returns = {
            "cmus.shuffle": "shuffle-on" if self._shuffle else "shuffle-off",
            "cmus.repeat": "repeat-on" if self._repeat else "repeat-off",
            "cmus.prev": "prev",
            "cmus.next": "next",
        }
        return returns.get(widget.name, self._status)

    def _eval_line(self, line):
        # not a typo, use decode detection to see whether we are
        # dealing with Python2 or Python3
        if hasattr(line, "decode"):
            line = line.encode("utf-8", "replace")
        name, key, value  = (line.split(" ", 2) + [None, None])[:3]

        if name == "status":
            self._status = key
        if name == "tag":
            self._tags.update({key: value})
        if name in ["duration", "position"]:
            self._tags.update({name:bumblebee.util.durationfmt(int(key))})
        if name == "set" and key == "repeat":
            self._repeat = value == "true"
        if name == "set" and key == "shuffle":
            self._shuffle = value == "true"

    def _load_song(self):
        info = ""
        try:
            info = bumblebee.util.execute("cmus-remote -Q")
        except RuntimeError:
            self._status = None

        self._tags = defaultdict(lambda: '')
        for line in info.split("\n"):
            self._eval_line(line)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
