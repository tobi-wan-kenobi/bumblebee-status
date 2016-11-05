import datetime
import bumblebee.module

def usage():
    return "battery or battery::<battery ID, defaults to BAT0>"

def notes():
    return "Reads /sys/class/power_supply/<ID>/[capacity|status]. Warning is at 20% remaining charge, Critical at 10%."

def description():
    return "Displays battery status, percentage and whether it's charging or discharging."

class Module(bumblebee.module.Module):
    def __init__(self, output, config):
        super(Module, self).__init__(output, config)
        self._battery = config.parameter("battery.device", "BAT0")
        self._capacity = 0
        self._status = "Unknown"

    def widgets(self):
        with open("/sys/class/power_supply/{}/capacity".format(self._battery)) as f:
            self._capacity = int(f.read())
        self._capacity = self._capacity if self._capacity < 100 else 100

        return bumblebee.output.Widget(self,"{:02d}%".format(self._capacity))

    def warning(self, widget):
        return self._capacity < self._config.parameter("battery.warning", 20)

    def critical(self, widget):
        return self._capacity < self._config.parameter("battery.critical", 10)

    def state(self, widget):
        with open("/sys/class/power_supply/{}/status".format(self._battery)) as f:
            self._status = f.read().strip()

        if self._status == "Discharging":
            status = "discharging-{}".format(min([ 10, 25, 50, 80, 100] , key=lambda i:abs(i-self._capacity)))
            return status
        else:
            if self._capacity > 95:
                return "charged"
            return "charging"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
