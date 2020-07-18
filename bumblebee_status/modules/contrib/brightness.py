# pylint: disable=C0111,R0903

"""Displays the brightness of a display

The following executables can be used if `use_acpi` is not enabled:
    * brightnessctl
    * light
    * xbacklight

Parameters:
    * brightness.step: The amount of increase/decrease on scroll in % (defaults to 2)
    * brightness.device_path: The device path (defaults to /sys/class/backlight/intel_backlight), can contain wildcards (in this case, the first matching path will be used); This is only used when brightness.use_acpi is set to true
    * brightness.use_acpi: If set to true, read brightness directly from the sys ACPI interface, using the device specified in brightness.device_path (defaults to false)

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
        self.__device_path = self.find_device(self.parameter("device_path", "/sys/class/backlight/intel_backlight"))

        if util.format.asbool(self.parameter("use_acpi", False)):
            self.__readcmd = self.__acpi
            # TODO: add setting
        elif shutil.which("light"):
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

    def find_device(self, device_path):
        res = glob.glob(device_path)
        if len(res) == 0:
            return device_path
        return res[0]

    def register_cmd(self, up_cmd, down_cmd):
        core.input.register(self, button=core.input.WHEEL_UP, cmd=up_cmd)
        core.input.register(self, button=core.input.WHEEL_DOWN, cmd=down_cmd)

    def brightness(self, widget):
        return self.__brightness

    def __acpi(self):
        try:
            backlight = 1
            max_brightness = 1
            with open("{}/brightness".format(self.__device_path)) as f:
                backlight = int(f.readline())
            with open("{}/max_brightness".format(self.__device_path)) as f:
                max_brightness = int(f.readline())
                return float(backlight*100)/max_brightness
        except:
            return "unable to read brightness from {}".format(self.__device_path)

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
            tmp = self.__readcmd()
            if isinstance(tmp, str):
                self.__brightness = tmp
            else:
                self.__brightness = "{:3.0f}%".format(float(tmp))
        except:
            self.__brightness = "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
