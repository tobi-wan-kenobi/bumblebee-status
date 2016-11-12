import string
import datetime
import subprocess
from collections import defaultdict

import bumblebee.util
import bumblebee.module

def description():
    return "Displays the current song and artist playing in cmus"

def parameters():
    return [
        "cmus.format: Format of the displayed song information, arbitrary tags (as available from cmus-remote -Q) can be used (defaults to {artist} - {title} {position}/{duration})"
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._status = "default"
        self._fmt = self._config.parameter("format", "{artist} - {title} {position}/{duration}")

    def _loadsong(self):
        process = subprocess.Popen(["cmus-remote", "-Q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._query, self._error = process.communicate()
        self._query = self._query.decode("utf-8").split("\n")
        self._status = "default"

    def _tags(self):
        tags = defaultdict(lambda: '')
        for line in self._query:
            if line.startswith("status"):
                ignore, status = line.split(" ", 2)
                self._status = status
            if line.startswith("tag"):
                ignore, key, value = line.split(" ", 2)
                tags.update({ key: value })
            if line.startswith("duration"):
                ignore, sec = line.split(" ")
                tags.update({ "duration": bumblebee.util.durationfmt(int(sec)) })
            if line.startswith("position"):
                ignore, sec = line.split(" ")
                tags.update({ "position": bumblebee.util.durationfmt(int(sec)) })

        return tags

    def widgets(self):
        self._loadsong()
        tags = self._tags()

        return bumblebee.output.Widget(self, string.Formatter().vformat(self._fmt, (), tags))

    def state(self, widget):
        return self._status

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
