import datetime
import bumblebee.module

def usage():
    return "battery or battery::<battery ID, defaults to BAT0>"

def notes():
    return "Reads /sys/class/power_supply/<ID>/[capacity|status]. Warning is at 20% remaining charge, Critical at 10%."

def description():
    return "Displays battery status, percentage and whether it's charging or discharging."

class Module(bumblebee.module.Module):
    def __init__(self, output, args):
        super(Module, self).__init__(args)
        self._battery = "BAT0" if not args else args[0]
        self._capacity = 0
        self._status = "Unknown"

    def data(self):
        with open("/sys/class/power_supply/{}/capacity".format(self._battery)) as f:
            self._capacity = int(f.read())
        self._capacity = self._capacity if self._capacity < 100 else 100

        return "{:02d}%".format(self._capacity)

    def warning(self):
        return self._capacity < 20

    def critical(self):
        return self._capacity < 10

    def state(self):
        with open("/sys/class/power_supply/{}/status".format(self._battery)) as f:
            self._status = f.read().strip()
        if self._status == "Discharging":
            if self._capacity < 10:
                return "discharging_critical"
            if self._capacity < 25:
                return "discharging_low"
            if self._capacity < 50:
                return "discharging_medium"
            if self._capacity < 75:
                return "discharging_high"
            return "discharging_full"
        else:
            if self._capacity > 95:
                return "charged"
            return "charging"
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
