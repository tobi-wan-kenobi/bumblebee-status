# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays the temperature on the current location based on the ip

Requires the following python packages:
    * requests

Parameters:
    * weather.location: Set location, defaults to 'auto' for getting location automatically from a web service
      If set to a comma-separated list, left-click and right-click can be used to rotate the locations.
      Locations should be city names or city ids.
    * weather.unit: metric (default), kelvin, imperial
    * weather.showcity: If set to true, show location information, otherwise hide it (defaults to true)
    * weather.showminmax: If set to true, show the minimum and maximum temperature, otherwise hide it (defaults to false)
    * weather.apikey: API key from http://api.openweathermap.org


contributed by `TheEdgeOfRage <https://github.com/TheEdgeOfRage>`_ - many thanks!
"""

import core.module
import core.widget
import core.input

import util.format
import util.location

import re

import requests
from requests.exceptions import RequestException


class Module(core.module.Module):
    @core.decorators.every(minutes=15)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__temperature = 0
        self.__apikey = self.parameter("apikey", "af7bfe22287c652d032a3064ffa44088")
        self.__location = util.format.aslist(self.parameter("location", "auto"))

        self.__index = 0
        self.__showcity = util.format.asbool(self.parameter("showcity", True))
        self.__showminmax = util.format.asbool(self.parameter("showminmax", False))
        self.__unit = self.parameter("unit", "metric")
        self.__valid = False

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.__next_location
        )
        core.input.register(
            self, button=core.input.RIGHT_MOUSE, cmd=self.__prev_location
        )

    def __next_location(self, event):
        self.__index = (self.__index + 1) % len(self.__location)
        self.update()

    def __prev_location(self, event):
        self.__index = (
            len(self.__location) - 1 if self.__index <= 0 else self.__index - 1
        )
        self.update()

    def temperature(self):
        return util.format.astemperature(self.__temperature, self.__unit)

    def tempmin(self):
        return util.format.astemperature(self.__tempmin, self.__unit)

    def tempmax(self):
        return util.format.astemperature(self.__tempmax, self.__unit)

    def city(self):
        city = re.sub(r"[_-]", " ", self.__city)
        return "{} ".format(city)

    def output(self, widget):
        if not self.__valid:
            return "?"
        if self.__showminmax:
            self.__showcity = False
            return (
                self.city()
                + self.temperature()
                + "  Hi:"
                + self.tempmax()
                + "  Lo:"
                + self.tempmin()
            )
        elif self.__showcity:
            return self.city() + self.temperature()
        else:
            return self.temperature()

    def state(self, widget):
        if self.__valid:
            if "thunderstorm" in self.__weather:
                return ["thunder"]
            elif "drizzle" in self.__weather:
                return ["rain"]
            elif "rain" in self.__weather:
                return ["rain"]
            elif "snow" in self.__weather:
                return ["snow"]
            elif "sleet" in self.__weather:
                return ["sleet"]
            elif "clear" in self.__weather:
                return ["clear"]
            elif "cloud" in self.__weather:
                return ["clouds"]

        return []

    def update(self):
        try:
            weather_url = "http://api.openweathermap.org/data/2.5/weather?appid={}".format(
                self.__apikey
            )
            weather_url = "{}&units={}".format(weather_url, self.__unit)
            if self.__location[self.__index] == "auto":
                coord = util.location.coordinates()
                weather_url = "{url}&lat={lat}&lon={lon}".format(
                    url=weather_url, lat=coord[0], lon=coord[1]
                )
            elif self.__location[self.__index].isdigit():
                weather_url = "{url}&id={id}".format(
                    url=weather_url, id=self.__location[self.__index]
                )
            else:
                weather_url = "{url}&q={city}".format(
                    url=weather_url, city=self.__location[self.__index]
                )
            weather = requests.get(weather_url).json()
            self.__city = weather["name"]
            self.__temperature = int(weather["main"]["temp"])
            self.__tempmin = int(weather["main"]["temp_min"])
            self.__tempmax = int(weather["main"]["temp_max"])
            self.__weather = weather["weather"][0]["main"].lower()
            self.__valid = True
        except Exception:
            self.__valid = False


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
