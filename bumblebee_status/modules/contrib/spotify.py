"""Displays the current song being played and allows pausing, skipping ahead, and skipping back.

Requires the following library:
    * python-dbus

Parameters:
    * spotify.format:   Format string (defaults to '{artist} - {title}')
      Available values are: {album}, {title}, {artist}, {trackNumber}
    * spotify.layout:   Comma-separated list to change order of widgets (defaults to song, previous, pause, next)
      Widget names are: spotify.song, spotify.prev, spotify.pause, spotify.next
    * spotify.concise_controls: When enabled, allows spotify to be controlled from just the spotify.song widget.
      Concise controls are:     Left Click: Toggle Pause; Wheel Up: Next; Wheel Down; Previous.
    * spotify.bus_name: String (defaults to `spotify`)
      Available values: spotify, spotifyd

contributed by `yvesh <https://github.com/yvesh>`_ - many thanks!

added controls by `LtPeriwinkle <https://github.com/LtPeriwinkle>`_ - many thanks!

fixed icons and layout parameter by `gkeep <https://github.com/gkeep>`_ - many thanks!
"""

import sys
import dbus

import core.module
import core.widget
import core.input
import core.decorators
import util.format

import logging

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.background = True

        self.__bus_name = self.parameter("bus_name", "spotify")

        self.__layout = util.format.aslist(
            self.parameter(
                "layout", "spotify.song,spotify.prev,spotify.pause,spotify.next",
            )
        )

        self.__bus = dbus.SessionBus()
        self.__song = ""
        self.__pause = ""
        self.__format = self.parameter("format", "{artist} - {title}")

        if self.__bus_name == "spotifyd":
            self.__cmd = "dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.spotifyd \
                /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."
        else:
            self.__cmd = "dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.spotify \
                /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."

        widget_map = {}
        for widget_name in self.__layout:
            widget = self.add_widget(name=widget_name)
            if widget_name == "spotify.prev":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": self.__cmd + "Previous",
                }
                widget.set("state", "prev")
            elif widget_name == "spotify.pause":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": self.__cmd + "PlayPause",
                }
            elif widget_name == "spotify.next":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": self.__cmd + "Next",
                }
                widget.set("state", "next")
            elif widget_name == "spotify.song":
                if util.format.asbool(self.parameter("concise_controls", "false")):
                    widget_map[widget] = [
                        {
                            "button": core.input.LEFT_MOUSE,
                            "cmd": self.__cmd + "PlayPause",
                        }, {
                            "button": core.input.WHEEL_UP,
                            "cmd": self.__cmd + "Next",
                        }, {
                            "button": core.input.WHEEL_DOWN,
                            "cmd": self.__cmd + "Previous",
                        }
                    ]
            else:
                raise KeyError(
                    "The spotify module does not have a {widget_name!r} widget".format(
                        widget_name=widget_name
                    )
                )
        # is there any reason the inputs can't be directly registered above?
        for widget, callback_options in widget_map.items():
            if isinstance(callback_options, dict):
                core.input.register(widget, **callback_options)

            elif isinstance(callback_options, list): # used by concise_controls
                for opts in callback_options:
                    core.input.register(widget, **opts)


    def hidden(self):
        return self.string_song == ""

    @core.decorators.scrollable
    def __get_song(self, widget):
        bus = self.__bus
        if self.__bus_name == "spotifyd":
            spotify = bus.get_object(
                "org.mpris.MediaPlayer2.spotifyd", "/org/mpris/MediaPlayer2"
            )
        else:
            spotify = bus.get_object(
                "org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2"
            )
        spotify_iface = dbus.Interface(spotify, "org.freedesktop.DBus.Properties")
        props = spotify_iface.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        self.__song = self.__format.format(
            album=str(props.get("xesam:album")),
            title=str(props.get("xesam:title")),
            artist=",".join(props.get("xesam:artist")),
            trackNumber=str(props.get("xesam:trackNumber")),
        )
        return self.__song

    def update(self):
        try:
            if self.__bus_name == "spotifyd":
                bus = self.__bus.get_object(
                    "org.mpris.MediaPlayer2.spotifyd", "/org/mpris/MediaPlayer2"
                )
            else:
                bus = self.__bus.get_object(
                    "org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2"
                )

            for widget in self.widgets():
                if widget.name == "spotify.pause":
                    playback_status = str(
                        dbus.Interface(
                            bus,
                            "org.freedesktop.DBus.Properties",
                        ).Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
                    )
                    if playback_status == "Playing":
                        widget.set("state", "playing")
                    else:
                        widget.set("state", "paused")
                elif widget.name == "spotify.song":
                    widget.set("state", "song")
                    widget.full_text(self.__get_song(widget))

        except Exception as e:
            self.__song = ""

    @property
    def string_song(self):
        if sys.version_info.major < 3:
            return unicode(self.__song)
        return str(self.__song)
