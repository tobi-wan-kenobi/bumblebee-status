"""get volume level or control it

Parameters:
    * amixer.device: Device to use (default is Master,0)
    * amixer.percent_change: How much to change volume by when scrolling on the module (default is 4%)

contributed by `zetxx <https://github.com/zetxx>`_ - many thanks!
"""
import re

import core.module
import core.widget
import core.input

import util.cli
import util.format

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.volume))

        self._level = "n/a"
        self._muted = True
        self._device = self.parameter("device", "Master,0")
        self._change = util.format.asint(
            self.parameter("percent_change", "4%").strip("%"), 0, 100
        )

        events = [
            {
                "type": "mute",
                "action": self.toggle,
                "button": core.input.LEFT_MOUSE,
            },
            {
                "type": "volume",
                "action": self.increase_volume,
                "button": core.input.WHEEL_UP,
            },
            {
                "type": "volume",
                "action": self.decrease_volume,
                "button": core.input.WHEEL_DOWN,
            },
        ]

        for event in events:
            core.input.register(self, button=event["button"], cmd=event["action"])

    def toggle(self, event):
        self.set_parameter("toggle")

    def increase_volume(self, event):
        self.set_parameter("{}%+".format(self._change))

    def decrease_volume(self, event):
        self.set_parameter("{}%-".format(self._change))

    def set_parameter(self, parameter):
        util.cli.execute("amixer -q set {} {}".format(self._device, parameter))

    def volume(self, widget):
        if self._level == "n/a":
            return self._level
        m = re.search(r"([\d]+)\%", self._level)
        self._muted = True
        if m:
            if m.group(1) != "0" and "[on]" in self._level:
                self._muted = False
            return "{}%".format(m.group(1))
        else:
            return "0%"

    def update(self):
        try:
            self._level = util.cli.execute(
                "amixer get {}".format(self._device)
            )
        except Exception as e:
            self._level = "n/a"

    def state(self, widget):
        if self._muted:
            return ["warning", "muted"]
        return ["unmuted"]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
