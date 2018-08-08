# pylint: disable=C0111,R0903

"""Displays the current song being played in DeaDBeeF and
provides some media control bindings.

Left click toggles pause, scroll up skips the current song,
scroll down returns to the previous song.

Requires the following library:
    * subprocess

Parameters:
    * deadbeef.format: Format string (defaults to "{artist} - {title}")
                       Available values are: {artist}, {title}, {album}, {length},
                                             {trackno}, {year}, {comment},
                                             {copyright}, {time}
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

try:
    import subprocess
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.deadbeef)
                                     )
        self._song = ""
        self._format = self.parameter("format", "{artist} - {title}")

        self.now_playing = ["deadbeef","--nowplaying","%a;%t;%b;%l;%n;%y;%c;%r;%e"]
        cmd = "deadbeef "
        
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_DOWN,
            cmd=cmd + "--prev")
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_UP,
            cmd=cmd + "--next")
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=cmd + "--play-pause")

    def deadbeef(self, widget):
        return str(self._song)

    def hidden(self):
        return str(self._song) == ""

    def update(self, widgets):
        try:
            deadbeef = subprocess.Popen(self.now_playing,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            data = deadbeef.communicate()[0]
            if data == "nothing":
                self._song = ""
            else:
                data = data.split(";")
                self._song = self._format.format(artist=data[0],
                                                 title=data[1],
                                                 album=data[2],
                                                 length=data[3],
                                                 trackno=data[4],
                                                 year=data[5],
                                                 comment=data[6],
                                                 copyright=data[7],
                                                 time=data[8])
        except Exception:
            self._song = ""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
