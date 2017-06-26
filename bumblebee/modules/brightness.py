# pylint: disable=C0111,R0903

"""Displays the brightness of a display

Parameters:
    * brightness.step: The amount of increase/decrease on scroll in % (defaults to 2)
    * brightness.device_path: The device path (defaults to /sys/class/backlight/intel_backlight)

"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.brightness)
        )
        self._brightness = 0

        self._device_path = self.parameter("device_path", "/sys/class/backlight/intel_backlight")
        step = self.parameter("step", 2)

        engine.input.register_callback(self, button=bumblebee.input.WHEEL_UP,
            cmd="xbacklight +{}%".format(step))
        engine.input.register_callback(self, button=bumblebee.input.WHEEL_DOWN,
            cmd="xbacklight -{}%".format(step))

    def brightness(self, widget):
        if isinstance(self._brightness, float):
            return "{:03.0f}%".format(self._brightness)
        else:
            return "n/a"

    def update(self, widgets):
        try:
            with open("{}/brightness".format(self._device_path)) as f:
                backlight = int(f.readline())
            with open("{}/max_brightness".format(self._device_path)) as f:
                max_brightness = int(f.readline())
                self._brightness=float(backlight*100/max_brightness)
        except:
            return "Error"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
