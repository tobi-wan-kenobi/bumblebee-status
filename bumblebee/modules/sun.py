# pylint: disable=C0111,R0903

"""Displays sunrise and sunset times

Requires the following python packages:
    * requests
    * suntime

Parameters:
    * cpu.lat : Latitude of your location
    * cpu.lon : Longitude of your location
"""

try:
    from suntime import Sun, SunTimeException
except ImportError:
    pass
try:
    import requests
except ImportError:
    pass
try:
    from dateutil.tz import tzlocal
except ImportError:
    pass

import datetime

import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine, config,
            bumblebee.output.Widget(full_text=self.suntimes)
        )
        self.interval(3600)
        self._lat = self.parameter("lat", None)
        self._lon = self.parameter("lon", None)
        try:
            if not self._lat or not self._lon:
                location_url = "http://ipinfo.io/json"
                location = requests.get(location_url).json()
                self._lat, self._lon = location["loc"].split(",")
            self._lat = float(self._lat)
            self._lon = float(self._lon)
        except Exception:
            pass
        self.update(None)

    def suntimes(self, _):
        if self._sunset and self._sunrise:
            if self._isup:
                return u"\u21A7{} \u21A5{}".format(
                    self._sunset.strftime('%H:%M'),
                    self._sunrise.strftime('%H:%M'))
            return u"\u21A5{} \u21A7{}".format(self._sunrise.strftime('%H:%M'),
                                               self._sunset.strftime('%H:%M'))
        return "?"

    def _calculate_times(self):
        self._isup = False
        try:
            if not self._lat or not self._lon:
                raise()
            sun = Sun(self._lat, self._lon)
        except Exception:
            self._sunrise = None
            self._sunset = None
            return

        order_matters = True

        try:
            self._sunrise = sun.get_local_sunrise_time()
        except SunTimeException:
            self._sunrise = "no sunrise"
            order_matters = False

        try:
            self._sunset = sun.get_local_sunset_time()
        except SunTimeException:
            self._sunset = "no sunset"
            order_matters = False

        if not order_matters:
            return

        now = datetime.datetime.now(tz=tzlocal())
        if now > self._sunset:
            tomorrow = (now + datetime.timedelta(days=1)).date()
            try:
                self._sunrise = sun.get_local_sunrise_time(tomorrow)
                self._sunset = sun.get_local_sunset_time(tomorrow)
            except SunTimeException:
                self._sunrise = "no sunrise"
                self._sunset = "no sunset"

        elif now > self._sunrise:
            tomorrow = (now + datetime.timedelta(days=1)).date()
            try:
                self._sunrise = sun.get_local_sunrise_time(tomorrow)
            except SunTimeException:
                self._sunrise = "no sunrise"
                return
            self._isup = True

    def update(self, widgets):
        if not self._lat or not self._lon:
            self._sunrise = None
            self._sunset = None
        self._calculate_times()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
