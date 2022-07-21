"""Displays temperature of blugon and Controls it.

Use wheel up and down to change temperature, middle click to toggle and right click to reset temperature.

Default Values:
    * Minimum temperature: 1000 (red)
    * Maximum temperature: 20000 (blue)
    * Default temperature: 6600

Requires the following executable:
    * blugon

Parameters:
    * blugon.step: The amount of increase/decrease on scroll (default: 200)

contributed by `DTan13 <https://github.com/DTan13>`
"""

import core.module
import core.widget

import util.cli
import util.format

import os


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        self.__state = True
        self.__default = 6600
        self.__step = (
            util.format.asint(self.parameter("step")) if self.parameter("step") else 200
        )
        self.__max, self.__min = 20000, 1000

        file = open(os.path.expanduser("~/.config/blugon/current"))
        self.__current = int(float(file.read()))

        events = [
            {
                "type": "toggle",
                "action": self.toggle,
                "button": core.input.MIDDLE_MOUSE,
            },
            {
                "type": "blue",
                "action": self.blue,
                "button": core.input.WHEEL_UP,
            },
            {
                "type": "red",
                "action": self.red,
                "button": core.input.WHEEL_DOWN,
            },
            {
                "type": "reset",
                "action": self.reset,
                "button": core.input.RIGHT_MOUSE,
            },
        ]

        for event in events:
            core.input.register(self, button=event["button"], cmd=event["action"])

    def set_temp(self):
        temp = self.__current if self.__state else self.__default
        util.cli.execute("blugon --setcurrent={}".format(temp))

    def full_text(self, widget):
        return self.__current if self.__state else self.__default

    def state(self, widget):
        if not self.__state:
            return ["critical"]

    def toggle(self, event):
        self.__state = not self.__state
        self.set_temp()

    def reset(self, event):
        self.__current = 6600
        self.set_temp()

    def blue(self, event):
        if self.__state and (self.__current < self.__max):
            self.__current += self.__step
        self.set_temp()

    def red(self, event):
        if self.__state and (self.__current > self.__min):
            self.__current -= self.__step
        self.set_temp()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
