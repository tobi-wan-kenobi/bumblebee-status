import sys
import dbus

import core.module
import core.widget
import core.input
import core.decorators
"""Displays the current song being played

Requires the following library:
    * python-dbus

Parameters:
    * spotify-buttons.format:   Format string (defaults to '{artist} - {title}')
      Available values are: {album}, {title}, {artist}, {trackNumber}, {playbackStatus}
    * spotify-buttons.layout:
"""

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.spotify))

        self.__layout = self.parameter("layout", "spotify-buttons.prev spotify-buttons.pause spotify-buttons.next")

        self.__song = ""
        self.__format = self.parameter("format", "{artist} - {title}")
        prev_button = self.parameter("previous", "LEFT_CLICK")
        next_button = self.parameter("next", "RIGHT_CLICK")
        pause_button = self.parameter("pause", "MIDDLE_CLICK")

        cmd = "dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.spotify \
                /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."

        widget_map = {}
        for widget_name in self.__layout.split():
            widget = self.add_widget(name = widget_name)
            if widget_name == "spotify-buttons.prev":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": cmd + "Previous",
                }
            elif widget_name == "spotify-buttons.pause":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": cmd + "PlayPause",
                }
            elif widget_name == "spotify-buttons.next":
                widget_map[widget] = {
                    "button": core.input.LEFT_MOUSE,
                    "cmd": cmd + "Next",
                }
        for widget, callback_options in widget_map.items():
            core.input.register(widget, **callback_options)

    @core.decorators.scrollable
    def spotify(self, widget):
        return self.string_song

    def hidden(self):
        return self.string_song == ""

    def update(self):
        try:
            bus = dbus.SessionBus()
            spotify = bus.get_object(
                "org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2"
            )
            spotify_iface = dbus.Interface(spotify, "org.freedesktop.DBus.Properties")
            props = spotify_iface.Get("org.mpris.MediaPlayer2.Player", "Metadata")
            playback_status = str(
                spotify_iface.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
            )
            self.__song = self.__format.format(
                album=str(props.get("xesam:album")),
                title=str(props.get("xesam:title")),
                artist=",".join(props.get("xesam:artist")),
                trackNumber=str(props.get("xesam:trackNumber")),
                playbackStatus="\u25B6"
                if playback_status == "Playing"
                else "\u258D\u258D"
                if playback_status == "Paused"
                else "",
            )

        except Exception:
            self.__song = ""

    @property
    def string_song(self):
        if sys.version_info.major < 3:
            return unicode(self.__song)
        return str(self.__song)
