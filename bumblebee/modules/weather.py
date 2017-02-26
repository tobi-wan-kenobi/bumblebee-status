# pylint: disable=C0111,R0903

"""Displays the temperature on the current location based on the ip

Requires the following python packages:
    * urllib

"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import json
from urllib.request import urlopen

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.temperature)
        )
        self._timer = 0
        self._temperature = 0

    def temperature(self, widget):
        return "{}°C".format(self._temperature)

    def update(self, widgets):
        if self._timer == 0:
            location_url = 'http://ipinfo.io/json'
            location = json.loads(urlopen(location_url).read())
            # city = location['city']
            # country = location['country']
            coord = location['loc'].split(',')
            # weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={city},{country}'.format(city=city, country=country)
            weather_url = 'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=9c672428ac92772c6437191a43a5b13f&units=metric'.format(lat=coord[0], lon=coord[1])
            weather = json.loads(urlopen(weather_url).read())
            self._temperature = weather['main']['temp']
            self._timer += 1
            return
        if self._timer < 300:
            self._timer += 1
            return
        self._timer = 0

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
