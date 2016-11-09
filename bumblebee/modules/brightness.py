import bumblebee.module

def description():
    return "Displays brightness percentage"

def parameters():
    return [
        "brightness.step: Steps (in percent) to increase/decrease brightness on scroll (defaults to 2)",
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._brightness = 0
        self._max = 0
        self._percent = 0

        step = self._config.parameter("step", 2)

        output.add_callback(module=self.instance(), button=4, cmd="xbacklight +{}%".format(step))
        output.add_callback(module=self.instance(), button=5, cmd="xbacklight -{}%".format(step))

    def widgets(self):
        with open("/sys/class/backlight/intel_backlight/brightness") as f:
            self._brightness = int(f.read())
        with open("/sys/class/backlight/intel_backlight/max_brightness") as f:
            self._max = int(f.read())
        self._brightness = self._brightness if self._brightness < self._max else self._max
        self._percent = int(round(self._brightness * 100 / self._max))

        return bumblebee.output.Widget(self, "{:02d}%".format(self._percent))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
