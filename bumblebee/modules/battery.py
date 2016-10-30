import datetime
import bumblebee.module

class Module(bumblebee.module.Module):
    def __init__(self, theme, args):
        super(Module, self).__init__(theme, args)
        self._battery = "BAT0" if not args else args[0]
        self._capacity = 0
        self._status = "Unknown"

    def data(self):
        with open("/sys/class/power_supply/%s/capacity" % self._battery) as f:
            self._capacity = int(f.read())
        with open("/sys/class/power_supply/%s/status" % self._battery) as f:
            self._status = f.read().strip()

        return "%02d%%" % self._capacity

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
