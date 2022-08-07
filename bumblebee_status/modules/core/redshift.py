# pylint: disable=C0111,R0903

"""Displays the current color temperature of redshift

Requires the following executable:
    * redshift

Parameters:
    * redshift.location : location provider, either of 'auto' (default), 'geoclue2',
      'ipinfo' or 'manual'
      'auto' uses whatever redshift is configured to do
    * redshift.lat : latitude if location is set to 'manual'
    * redshift.lon : longitude if location is set to 'manual'
    * redshift.show_transition: information about the transitions (x% day) defaults to True
    * redshift.adjust: set this to 'true' (defaults to false) to let bumblebee-status adjust color temperature, instead of just showing the current settings
"""

import re
import threading

import core.module
import core.widget
import core.input
import core.decorators

import util.cli
import util.format
import util.location


def get_redshift_value(module):
    widget = module.widget()
    location = module.parameter("location", "auto")
    lat = module.parameter("lat", None)
    lon = module.parameter("lon", None)

    # Even if location method is set to manual, if we have no lat or lon,
    # fall back to the geoclue2 method.
    if location == "manual" and (lat is None or lon is None):
        location = "geoclue2"

    command = ["redshift"]

    if util.format.asbool(module.parameter("adjust", "false")) == True:
        command.extend(["-o", "-v"])
    else:
        command.append("-p")

    if location == "manual":
        command.extend(["-l", "{}:{}".format(lat, lon)])
    if location == "geoclue2":
        command.extend(["-l", "geoclue2"])

    try:
        res = util.cli.execute(" ".join(command))
    except Exception:
        res = ""
    widget.set("temp", "n/a")
    widget.set("transition", "")
    widget.set("state", "day")
    for line in res.split("\n"):
        line = line.lower()
        if "temperature" in line:
            widget.set("temp", line.split(" ")[2].upper())
        if "period" in line:
            state = line.split(" ")[1]
            if "day" in state:
                widget.set("state", "day")
            elif "night" in state:
                widget.set("state", "night")
            else:
                widget.set("state", "transition")
                match = re.search(r"(\d+)\.\d+% ([a-z]+)", line)
                widget.set(
                    "transition", "({}% {})".format(match.group(1), match.group(2))
                )
    core.event.trigger("update", [widget.module.id], redraw_only=True)


class Module(core.module.Module):
    @core.decorators.every(seconds=10)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))

        self.__thread = None
        self.show_transition = util.format.asbool(
            self.parameter("show_transition", True)
        )

        if self.parameter("location", "") == "ipinfo":
            # override lon/lat with ipinfo
            try:
                location = util.location.coordinates()
                self.set("lat", location[0])
                self.set("lon", location[1])
                self.set("location", "manual")
            except Exception:
                # Fall back to geoclue2.
                self.set("location", "geoclue2")

        self._text = ""

    def text(self, widget):
        val = widget.get("temp", "n/a")
        transition = widget.get("transition", "")
        if transition and self.show_transition:
            val = "{} {}".format(val, transition)
        return val

    def update(self):
        if self.__thread is not None and self.__thread.is_alive():
            return
        self.__thread = threading.Thread(target=get_redshift_value, args=(self,))
        self.__thread.start()

    def state(self, widget):
        return widget.get("state", None)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
