# pylint: disable=C0111,R0903

"""Displays the current song being played
Requires the following library:
    * python-dbus
Parameters:
    * spotify.format:   Format string (defaults to "{artist} - {title}")
                        Available values are: {album}, {title}, {artist}, {trackNumber}, {playbackStatus}
    * spotify.previous: Change binding for previous song (default is left click)
    * spotify.next:     Change binding for next song (default is right click)
    * spotify.pause:    Change binding for toggling pause (default is middle click)
    Available options for spotify.previous, spotify.next and spotify.pause are:
        LEFT_CLICK, RIGHT_CLICK, MIDDLE_CLICK, SCROLL_UP, SCROLL_DOWN
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

from bumblebee.output import scrollable

try:
    import dbus
except ImportError:
    pass


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.spotify)
                                     )
        buttons = {"LEFT_CLICK":bumblebee.input.LEFT_MOUSE,
                   "RIGHT_CLICK":bumblebee.input.RIGHT_MOUSE,
                   "MIDDLE_CLICK":bumblebee.input.MIDDLE_MOUSE,
                   "SCROLL_UP":bumblebee.input.WHEEL_UP,
                   "SCROLL_DOWN":bumblebee.input.WHEEL_DOWN,
                   }
        
        self._song = ""
        self._format = self.parameter("format", "{artist} - {title}")
        prev_button = self.parameter("previous", "LEFT_CLICK")
        next_button = self.parameter("next", "RIGHT_CLICK")
        pause_button = self.parameter("pause", "MIDDLE_CLICK")

        cmd = "dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.spotify \
                /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."
        engine.input.register_callback(self, button=buttons[prev_button],
            cmd=cmd + "Previous")
        engine.input.register_callback(self, button=buttons[next_button],
            cmd=cmd + "Next")
        engine.input.register_callback(self, button=buttons[pause_button],
            cmd=cmd + "PlayPause")

##    @scrollable
    def spotify(self, widget):
        return str(self._song)

    def hidden(self):
        return str(self._song) == ""

    def update(self, widgets):
        try:
            bus = dbus.SessionBus()
            spotify = bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
            spotify_iface = dbus.Interface(spotify, 'org.freedesktop.DBus.Properties')
            props = spotify_iface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            playback_status = str(spotify_iface.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus'))
            self._song = self._format.format(album=str(props.get('xesam:album')),
                                             title=str(props.get('xesam:title')),
                                             artist=','.join(props.get('xesam:artist')),
                                             trackNumber=str(props.get('xesam:trackNumber')),
                                             playbackStatus=u"\u25B6" if playback_status=="Playing" else u"\u258D\u258D" if playback_status=="Paused" else "",)
        except Exception:
            self._song = ""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
