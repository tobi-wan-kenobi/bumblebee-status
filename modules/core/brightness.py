# pylint: disable=C0111,R0903

"""Displays the brightness of a display

Parameters:
    * brightness.step: The amount of increase/decrease on scroll in % (defaults to 2)

contributed by `TheEdgeOfRage <https://github.com/TheEdgeOfRage>`_ - many thanks!
"""

import glob
import shutil

import core.module
import core.widget
import core.input
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(seconds=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.brightness))

        self.__brightness = "n/a"
        self.__readcmd = None
        step = self.parameter("step", 2)

        if shutil.which("light"):
            self.__readcmd = self.__light
            self.register_cmd("light -A {}%".format(step), "light -U {}%".format(step))
        elif shutil.which("brightnessctl"):
            self.__readcmd = self.__brightnessctl
            self.register_cmd(
                "brightnessctl s {}%+".format(step), "brightnessctl s {}%-".format(step)
            )
        else:
            self.__readcmd = self.__xbacklight
            self.register_cmd(
                "xbacklight +{}%".format(step), "xbacklight -{}%".format(step)
            )

    def register_cmd(self, up_cmd, down_cmd):
        core.input.register(self, button=core.input.WHEEL_UP, cmd=up_cmd)
        core.input.register(self, button=core.input.WHEEL_DOWN, cmd=down_cmd)

    def brightness(self, widget):
        return self.__brightness

    def __light(self):
        return util.cli.execute("light").strip()

    def __brightnessctl(self):
        m = util.cli.execute("brightnessctl m").strip()
        g = util.cli.execute("brightnessctl g").strip()
        return float(g) / float(m) * 100.0

    def __xbacklight(self):
        return util.cli.execute("xbacklight -get").strip()

    def update(self):
        try:
            self.__brightness = "{:3.0f}%".format(float(self.__readcmd()))
        except:
            self.__brightness = "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
