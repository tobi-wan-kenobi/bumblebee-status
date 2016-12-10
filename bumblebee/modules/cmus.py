# pylint: disable=C0111,R0903

"""Displays information about the current song in cmus."""

from collections import defaultdict

import string

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

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
        self._fmt = self.parameter("format", "{artist} - {title} {position}/{duration}")

    def description(self):
        return string.Formatter().vformat(self._fmt, (), self._tags)

    def update(self, widgets):
        self._load_song()

    def _load_song(self):
        info = ""
        try:
            info = bumblebee.util.execute("cmus-remote -Q")
        except RuntimeError:
            pass
        self._tags = defaultdict(lambda: '')
        for line in info.split("\n"):
            if line.startswith("status"):
                self._status = line.split(" ", 2)[1]
            if line.startswith("tag"):
                key, value = line.split(" ", 2)[1:]
                self._tags.update({ key: value })
            if line.startswith("duration"):
                self._tags.update({
                    "duration": bumblebee.util.durationfmt(int(line.split(" ")[1]))
                })
            if line.startswith("position"):
                self._tags.update({
                    "position": bumblebee.util.durationfmt(int(line.split(" ")[1]))
                })
            if line.startswith("set repeat "):
                self._repeat = False if "false" in line else True
            if line.startswith("set shuffle "):
                self._shuffle = False if "false" in line else True
