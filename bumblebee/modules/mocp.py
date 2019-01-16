# pylint: disable=C0111,R0903
# -*- coding: utf-8 -*-

"""Displays information about the current song in mocp. Left click toggles play/pause. Right click toggles shuffle.

Requires the following executable:
    * mocp

Parameters:
    * mocp.format: Format string for the song information. Replace string sequences with the actual information:
         %state     State
         %file      File
         %title     Title, includes track, artist, song title and album
         %artist    Artist
         %song      SongTitle
         %album     Album
         %tt        TotalTime
         %tl        TimeLeft
         %ts        TotalSec
         %ct        CurrentTime
         %cs        CurrentSec
         %b         Bitrate
         %r         Sample rate
"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

from bumblebee.output import scrollable

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(name="mocp.main", full_text=self.description)
                                     )

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="mocp -G")
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd="mocp -t shuffle")
        self._format = self.parameter("format", "%state %artist - %song | %ct/%tt")
        self._running = 0

    #@scrollable
    def description(self, widget):
        return self._info if self._running == 1 else "Music On Console Player"

    def update(self, widgets):
        self._load_song()

    def _load_song(self):
        try:
            self._info = bumblebee.util.execute("mocp -Q '" + self._format +  "'" ).strip()
            self._running = 1
        except RuntimeError:
            self._running = 0

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
