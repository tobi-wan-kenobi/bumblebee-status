# pylint: disable=C0111,R0903

"""Displays sunrise and sunset times

Requires the following python packages:
    * requests
    * suntime

Parameters:
    * cpu.lat : Latitude of your location
    * cpu.lon : Longitude of your location
"""

from suntime import Sun, SunTimeException
import requests
from dateutil.tz import tzlocal

import datetime

import core.module
import core.widget
import core.decorators

import util.location

class Module(core.module.Module):
    @core.decorators.every(hours=1)
    def __init__(self, config):
        super().__init__(config, core.widget.Widget(self.suntimes))

        self.__lat = self.parameter('lat', None)
        self.__lon = self.parameter('lon', None)

        if not self.__lat or not self.__lon:
            self.__lat, self.__lon = util.location.coordinates()

    def suntimes(self, _):
        if self.__sunset and self.__sunrise:
            if self.__isup:
                return u'\u21A7{} \u21A5{}'.format(
                    self.__sunset.strftime('%H:%M'),
                    self.__sunrise.strftime('%H:%M'))
            return u'\u21A5{} \u21A7{}'.format(self.__sunrise.strftime('%H:%M'),
                                               self.__sunset.strftime('%H:%M'))
        return 'n/a'

    def __calculate_times(self):
        self.__isup = False
        try:
            if not self.__lat or not self.__lon:
                raise()
            sun = Sun(float(self.__lat), float(self.__lon))
        except Exception:
            self.__sunrise = None
            self.__sunset = None
            return

        order_matters = True

        try:
            self.__sunrise = sun.get_local_sunrise_time()
        except SunTimeException:
            self.__sunrise = 'no sunrise'
            order_matters = False

        try:
            self.__sunset = sun.get_local_sunset_time()
        except SunTimeException:
            self.__sunset = 'no sunset'
            order_matters = False

        if not order_matters:
            return

        now = datetime.datetime.now(tz=tzlocal())
        if now > self.__sunset:
            tomorrow = (now + datetime.timedelta(days=1)).date()
            try:
                self.__sunrise = sun.get_local_sunrise_time(tomorrow)
                self.__sunset = sun.get_local_sunset_time(tomorrow)
            except SunTimeException:
                self.__sunrise = 'no sunrise'
                self.__sunset = 'no sunset'

        elif now > self.__sunrise:
            tomorrow = (now + datetime.timedelta(days=1)).date()
            try:
                self.__sunrise = sun.get_local_sunrise_time(tomorrow)
            except SunTimeException:
                self.__sunrise = 'no sunrise'
                return
            self.__isup = True

    def update(self ):
        if not self.__lat or not self.__lon:
            self.__sunrise = None
            self.__sunset = None
        self.__calculate_times()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
