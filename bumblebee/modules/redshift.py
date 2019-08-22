# pylint: disable=C0111,R0903

"""Displays the current color temperature of redshift

Requires the following executable:
    * redshift

Parameters:
    * redshift.location : location provider, either of "geoclue2" (default), \
"ipinfo" (requires the requests package), or "manual"
    * redshift.lat : latitude if location is set to "manual"
    * redshift.lon : longitude if location is set to "manual"
"""

import threading
try:
    import requests
except ImportError:
    pass

import bumblebee.input
import bumblebee.output
import bumblebee.engine


def is_terminated():
    for thread in threading.enumerate():
        if thread.name == "MainThread" and not thread.is_alive():
            return True
    return False


def get_redshift_value(widget, location, lat, lon):
    while True:
        if is_terminated():
            return
        widget.get("condition").acquire()
        while True:
            try:
                widget.get("condition").wait(1)
            except RuntimeError:
                continue
            break
        widget.get("condition").release()

        command = ["redshift", "-p", "-l"]
        if location == "manual":
            command.append(lat + ":" + lon)
        else:
            command.append("geoclue2")

        try:
            res = bumblebee.util.execute(" ".join(command))
        except Exception:
            res = ""
            widget.set("temp", "n/a")
            widget.set("transition", None)
            widget.set("state", "day")
        for line in res.split("\n"):
            line = line.lower()
            if "temperature" in line:
                widget.set("temp", line.split(" ")[2])
            if "period" in line:
                state = line.split(" ")[1]
                if "day" in state:
                    widget.set("state", "day")
                elif "night" in state:
                    widget.set("state", "night")
                else:
                    widget.set("state", "transition")
                    widget.set("transition", " ".join(line.split(" ")[2:]))


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.text)
        super(Module, self).__init__(engine, config, widget)

        self._location = self.parameter("location", "geoclue2")
        self._lat = self.parameter("lat", None)
        self._lon = self.parameter("lon", None)

        # Even if location method is set to manual, if we have no lat or lon,
        # fall back to the geoclue2 method.
        if self._location == "manual" and (self._lat is None
                                           or self._lon is None):
            self._location == "geoclue2"

        if self._location == "ipinfo":
            try:
                location_url = "http://ipinfo.io/json"
                location = requests.get(location_url).json()
                self._lat, self._lon = location["loc"].split(",")
                self._lat = str(float(self._lat))
                self._lon = str(float(self._lon))
                self._location = "manual"
            except Exception:
                # Fall back to geoclue2.
                self._location = "geoclue2"

        self._text = ""
        self._condition = threading.Condition()
        widget.set("condition", self._condition)
        self._thread = threading.Thread(target=get_redshift_value,
                                        args=(widget, self._location,
                                              self._lat, self._lon))
        self._thread.start()
        self._condition.acquire()
        self._condition.notify()
        self._condition.release()

    def text(self, widget):
        return "{}".format(self._text)

    def update(self, widgets):
        widget = widgets[0]
        self._condition.acquire()
        self._condition.notify()
        self._condition.release()
        temp = widget.get("temp", "n/a")
        self._text = temp
        transition = widget.get("transition", None)
        if transition:
            self._text = "{} {}".format(temp, transition)

    def state(self, widget):
        return widget.get("state", None)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
