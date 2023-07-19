"""get volume level or control it

Requires the following executable:
    * wpctl

Parameters:
    * wpctl.percent_change: How much to change volume by when scrolling on the module (default is 4%)

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

        self.__level = "N/A"
        self.__muted = True
        self.__change = (
            util.format.asint(self.parameter("percent_change", "4%").strip("%"), 0, 200)
            / 100.0
        )  # divide by 100 because wpctl represents 100% volume as 1.00, 50% as 0.50, etc

        self.__id = self.parameter("sink_id") or "@DEFAULT_AUDIO_SINK@"

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
        util.cli.execute("wpctl set-mute {} toggle".format(self.__id))

    def increase_volume(self, event):
        util.cli.execute(
            "wpctl set-volume --limit 1.0 {} {}+".format(self.__id, self.__change)
        )

    def decrease_volume(self, event):
        util.cli.execute(
            "wpctl set-volume --limit 1.0 {} {}-".format(self.__id, self.__change)
        )

    def volume(self, widget):
        if self.__level == "N/A":
            return self.__level
        return "{}%".format(int(float(self.__level) * 100))

    def update(self):
        try:
            # `wpctl get-volume` will return a string like "Volume: n.nn" or "Volume: n.nn [MUTED]"
            volume = util.cli.execute("wpctl get-volume {}".format(self.__id))
            v = re.search("\d\.\d+", volume)
            m = re.search("MUTED", volume)
            self.__level = v.group()
            self.__muted = True if m else False
        except Exception:
            self.__level = "N/A"

    def state(self, widget):
        if self.__muted:
            return ["warning", "muted"]
        return ["unmuted"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
