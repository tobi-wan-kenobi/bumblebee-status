# pylint: disable=C0111,R0903

"""Displays information about the current song in vlc, audacious, bmp, xmms2, spotify and others

Requires the following executable:
    * playerctl

Parameters:
    * playerctl.format:   Format string (defaults to '{{artist}} - {{title}}  {{duration(position)}}/{{duration(mpris:length)}}').
      The format string is passed to 'playerctl -f' as an argument. Read `the README <https://github.com/altdesktop/playerctl#printing-properties-and-metadata>`_ for more information.
    * playerctl.layout:   Comma-separated list to change order of widgets (defaults to song, previous, pause, next)
      Widget names are: playerctl.song, playerctl.prev, playerctl.pause, playerctl.next
    * playerctl.args:     The arguments added to playerctl.
      You can check 'playerctl --help' or `its README <https://github.com/altdesktop/playerctl#using-the-cli>`_. For example, it could be '-p vlc,%any'.
    * playerctl.hide:   Hide the widgets when no players are found. Defaults to "false".

Parameters are inspired by the `spotify` module, many thanks to its developers!

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

        self.__hide = util.format.asbool(self.parameter("hide", "false"));

        self.__layout = util.format.aslist(
            self.parameter(
                "layout", "playerctl.prev, playerctl.song, playerctl.pause, playerctl.next"
            )
        )

        self.__cmd = "playerctl " + self.parameter("args", "") + " "
        self.__format = self.parameter("format", "{{artist}} - {{title}}  {{duration(position)}}/{{duration(mpris:length)}}")

        widget_map = {}
        for widget_name in self.__layout:
            widget = self.add_widget(name=widget_name)
            if widget_name == "playerctl.prev":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": self.__cmd + "previous",
                }
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

    def hidden(self):
        return self.__hide and self.status() == None

    def status(self):
        try:
            playback_status = str(util.cli.execute(self.__cmd + "status 2>&1 || true", shell = True)).strip()
            if playback_status == "No players found":
                return None
            return playback_status
        except Exception as e:
            logging.exception(e)
            return None

    def update(self):
        playback_status = self.status()
        for widget in self.widgets():
            if playback_status:
                if widget.name == "playerctl.pause":
                    if playback_status == "Playing":
                        widget.set("state", "playing")
                    elif playback_status == "Paused":
                        widget.set("state", "paused")
                    elif playback_status == "Stopped":
                        widget.set("state", "stopped")
                    else:
                        widget.set("state", "")
                elif widget.name == "playerctl.next":
                    widget.set("state", "next")
                elif widget.name == "playerctl.prev":
                    widget.set("state", "prev")
                elif widget.name == "playerctl.song":
                    widget.full_text(self.__get_song())
            else:
                widget.set("state", "")
                widget.full_text(" ")

    def __get_song(self):
        try:
            return str(util.cli.execute(self.__cmd + "metadata -f '" + self.__format + "'")).strip()
        except Exception as e:
            logging.exception(e)
            return " "
