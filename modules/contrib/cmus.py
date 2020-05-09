# pylint: disable=C0111,R0903

"""Displays information about the current song in cmus.

Requires the following executable:
    * cmus-remote

Parameters:
    * cmus.format: Format string for the song information. Tag values can be put in curly brackets (i.e. {artist})

      Additional tags:
        * {file} - full song file name
        * {file1} - song file name without path prefix
          if {file} = '/foo/bar.baz', then {file1} = 'bar.baz'
        * {file2} - song file name without path prefix and extension suffix
          if {file} = '/foo/bar.baz', then {file2} = 'bar'
    * cmus.layout: Space-separated list of widgets to add. Possible widgets are the buttons/toggles cmus.prev, cmus.next, cmus.shuffle and cmus.repeat, and the main display with play/pause function cmus.main.
    * cmus.server: The address of the cmus server, either a UNIX socket or host[:port]. Connects to the local instance by default.
    * cmus.passwd: The password to use for the TCP/IP connection.

contributed by `TheEdgeOfRage <https://github.com/TheEdgeOfRage>`_ - many thanks!
"""

from collections import defaultdict

import os
import string

import core.module
import core.input
import core.decorators

import util.cli
import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self._layout = self.parameter(
            "layout", "cmus.prev cmus.main cmus.next cmus.shuffle cmus.repeat"
        )
        self._fmt = self.parameter("format", "{artist} - {title} {position}/{duration}")
        self._server = self.parameter("server", None)
        self._passwd = self.parameter("passwd", None)
        self._status = None
        self._shuffle = False
        self._repeat = False
        self._tags = defaultdict(lambda: "")

        # Create widgets
        widget_map = {}
        for widget_name in self._layout.split():
            widget = self.add_widget(name=widget_name)
            self._cmd = "cmus-remote"
            if self._server is not None:
                self._cmd = "{cmd} --server {server}".format(
                    cmd=self._cmd, server=self._server
                )
                if self._passwd is not None:
                    self._cmd = "{cmd} --passwd {passwd}".format(
                        cmd=self._cmd, passwd=self._passwd
                    )

            if widget_name == "cmus.prev":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": "{cmd} -r".format(cmd=self._cmd),
                }
            elif widget_name == "cmus.main":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": "{cmd} -u".format(cmd=self._cmd),
                }
                widget.full_text(self.description)
            elif widget_name == "cmus.next":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": "{cmd} -n".format(cmd=self._cmd),
                }
            elif widget_name == "cmus.shuffle":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": "{cmd} -S".format(cmd=self._cmd),
                }
            elif widget_name == "cmus.repeat":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": "{cmd} -R".format(cmd=self._cmd),
                }
            else:
                raise KeyError(
                    "The cmus module does not support a {widget_name!r} widget".format(
                        widget_name=widget_name
                    )
                )

        # Register input callbacks
        for widget, callback_options in widget_map.items():
            core.input.register(widget, **callback_options)

    def hidden(self):
        return self._status is None

    @core.decorators.scrollable
    def description(self, widget):
        return string.Formatter().vformat(self._fmt, (), self._tags)

    def update(self):
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
        if line.startswith("file "):
            full_file = line[5:]
            file1 = os.path.basename(full_file)
            file2 = os.path.splitext(file1)[0]
            self._tags.update({"file": full_file})
            self._tags.update({"file1": file1})
            self._tags.update({"file2": file2})
            return
        name, key, value = (line.split(" ", 2) + [None, None])[:3]

        if name == "status":
            self._status = key
        if name == "tag":
            self._tags.update({key: value})
        if name in ["duration", "position"]:
            self._tags.update({name: util.format.duration(int(key))})
        if name == "set" and key == "repeat":
            self._repeat = value == "true"
        if name == "set" and key == "shuffle":
            self._shuffle = value == "true"

    def _load_song(self):
        info = ""
        try:
            info = util.cli.execute("{cmd} -Q".format(cmd=self._cmd))
        except RuntimeError:
            self._status = None

        self._tags = defaultdict(lambda: "")
        for line in info.split("\n"):
            self._eval_line(line)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
