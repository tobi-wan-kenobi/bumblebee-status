"""
Displays zero or more of:
    * Public IP address
    * Country Name
    * Country Code
    * City Name
    * Geographic Coordinates\

Maximum refresh interval should be 5 minutes to avoid free SLA breach from providers
Note: 1 request/5 minutes is 8640 requests/month
Provider information contained in core.location

Left mouse click on the widget forces immediate update

Parameters:
publicip.format: Format string (defaults to ‘{ip} ({country_code})’)

Available format strings:
ip
country_name
country_code
city_name
coordinates

Examples:
bumblebee-status -m publicip -p publicip.format="{ip} ({country_code})"
bumblebee-status -m publicip -p publicip.format="{ip} which is in {city_name}"
bumblebee-status -m publicip -p publicip.format="Your packets are right here: {coordinates}"
"""

import core.module
import core.widget
import core.decorators
import core.input
import util.format
import util.location


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.public_ip))

        # Immediate update (override default) when left click on widget
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__click_update)

        self.__ip = ""  # Public IP address
        self.__country_name = ""  # Country name associated with public IP address
        self.__country_code = ""  # Country code associated with public IP address
        self.__city_name = ""  # City name associated with public IP address
        self.__coordinates = ""  # Coordinates assoicated with public IP address

        # By default show: <ip> (<2 letter country code>)
        self._format = self.parameter("format", "{ip} ({country_code})")

    def __click_update(self, event):
        util.location.reset()

    def public_ip(self, widget):
        if not self.__ip:
            return "Error fetching IP"
        else:
            return self._format.format(
                ip=self.__ip,
                country_name=self.__country_name,
                country_code=self.__country_code,
                city_name=self.__city_name,
                coordinates=self.__coordinates,
            )

    def update(self):
        try:
            __info = util.location.location_info()
            self.__ip = __info["public_ip"]
            self.__country_name = __info["country"]
            self.__country_code = __info["country_code"]
            self.__city_name = __info["city_name"]
            __lat = __info["latitude"]  
            __lon = __info["longitude"]  
            __lat = "{:.2f}".format(__lat)
            __lon = "{:.2f}".format(__lon)
            __output = __lat + "°N" + "," + " " + __lon + "°E"
            self.__coordinates = __output
        except Exception:
            pass


# vim: tabstop=7 expandtab shiftwidth=4 softtabstop=4
