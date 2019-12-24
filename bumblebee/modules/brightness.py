# pylint: disable=C0111,R0903

"""Displays the brightness of a display

Parameters:
    * brightness.step: The amount of increase/decrease on scroll in % (defaults to 2)
    * brightness.device_path: The device path (defaults to /sys/class/backlight/intel_backlight), can contain wildcards (in this case, the first matching path will be used)

"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

import glob

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.brightness))
        self._brightness = 0

        self._device_path = self.find_device(self.parameter("device_path", "/sys/class/backlight/intel_backlight"))
        step = self.parameter("step", 2)

        if bumblebee.util.which("light"):
            self.register_cmd(engine, "light -A {}%".format(step),
                              "light -U {}%".format(step))
        elif bumblebee.util.which("brightnessctl"):
            self.register_cmd(engine, "brightnessctl s {}%+".format(step),
                              "brightnessctl s {}%-".format(step))
        else:
            self.register_cmd(engine, "xbacklight +{}%".format(step),
                              "xbacklight -{}%".format(step))

    def find_device(self, device_path):
        res = glob.glob(device_path)
        if len(res) == 0:
            return device_path
        return res[0]

    def register_cmd(self, engine, upCmd, downCmd):
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_UP, cmd=upCmd)
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_DOWN, cmd=downCmd)

    def brightness(self, widget):
        if isinstance(self._brightness, float):
            return "{:3.0f}%".format(self._brightness).strip()
        else:
            return "n/a"

    def update(self, widgets):
        try:
            with open("{}/brightness".format(self._device_path)) as f:
                backlight = int(f.readline())
            with open("{}/max_brightness".format(self._device_path)) as f:
                max_brightness = int(f.readline())
                self._brightness = float(backlight * 100 / max_brightness)
        except:
            return "Error"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
