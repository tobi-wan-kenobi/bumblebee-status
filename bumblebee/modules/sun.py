# pylint: disable=C0111,R0903

"""Displays sunrise and sunset times

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

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
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
            return u"\u21A5{} \u21A7{}".format(self._sunrise.strftime('%H:%M'), self._sunset.strftime('%H:%M'))
        return "?"

    def _calculate_times(self):
        try:
            sun = Sun(self._lat, self._lon)
        except Exception:
            self._sunrise = None
            self._sunset = None
            return

        try:
            self._sunrise = sun.get_local_sunrise_time()
        except SunTimeException:
            self._sunrise = 'no sunrise'

        try:
            self._sunset = sun.get_local_sunset_time()
        except SunTimeException:
            self._sunset = 'no sunset'

    def update(self, widgets):
        if not self._lat or not self._lon:
            self._sunrise = None
            self._sunset = None
        self._calculate_times()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
