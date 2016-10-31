import datetime
import bumblebee.module

class Module(bumblebee.module.Module):
    def __init__(self, theme, args):
        super(Module, self).__init__(theme, args)
        self._battery = "BAT0" if not args else args[0]
        self._capacity = 0
        self._status = "Unknown"

    def data(self):
        with open("/sys/class/power_supply/{}/capacity".format(self._battery)) as f:
            self._capacity = int(f.read())

        return "{:02d}%".format(self._capacity)

    def state(self):
        with open("/sys/class/power_supply/{}/status".format(self._battery)) as f:
            self._status = f.read().strip()
        if self._status == "Discharging":
            return "discharging"
        else:
            return "charging"
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
