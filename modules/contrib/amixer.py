"""get volume level

Parameters:
    * amixer.device: Device to use, defaults to "Master,0"
"""
import re

import core.module
import core.widget

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.volume))

        self.__level = "n/a"
        self.__muted = True
        device = self.parameter("device", "Master,0")
        self._cmdString = "amixer get {}".format(device)

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
                "amixer get {}".format(self.parameter("device", "Master,0"))
            )
        except Exception as e:
            self.__level = "n/a"

    def state(self, widget):
        if self.__muted:
            return ["warning", "muted"]
        return ["unmuted"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
