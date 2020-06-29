"""Displays the current song being played and allows pausing, skipping ahead, and skipping back.

Requires the following library:
    * python-dbus

Parameters:
    * spotify.format:   Format string (defaults to '{artist} - {title}')
      Available values are: {album}, {title}, {artist}, {trackNumber}
    * spotify.layout:   Space-separated list to change order of widgets (defaults to song, previous, pause, next)
      Widget names are: spotify.song, spotify.prev, spotify.pause, spotify.next
      Example: `spotify.layout="spotify.prev spotify.song spotify.pause spotify.next"`

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


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.__layout = self.parameter(
            "layout", "spotify.song spotify.prev spotify.pause spotify.next",
        )

        self.__song = ""
        self.__pause = ""
        self.__format = self.parameter("format", "{artist} - {title}")

        self.__cmd = "dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.spotify \
                /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."

    def hidden(self):
        return self.string_song == ""

    def __get_song(self):
        bus = dbus.SessionBus()
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

    def update(self):
        try:
            self.clear_widgets()
            self.__get_song()

            widget_map = {}
            for widget_name in self.__layout.split():
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
                    playback_status = str(
                        dbus.Interface(
                            dbus.SessionBus().get_object(
                                "org.mpris.MediaPlayer2.spotify",
                                "/org/mpris/MediaPlayer2",
                            ),
                            "org.freedesktop.DBus.Properties",
                        ).Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
                    )
                    if playback_status == "Playing":
                        widget.set("state", "playing")
                    else:
                        widget.set("state", "paused")
                elif widget_name == "spotify.next":
                    widget_map[widget] = {
                        "button": core.input.LEFT_MOUSE,
                        "cmd": self.__cmd + "Next",
                    }
                    widget.set("state", "next")
                elif widget_name == "spotify.song":
                    widget.set("state", "song")
                    widget.full_text(self.__song)
                else:
                    raise KeyError(
                        "The spotify module does not have a {widget_name!r} widget".format(
                            widget_name=widget_name
                        )
                    )
            for widget, callback_options in widget_map.items():
                core.input.register(widget, **callback_options)

        except Exception:
            self.__song = ""

    @property
    def string_song(self):
        if sys.version_info.major < 3:
            return unicode(self.__song)
        return str(self.__song)
