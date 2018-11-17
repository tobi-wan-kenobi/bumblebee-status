# pylint: disable=C0111,R0903

"""Displays battery status, remaining percentage and charging information.

Parameters:
    * battery.device     : Comma-separated list of battery devices to read information from (defaults to auto for auto-detection)
    * battery.warning    : Warning threshold in % of remaining charge (defaults to 20)
    * battery.critical   : Critical threshold in % of remaining charge (defaults to 10)
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
        widgets = []
        super(Module, self).__init__(engine, config, widgets)
        self._batteries = []
        self._batteries.append("/sys/class/power_supply/BAT0")
        self._batteries.append("/sys/class/power_supply/BAT1")
        self.update(widgets)
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-power-statistics")

    def update(self, widgets):
        widget_all = []
        widget_all_name = "All"
        widget_all = self.widget(widget_all_name)
        if not widget_all:
                widget_all = bumblebee.output.Widget(full_text=self.capacity_all, name="All")
        self.capacity_all(widget_all)
        while len(widgets) > 0: del widgets[0]
        widgets.append(widget_all)
        self._widgets = widgets

    def remaining(self):
        estimate = 0.0
        try:
            estimate = power.PowerManagement().get_time_remaining_estimate()
            # do not show remaining if on AC
            if estimate == power.common.TIME_REMAINING_UNLIMITED:
                return None
            if estimate == power.common.TIME_REMAINING_UNKNOWN:
                return ""
        except Exception:
            return ""
        return bumblebee.util.durationfmt(estimate*60, shorten=True, suffix=True) # estimate is in minutes

    def capacity_all(self, widget):
        widget.set("capacity", -1)
        widget.set("ac", False)
        # if not os.path.exists(widget.name):
        #     widget.set("capacity", 100)
        #     widget.set("ac", True)
        #     return "ac"
        capacity = 100
        energy_now = 0
        energy_full = 0
        for path in self._batteries:
            try:
                with open("{}/energy_full".format(path)) as f:
                    energy_full += int(f.read())
                with open("{}/energy_now".format(path)) as o:
                    energy_now += int(o.read())
            except IOError:
                return "n/a"

        capacity = int( energy_now / energy_full  * 100)
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
