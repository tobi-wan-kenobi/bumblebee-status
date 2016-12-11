# pylint: disable=C0111,R0903

"""Displays volume and mute status of PulseAudio devices.

Aliases: pasink, pasource
"""

import re

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

ALIASES = [ "pasink", "pasource" ]

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.volume)
        )

        self._left = 0
        self._right = 0
        self._mono = 0
        self._mute = False
        channel = "sink" if self.name == "pasink" else "source"

        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd="pavucontrol")
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="pactl set-{}-mute @DEFAULT_{}@ toggle".format(channel, channel.upper()))
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_UP,
            cmd="pactl set-{}-volume @DEFAULT_{}@ +2%".format(channel, channel.upper()))
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_DOWN,
            cmd="pactl set-{}-volume @DEFAULT_{}@ -2%".format(channel, channel.upper()))

    def _default_device(self):
        output = bumblebee.util.execute("pactl info")
        pattern = "Default Sink: " if self.name == "pasink" else "Default Source: "
        for line in output.split("\n"):
            if line.startswith(pattern):
                return line.replace(pattern, "")
        return "n/a"

    def volume(self, widget):
        if int(self._mono) > 0:
            return "{}%".format(self._mono)
        elif self._left == self._right:
            return "{}%".format(self._left)
        else:
            return "{}%/{}%".format(self._left, self._right)
        return "n/a"

    def update(self, widgets):
        channel = "sinks" if self.name == "pasink" else "sources"
        device = self._default_device()

        result = bumblebee.util.execute("pactl list {}".format(channel))
        found = False
        for line in result.split("\n"):
            if "Name:" in line and found == True:
                break
            if device in line:
                found = True

            if "Mute:" in line and found == True:
                self._mute = False if " no" in line.lower() else True

            if "Volume:" in line and found == True:
                m = None
                if "mono" in line:
                    m = re.search(r'mono:.*\s*\/\s*(\d+)%', line)
                else:
                    m = re.search(r'left:.*\s*\/\s*(\d+)%.*right:.*\s*\/\s*(\d+)%', line)
                if not m: continue

                if "mono" in line:
                    self._mono = m.group(1)
                else:
                    self._left = m.group(1)
                    self._right = m.group(2)

    def state(self, widget):
        if self._mute:
            return [ "warning", "muted" ]
        return [ "unmuted" ]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
