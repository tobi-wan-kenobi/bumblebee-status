"""get volume level or control it

Requires the following executable:
    * pamixer

Parameters:
    * pamixer.percent_change: How much to change volume by when scrolling on the module (default is 4%)

heavily based on amixer module
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

        self.__level = "volume 0%"
        self.__muted = True
        self.__change = util.format.asint(
            self.parameter("percent_change", "4%").strip("%"), 0, 200
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
        self.set_parameter("--toggle-mute")

    def increase_volume(self, event):
        self.set_parameter("--increase {}".format(self.__change))

    def decrease_volume(self, event):
        self.set_parameter("--decrease {}".format(self.__change))

    def set_parameter(self, parameter):
        util.cli.execute("pamixer {}".format(parameter))

    def volume(self, widget):
        if self.__level == "volume 0%":
            self.__muted = True
            return self.__level
        m = re.search(r"([\d]+)\%", self.__level)
        if m:
            if m.group(1) != "0%" in self.__level:
                self.__muted = False
            return "volume {}%".format(m.group(1))
        else:
            return "volume 0%"

    def update(self):
        try:
            volume = util.cli.execute("pamixer --get-volume-human".format())
            self.__level = volume
            self.__muted = False
        except Exception as e:
            self.__level = "volume 0%"

    def state(self, widget):
        if self.__muted:
            return ["warning", "muted"]
        return ["unmuted"]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
