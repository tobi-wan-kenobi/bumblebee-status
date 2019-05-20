# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays the temperature on the current location based on the ip

Requires the following python packages:
    * requests

Parameters:
    * weather.location: Set location, defaults to 'auto' for getting location from http://ipinfo.io
                        If set to a comma-separated list, left-click and right-click can be used to rotate the locations.
                        Locations should be city names or city ids.
    * weather.unit: metric (default), kelvin, imperial
    * weather.showcity: If set to true, show location information, otherwise hide it (defaults to true)
    * weather.apikey: API key from http://api.openweathermap.org
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import re

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._temperature = 0
        self._apikey = self.parameter("apikey", "af7bfe22287c652d032a3064ffa44088")
        self._location = self.parameter("location", "auto")
        if "," in self._location:
            self._location = self._location.split(",")
        else:
            self._location = [self._location]
        self._index = 0
        self._showcity = bumblebee.util.asbool(self.parameter("showcity", True))
        self._unit = self.parameter("unit", "metric")
        self._valid = False
        self.interval(15)

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd=self._next_location)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=self._prev_location)

    def _next_location(self, event):
        self._index = 0 if self._index >= len(self._location) - 1 else self._index + 1
        self.update(self.widgets())

    def _prev_location(self, event):
        self._index = len(self._location)-1 if self._index <= 0 else self._index - 1
        self.update(self.widgets())

    def _unit_suffix(self):
        if self._unit == "metric":
            return "C"
        if self._unit == "kelvin":
            return "K"
        if self._unit == "imperial":
            return "F"
        return ""

    def temperature(self):
        return u"{}°{}".format(self._temperature, self._unit_suffix())

    def city(self):
        city = re.sub('[_-]', ' ', self._city)
        return u"{} ".format(city)

    def output(self, widget):
        if not self._valid:
            return u"?"
        if self._showcity:
            return self.city() + self.temperature()
        else:
            return self.temperature()

    def state(self, widget):
        if self._valid:
            if "thunderstorm" in self._weather:
                return ['thunder']
            elif "drizzle" in self._weather:
                return ['rain']
            elif "rain" in self._weather:
                return ['rain']
            elif "snow" in self._weather:
                return ['snow']
            elif "sleet" in self._weather:
                return ['sleet']
            elif "clear" in self._weather:
                return ['clear']
            elif "cloud" in self._weather:
                return ['clouds']
            else:
                return []

        return []

    def update(self, widgets):
        try:
            weather_url = "http://api.openweathermap.org/data/2.5/weather?appid={}".format(self._apikey)
            weather_url = "{}&units={}".format(weather_url, self._unit)
            if self._location[self._index] == "auto":
                location_url = "http://ipinfo.io/json"
                location = requests.get(location_url).json()
                coord = location["loc"].split(",")
                weather_url = "{url}&lat={lat}&lon={lon}".format(url=weather_url, lat=coord[0], lon=coord[1])
            elif self._location[self._index].isdigit():
                weather_url = "{url}&id={id}".format(url=weather_url, id=self._location[self._index])
            else:
                weather_url = "{url}&q={city}".format(url=weather_url, city=self._location[self._index])
            weather = requests.get(weather_url).json()
            self._city = weather['name']
            self._temperature = int(weather['main']['temp'])
            self._weather = weather['weather'][0]['main'].lower()
            self._valid = True
        except RequestException:
            self._valid = False
        except Exception:
            self._valid = False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
