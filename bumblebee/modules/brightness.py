import bumblebee.module

def description():
    return "Displays brightness percentage"

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._brightness = 0
        self._max = 0
        self._percent = 0

    def widgets(self):
        with open("/sys/class/backlight/intel_backlight/brightness") as f:
            self._brightness = int(f.read())
        with open("/sys/class/backlight/intel_backlight/max_brightness") as f:
            self._max = int(f.read())
        self._brightness = self._brightness if self._brightness < self._max else self._max
        self._percent = round(self._brightness * 100 / self._max)

        return bumblebee.output.Widget(self, "{:02d}%".format(self._percent))

