# pylint: disable=C0111,R0903

"""Displays the current song being played

Requires the following library:
    * python-dbus

Parameters:
    * deezer.format:   Format string (defaults to '{artist} - {title}')
      Available values are: {album}, {title}, {artist}, {trackNumber}, {playbackStatus}
    * deezer.previous: Change binding for previous song (default is left click)
    * deezer.next:     Change binding for next song (default is right click)
    * deezer.pause:    Change binding for toggling pause (default is middle click)

    Available options for deezer.previous, deezer.next and deezer.pause are:
        LEFT_CLICK, RIGHT_CLICK, MIDDLE_CLICK, SCROLL_UP, SCROLL_DOWN

contributed by `wwmoraes <https://github.com/wwmoraes>`_ - many thanks!
"""

import dbus

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.deezer))

        buttons = {
            "LEFT_CLICK": core.input.LEFT_MOUSE,
            "RIGHT_CLICK": core.input.RIGHT_MOUSE,
            "MIDDLE_CLICK": core.input.MIDDLE_MOUSE,
            "SCROLL_UP": core.input.WHEEL_UP,
            "SCROLL_DOWN": core.input.WHEEL_DOWN,
        }

        self._song = ""
        self._format = self.parameter("format", "{artist} - {title}")
        prev_button = self.parameter("previous", "LEFT_CLICK")
        next_button = self.parameter("next", "RIGHT_CLICK")
        pause_button = self.parameter("pause", "MIDDLE_CLICK")

        cmd = "dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.deezer \
                /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."
        core.input.register(self, button=buttons[prev_button], cmd=cmd + "Previous")
        core.input.register(self, button=buttons[next_button], cmd=cmd + "Next")
        core.input.register(self, button=buttons[pause_button], cmd=cmd + "PlayPause")

    def deezer(self, widget):
        return str(self._song)

    def hidden(self):
        return str(self._song) == ""

    def update(self):
        try:
            bus = dbus.SessionBus()
            deezer = bus.get_object(
                "org.mpris.MediaPlayer2.deezer", "/org/mpris/MediaPlayer2"
            )
            deezer_iface = dbus.Interface(deezer, "org.freedesktop.DBus.Properties")
            props = deezer_iface.Get("org.mpris.MediaPlayer2.Player", "Metadata")
            playback_status = str(
                deezer_iface.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
            )
            self._song = self._format.format(
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
            self._song = ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
