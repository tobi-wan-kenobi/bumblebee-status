# pylint: disable=C0111,R0903
# -*- coding: utf-8 -*-

"""Displays information about the current song in mocp. Left click toggles play/pause. Right click toggles shuffle.

Requires the following executable:
    * mocp

Parameters:
    * mocp.format: Format string for the song information. Replace string sequences with the actual information:

       * %state     State
       * %file      File
       * %title     Title, includes track, artist, song title and album
       * %artist    Artist
       * %song      SongTitle
       * %album     Album
       * %tt        TotalTime
       * %tl        TimeLeft
       * %ts        TotalSec
       * %ct        CurrentTime
       * %cs        CurrentSec
       * %b         Bitrate
       * %r         Sample rate

contributed by `chrugi <https://github.com/chrugi>`_ - many thanks!
"""

import core.module
import core.widget
import core.input

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.description))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd="mocp -G")
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd="mocp -t shuffle")
        self.__format = self.parameter("format", "%state %artist - %song | %ct/%tt")
        self.__running = False

    def description(self, widget):
        return self.__info if self.__running == True else "Music On Console Player"

    def update(self):
        self.__load_song()

    def __load_song(self):
        try:
            self.__info = util.cli.execute("mocp -Q '{}'".format(self.__format)).strip()
            self.__running = True
        except RuntimeError:
            self.__running = False


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
