# pylint: disable=C0111,R0903

"""Displays information about the current song in vlc, audacious, bmp, xmms2, spotify and others

Requires the following executable:
    * playerctl

Parameters:
    * playerctl.format:   Format string (defaults to '{artist} - {title}')
      Available values are: {album}, {title}, {artist}, {trackNumber}
    * playerctl.layout:   Comma-separated list to change order of widgets (defaults to song, previous, pause, next)
      Widget names are: playerctl.song, playerctl.prev, playerctl.pause, playerctl.next

Parameters are inherited from `spotify` module, many thanks to its developers!

contributed by `smitajit <https://github.com/smitajit>`_ - many thanks!
"""

import core.module
import core.widget
import core.input
import util.cli
import util.format

import logging

class Module(core.module.Module):
    def __init__(self, config, theme):
        super(Module, self).__init__(config, theme, [])

        self.background = True

        self.__layout = util.format.aslist(
            self.parameter(
                "layout", "playerctl.prev, playerctl.song, playerctl.pause, playerctl.next"
            )
        )

        self.__song = ""
        self.__cmd = "playerctl "
        self.__format = self.parameter("format", "{artist} - {title}")

        widget_map = {}
        for widget_name in self.__layout:
            widget = self.add_widget(name=widget_name)
            if widget_name == "playerctl.prev":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": self.__cmd + "previous",
                }
                widget.set("state", "prev")
            elif widget_name == "playerctl.pause":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": self.__cmd + "play-pause",
                }
            elif widget_name == "playerctl.next":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": self.__cmd + "next",
                }
                widget.set("state", "next")
            elif widget_name == "playerctl.song":
                widget_map[widget] = [
                    {
                        "button": core.input.LEFT_MOUSE,
                        "cmd": self.__cmd + "play-pause",
                    }, {
                        "button": core.input.WHEEL_UP,
                        "cmd": self.__cmd + "next",
                    }, {
                        "button": core.input.WHEEL_DOWN,
                        "cmd": self.__cmd + "previous",
                    }
                ]
            else:
                raise KeyError(
                    "The playerctl module does not have a {widget_name!r} widget".format(
                        widget_name=widget_name
                    )
                )

        for widget, callback_options in widget_map.items():
            if isinstance(callback_options, dict):
                core.input.register(widget, **callback_options)

    def update(self):
        try:
            self.__get_song()

            for widget in self.widgets():
                if widget.name == "playerctl.pause":
                    playback_status = str(util.cli.execute(self.__cmd + "status")).strip()
                    if playback_status != "":
                        if playback_status == "Playing":
                            widget.set("state", "playing")
                        else:
                            widget.set("state", "paused")
                elif widget.name == "playerctl.song":
                    widget.set("state", "song")
                    widget.full_text(self.__song)
        except Exception as e:
            logging.exception(e)
            self.__song = ""

    def __get_song(self):
        album = str(util.cli.execute(self.__cmd + "metadata xesam:album")).strip()
        title = str(util.cli.execute(self.__cmd + "metadata xesam:title")).strip()
        artist = str(util.cli.execute(self.__cmd + "metadata xesam:albumArtist")).strip()
        track_number = str(util.cli.execute(self.__cmd + "metadata xesam:trackNumber")).strip()

        self.__song = self.__format.format(
            album = album,
            title = title,
            artist = artist,
            trackNumber = track_number
        )
