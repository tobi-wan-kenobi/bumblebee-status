# pylint: disable=C0111,R0903

"""Displays the current song being played

Requires the following library:
    * python-dbus

Parameters:
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

try:
    import dbus
except ImportError:
    pass


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.spotify)
                                     )
        self._song = ""

        cmd="dbus-send --session --type=method_call --dest=org.mpris.MediaPlayer2.spotify \
                /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=cmd + "Previous")
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd=cmd + "Next")
        engine.input.register_callback(self, button=bumblebee.input.MIDDLE_MOUSE,
            cmd=cmd + "PlayPause")

    def spotify(self, widget):
        return str(self._song)

    def update(self, widgets):
        try:
            bus = dbus.SessionBus()
            spotify = bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
            spotify_iface = dbus.Interface(spotify, 'org.freedesktop.DBus.Properties')
            props = spotify_iface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            self._song = (str(props['xesam:artist'][0]) + " - " + str(props['xesam:title']))
        except Exception:
            self._song = ""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
