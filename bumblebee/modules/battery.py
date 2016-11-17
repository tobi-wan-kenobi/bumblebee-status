import datetime
import bumblebee.module
import os.path

def description():
    return "Displays battery status, percentage and whether it's charging or discharging."

def parameters():
    return [ "battery.device: The device to read from (defaults to BAT0)" ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._battery = config.parameter("device", "BAT0")
        self._capacity = 100
        self._status = "Unknown"

    def widgets(self):
        self._AC = False;
        self._path = "/sys/class/power_supply/{}".format(self._battery)
        if not os.path.exists(self._path):
            self._AC = True;
            return bumblebee.output.Widget(self,"AC")

        with open(self._path + "/capacity") as f:
            self._capacity = int(f.read())
        self._capacity = self._capacity if self._capacity < 100 else 100

        return bumblebee.output.Widget(self,"{:02d}%".format(self._capacity))

    def warning(self, widget):
        return self._capacity < self._config.parameter("warning", 20)

    def critical(self, widget):
        return self._capacity < self._config.parameter("critical", 10)

    def state(self, widget):
        if self._AC:
            return "AC"

        with open(self._path + "/status") as f:
            self._status = f.read().strip()

        if self._status == "Discharging":
            status = "discharging-{}".format(min([ 10, 25, 50, 80, 100] , key=lambda i:abs(i-self._capacity)))
            return status
        else:
            if self._capacity > 95:
                return "charged"
            return "charging"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
