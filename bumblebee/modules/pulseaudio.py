# pylint: disable=C0111,R0903

"""Displays volume and mute status and controls for PulseAudio devices. Use wheel up and down to change volume, left click mutes, right click opens pavucontrol.

Aliases: pasink (use this to control output instead of input), pasource

Parameters:
    * pulseaudio.autostart: If set to "true" (default is "false"), automatically starts the pulseaudio daemon if it is not running
    * pulseaudio.percent_change: How much to change volume by when scrolling on the module (default is 2%)
    * pulseaudio.limit: Upper limit for setting the volume (default is 0%, which means "no limit")
                        Note: If the left and right channels have different volumes, the limit might not be reached exactly.
    * pulseaudio.showbars: 1 for showing volume bars, requires --markup=pango;
                           0 for not showing volume bars (default)

Requires the following executable:
    * pulseaudio
    * pactl
    * pavucontrol
"""

import re

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

def autostart_daemon():
    try:
        bumblebee.util.execute("pulseaudio --check")
    except Exception:
        try:
            bumblebee.util.execute("pulseaudio --start")
        except:
            pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.volume)
        )
        if bumblebee.util.asbool(self.parameter("autostart", False)):
            autostart_daemon()

        self._change = 2
        self._change = int(self.parameter("percent_change", "2%").strip("%"))
        if self._change < 0 or self._change > 100:
            self._change = 2

        self._limit = 0
        self._limit = int(self.parameter("limit", "0%").strip("%s"))
        if self._limit < 0:
            self._limit = 0

        self._left = 0
        self._right = 0
        self._mono = 0
        self._mute = False
        self._failed = False
        self._channel = "sink" if self.name == "pasink" else "source"
        self._showbars = bumblebee.util.asbool(self.parameter("showbars", 0))

        self._patterns = [
            {"expr": "Name:", "callback": (lambda line: False)},
            {"expr": "Mute:", "callback": (lambda line: self.mute(False if " no" in line.lower() else True))},
            {"expr": "Volume:", "callback": self.getvolume},
        ]

        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd="pavucontrol")

        events = [
            {"type": "mute", "action": self.toggle, "button": bumblebee.input.LEFT_MOUSE},
            {"type": "volume", "action": self.increase_volume, "button": bumblebee.input.WHEEL_UP},
            {"type": "volume", "action": self.decrease_volume, "button": bumblebee.input.WHEEL_DOWN},
        ]

        for event in events:
            engine.input.register_callback(self, button=event["button"], cmd=event["action"])

    def set_volume(self, amount):
        bumblebee.util.execute("pactl set-{}-{} @DEFAULT_{}@ {}".format(
            self._channel, "volume", self._channel.upper(), amount))

    def increase_volume(self, event):
        if self._limit > 0: # we need to check the limit
            left = int(self._left)
            right = int(self._right)
            if left + self._change >= self._limit or right + self._change >= self._limit:
                if left == right:
                    # easy case, just set to limit
                    self.set_volume("{}%".format(self._limit))
                    return
                else:
                    # don't adjust anymore, since i don't know how to update only one channel
                    return

        self.set_volume("+{}%".format(self._change))

    def decrease_volume(self, event):
        self.set_volume("-{}%".format(self._change))

    def toggle(self, event):
        bumblebee.util.execute("pactl set-{}-{} @DEFAULT_{}@ {}".format(
            self._channel, "mute", self._channel.upper(), "toggle"))

    def mute(self, value):
        self._mute = value

    def getvolume(self, line):
        if "mono" in line:
            m = re.search(r'mono:.*\s*\/\s*(\d+)%', line)
            if m:
                self._mono = m.group(1)
        else:
            m = re.search(r'left:.*\s*\/\s*(\d+)%.*right:.*\s*\/\s*(\d+)%', line)
            if m:
                self._left = m.group(1)
                self._right = m.group(2)
        return True

    def _default_device(self):
        output = bumblebee.util.execute("pactl info")
        pattern = "Default {}: ".format("Sink" if self.name == "pasink" else "Source")
        for line in output.split("\n"):
            if line.startswith(pattern):
                return line.replace(pattern, "")
        return "n/a"

    def volume(self, widget):
        if self._failed == True:
            return "n/a"
        if int(self._mono) > 0:
            vol = "{}%".format(self._mono)
            if self._showbars:
                vol = "{} {}".format(
                    vol, bumblebee.output.hbar(float(self._mono)))
            return vol
        elif self._left == self._right:
            vol = "{}%".format(self._left)
            if self._showbars:
                vol = "{} {}".format(
                    vol, bumblebee.output.hbar(float(self._left)))
            return vol
        else:
            vol = "{}%/{}%".format(self._left, self._right)
            if self._showbars:
                vol = "{} {}{}".format(
                    vol,
                    bumblebee.output.hbar(float(self._left)),
                    bumblebee.output.hbar(float(self._right)))
            return vol

    def update(self, widgets):
        try:
            self._failed = False
            channel = "sinks" if self.name == "pasink" else "sources"
            device = self._default_device()

            result = bumblebee.util.execute("pactl list {}".format(channel))
            found = False

            for line in result.split("\n"):
                if "Name: {}".format(device) in line:
                    found = True
                    continue
                if found is False:
                    continue
                for pattern in self._patterns:
                    if not pattern["expr"] in line:
                        continue
                    if pattern["callback"](line) is False and found == True:
                        return
        except Exception:
            self._failed = True
            if bumblebee.util.asbool(self.parameter("autostart", False)):
                autostart_daemon()
                self.update(widgets)

    def state(self, widget):
        if self._mute:
            return ["warning", "muted"]
        if int(self._left) > int(100):
            return ["critical", "unmuted"]
        return ["unmuted"]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
