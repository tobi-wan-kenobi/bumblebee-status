# pylint: disable=C0111,R0903

"""Displays battery status, remaining percentage and charging information.

Parameters:
    * battery.device       : Comma-separated list of battery devices to read information from (defaults to auto for auto-detection)
    * battery.warning      : Warning threshold in % of remaining charge (defaults to 20)
    * battery.critical     : Critical threshold in % of remaining charge (defaults to 10)
    * batter.showremaining : If set to true (default) shows the remaining time until the batteries are completely discharged
"""

import os
import glob

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

try:
    import power
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        self._batteries = []
        # TODO: list all batteries
        self._batteries.append("/sys/class/power_supply/BAT0")
        self._batteries.append("/sys/class/power_supply/BAT1")
        self._batteries.append("/sys/class/power_supply/battery")

        super(Module, self).__init__(engine, config, bumblebee.output.Widget(full_text=self.capacity))

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-power-statistics")

    def remaining(self):
        estimate = 0.0
        power_now = 0.0
        try:
            estimate = power.PowerManagement().get_time_remaining_estimate()
            # do not show remaining if on AC
            if estimate == power.common.TIME_REMAINING_UNLIMITED:
                return None
            elif estimate == power.common.TIME_REMAINING_UNKNOWN:
                return ""
        except Exception:
            return ""
        return bumblebee.util.durationfmt(estimate*60, shorten=True, suffix=True) # estimate is in minutes

    def capacity(self, widget):
        widget.set("capacity", -1)
        widget.set("ac", False)
        capacity = 100
        self.energy_now = 0
        self.energy_full = 0
        errors = 0
        for path in self._batteries:
            try:
                with open("{}/energy_full".format(path)) as f:
                    self.energy_full += int(f.read())
                with open("{}/energy_now".format(path)) as o:
                    self.energy_now += int(o.read())
            except IOError:
                return "n/a"
            except Exception:
                errors += 1

        if errors == len(self._batteries):
            # if all batteries return errors, but we are still running
            # assume we are on A/C
            widget.set("ac", True)
            widget.set("capacity", 100)
            return "ac"

        capacity = int( float(self.energy_now) / float(self.energy_full) * 100.0)
        capacity = capacity if capacity < 100 else 100
        widget.set("capacity", capacity)
        output =  "{}%".format(capacity)
        widget.set("theme.minwidth", "100%")
        
        if bumblebee.util.asbool(self.parameter("showremaining", True))\
                and self.getCharge(widget) == "Discharging":
            output = "{} {}".format(output, self.remaining())

        return output

       
    def state(self, widget):
        state = []
        capacity = widget.get("capacity")

        if capacity < 0:
            return ["critical", "unknown"]

        if capacity < int(self.parameter("critical", 10)):
            state.append("critical")
        elif capacity < int(self.parameter("warning", 20)):
            state.append("warning")

        if widget.get("ac"):
            state.append("AC")
        else:
            charge = self.getCharge(widget)
            if charge == "Discharging":
                state.append("discharging-{}".format(min([10, 25, 50, 80, 100], key=lambda i: abs(i-capacity))))
            elif charge == "Unknown":
                state.append("unknown-{}".format(min([10, 25, 50, 80, 100], key=lambda i: abs(i-capacity))))
            else:
                if capacity > 95:
                    state.append("charged")
                else:
                    state.append("charging")

        return state

    def getCharge(self, widget):
        charge = ""
        charge_list = []
        for x in range(len(self._batteries)):
            try:
                with open("{}/status".format(self._batteries[x])) as f:
                    charge_list.append(f.read().strip())
            except IOError:
                    pass
        for x in range(len(charge_list)):
            if charge_list[x] == "Discharging":
                charge = charge_list[x]
                break
        return charge
