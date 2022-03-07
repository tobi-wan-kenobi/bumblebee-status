# pylint: disable=C0111,R0903

"""Displays the current song being played in DeaDBeeF and provides
some media control bindings.
Left click toggles pause, scroll up skips the current song, scroll
down returns to the previous song.

Parameters:
    * deadbeef.format:    Format string (defaults to '{artist} - {title}')
      Available values are: {artist}, {title}, {album}, {length},
      {trackno}, {year}, {comment},
      {copyright}, {time}
      This is deprecated, but much simpler.
    * deadbeef.tf_format: A foobar2000 title formatting-style format string.
      These can be much more sophisticated than the standard
      format strings. This is off by default, but specifying
      any tf_format will enable it. If both deadbeef.format
      and deadbeef.tf_format are specified, deadbeef.tf_format
      takes priority.
    * deadbeef.tf_format_if_stopped: Controls whether or not the tf_format format
      string should be displayed even if no song is paused or
      playing. This could be useful if you want to implement
      your own stop strings with the built in logic. Any non-
      null value will enable this (by default the module will
      hide itself when the player is stopped).
    * deadbeef.previous:  Change binding for previous song (default is left click)
    * deadbeef.next:      Change binding for next song (default is right click)
    * deadbeef.pause:     Change binding for toggling pause (default is middle click)

    Available options for deadbeef.previous, deadbeef.next and deadbeef.pause are:
        LEFT_CLICK, RIGHT_CLICK, MIDDLE_CLICK, SCROLL_UP, SCROLL_DOWN

contributed by `joshbarrass <https://github.com/joshbarrass>`_ - many thanks!
"""
import sys

import subprocess
import logging

import core.module
import core.widget
import core.input
import core.decorators

import util.cli
import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.deadbeef))

        buttons = {
            "LEFT_CLICK": core.input.LEFT_MOUSE,
            "RIGHT_CLICK": core.input.RIGHT_MOUSE,
            "MIDDLE_CLICK": core.input.MIDDLE_MOUSE,
            "SCROLL_UP": core.input.WHEEL_UP,
            "SCROLL_DOWN": core.input.WHEEL_DOWN,
        }

        self._song = ""
        self._format = self.parameter("format", "{artist} - {title}")
        self._tf_format = self.parameter("tf_format", "")
        self._show_tf_when_stopped = util.format.asbool(
            self.parameter("tf_format_if_stopped", False)
        )
        prev_button = self.parameter("previous", "LEFT_CLICK")
        next_button = self.parameter("next", "RIGHT_CLICK")
        pause_button = self.parameter("pause", "MIDDLE_CLICK")

        self.now_playing = "deadbeef --nowplaying %a;%t;%b;%l;%n;%y;%c;%r;%e"
        self.now_playing_tf = "deadbeef --nowplaying-tf "
        cmd = "deadbeef "

        core.input.register(self, button=buttons[prev_button], cmd=cmd + "--prev")
        core.input.register(self, button=buttons[next_button], cmd=cmd + "--next")
        core.input.register(
            self, button=buttons[pause_button], cmd=cmd + "--play-pause"
        )

        # modify the tf_format if we don't want it to show on stop
        # this adds conditions to the query itself, rather than
        # polling to see if deadbeef is running
        # doing this reduces the number of calls we have to make
        if self._tf_format and not self._show_tf_when_stopped:
            self._tf_format = "$if($or(%isplaying%,%ispaused%),{query})".format(
                query=self._tf_format
            )

    @core.decorators.scrollable
    def deadbeef(self, widget):
        return self.string_song

    def hidden(self):
        return self.string_song == ""

    def update(self):
        widgets = self.widgets()
        try:
            if self._tf_format == "":  # no tf format set, use the old style
                return self.update_standard(widgets)
            return self.update_tf(widgets)
        except Exception as e:
            logging.exception(e)
            self._song = "error"

    def update_tf(self, widgets):
        ## ensure that deadbeef is actually running
        ## easiest way to do this is to check --nowplaying for
        ##  the string 'nothing'
        if util.cli.execute(self.now_playing) == "nothing":
            self._song = ""
            return
        ## perform the actual query -- these can be much more sophisticated
        data = util.cli.execute(self.now_playing_tf + '"'+self._tf_format+'"')
        self._song = data

    def update_standard(self, widgets):
        data = util.cli.execute(self.now_playing)
        if data == "nothing":
            self._song = ""
        else:
            data = data.split(";")
            self._song = self._format.format(
                artist=data[0],
                title=data[1],
                album=data[2],
                length=data[3],
                trackno=data[4],
                year=data[5],
                comment=data[6],
                copyright=data[7],
                time=data[8],
            )

    @property
    def string_song(self):
        """\
Returns the current song as a string, either as a unicode() (Python <
3) or a regular str() (Python >= 3)
        """
        if sys.version_info.major < 3:
            return unicode(self._song)
        return str(self._song)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
