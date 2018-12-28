# pylint: disable=C0111,R0903

"""Displays the current song being played in DeaDBeeF and
provides some media control bindings.
Left click toggles pause, scroll up skips the current song,
scroll down returns to the previous song.
Requires the following library:
    * subprocess
Parameters:
    * deadbeef.format:   Format string (defaults to "{artist} - {title}")
                         Available values are: {artist}, {title}, {album}, {length},
                                               {trackno}, {year}, {comment},
                                               {copyright}, {time}
    * deadbeef.previous: Change binding for previous song (default is left click)
    * deadbeef.next:     Change binding for next song (default is right click)
    * deadbeef.pause:    Change binding for toggling pause (default is middle click)
    Available options for deadbeef.previous, deadbeef.next and deadbeef.pause are:
        LEFT_CLICK, RIGHT_CLICK, MIDDLE_CLICK, SCROLL_UP, SCROLL_DOWN
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

from bumblebee.output import scrollable

try:
    import subprocess
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.deadbeef)
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

        self.now_playing = ["deadbeef","--nowplaying","%a;%t;%b;%l;%n;%y;%c;%r;%e"]
        cmd = "deadbeef "
        
        engine.input.register_callback(self, button=buttons[prev_button],
            cmd=cmd + "--prev")
        engine.input.register_callback(self, button=buttons[next_button],
            cmd=cmd + "--next")
        engine.input.register_callback(self, button=buttons[pause_button],
            cmd=cmd + "--play-pause")

    @scrollable
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
