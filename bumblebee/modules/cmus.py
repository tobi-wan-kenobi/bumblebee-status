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

        output.add_callback(module="cmus.prev", button=1, cmd="cmus-remote -r")
        output.add_callback(module="cmus.next", button=1, cmd="cmus-remote -n")
        output.add_callback(module="cmus.shuffle", button=1, cmd="cmus-remote -S")
        output.add_callback(module="cmus.repeat", button=1, cmd="cmus-remote -R")
        output.add_callback(module=self.instance(), button=1, cmd="cmus-remote -u")

    def _loadsong(self):
        process = subprocess.Popen(["cmus-remote", "-Q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._query, self._error = process.communicate()
        self._query = self._query.decode("utf-8").split("\n")
        self._status = "default"

    def _tags(self):
        tags = defaultdict(lambda: '')
        for line in self._query:
            if line.startswith("status"):
                status = line.split(" ", 2)[1]
                self._status = status
            if line.startswith("tag"):
                key, value = line.split(" ", 2)[1:]
                tags.update({ key: value })
            if line.startswith("duration"):
                sec = line.split(" ")[1]
                tags.update({ "duration": bumblebee.util.durationfmt(int(sec)) })
            if line.startswith("position"):
                sec = line.split(" ")[1]
                tags.update({ "position": bumblebee.util.durationfmt(int(sec)) })
            if line.startswith("set repeat "):
                self._repeat = False if line.split(" ")[2] == "false" else True
            if line.startswith("set shuffle "):
                self._shuffle = False if line.split(" ")[2] == "false" else True

        return tags

    def widgets(self):
        self._loadsong()
        tags = self._tags()

        return [
            bumblebee.output.Widget(self, "", instance="cmus.prev"),
            bumblebee.output.Widget(self, string.Formatter().vformat(self._fmt, (), tags)),
            bumblebee.output.Widget(self, "", instance="cmus.next"),
            bumblebee.output.Widget(self, "", instance="cmus.shuffle"),
            bumblebee.output.Widget(self, "", instance="cmus.repeat"),
        ]

    def state(self, widget):
        if widget.instance() == "cmus.shuffle":
            return "on" if self._shuffle else "off"
        if widget.instance() == "cmus.repeat":
            return "on" if self._repeat else "off"
        return self._status

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
