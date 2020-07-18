"""get volume level or control it

Requires the following executable:
    * amixer

Parameters:
    * amixer.device: Device to use (default is Master,0)
    * amixer.percent_change: How much to change volume by when scrolling on the module (default is 4%)

contributed by `zetxx <https://github.com/zetxx>`_ - many thanks!

input handling contributed by `ardadem <https://github.com/ardadem>`_ - many thanks!
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

        self.__level = "n/a"
        self.__muted = True
        self.__device = self.parameter("device", "Master,0")
        self.__change = util.format.asint(
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
        self.set_parameter("{}%+".format(self.__change))

    def decrease_volume(self, event):
        self.set_parameter("{}%-".format(self.__change))

    def set_parameter(self, parameter):
        util.cli.execute("amixer -q set {} {}".format(self.__device, parameter))

    def volume(self, widget):
        if self.__level == "n/a":
            return self.__level
        m = re.search(r"([\d]+)\%", self.__level)
        self.__muted = True
        if m:
            if m.group(1) != "0" and "[on]" in self.__level:
                self.__muted = False
            return "{}%".format(m.group(1))
        else:
            return "0%"

    def update(self):
        try:
            self.__level = util.cli.execute(
                "amixer get {}".format(self.__device)
            )
        except Exception as e:
            self.__level = "n/a"

    def state(self, widget):
        if self.__muted:
            return ["warning", "muted"]
        return ["unmuted"]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
