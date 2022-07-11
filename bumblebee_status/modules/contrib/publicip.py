"""
Displays information about the public IP address associated with the default route:
    * Public IP address
    * Country Name
    * Country Code
    * City Name
    * Geographic Coordinates

Left mouse click on the widget forces immediate update
Any change to the default route will cause the widget to update

Requirements:
    * netifaces

Parameters:
    * publicip.format: Format string (defaults to ‘{ip} ({country_code})’)
    * Available format strings - ip, country_name, country_code, city_name, coordinates

Examples:
    * bumblebee-status -m publicip -p publicip.format="{ip} ({country_code})"
    * bumblebee-status -m publicip -p publicip.format="{ip} which is in {city_name}"
    * bumblebee-status -m publicip -p publicip.format="Your packets are right here: {coordinates}"

contributed by `tfwiii <https://github.com/tfwiii>`_ - many thanks!
"""

import re
import threading
import netifaces
import time

import core.module
import core.widget
import core.input
import core.decorators

import util.format
import util.location


def update_publicip_information(module):
    widget = module.widget()
    __previous_default_route = None
    __current_default_route = None
    __interval = 5  # Interval between default route change checks

    while True:
        __current_default_route = netifaces.gateways()["default"][2]

        # Updates public ip information if a change to default route is detected
        if __current_default_route != __previous_default_route:
            # Sets __previous_default_route in preparation for next change check
            __previous_default_route = __current_default_route

            # Refresh location information
            util.location.reset()

            # Fetch fresh location information
            __info = util.location.location_info()

            # Contstruct coordinates string
            __lat = "{:.2f}".format(__info["latitude"])
            __lon = "{:.2f}".format(__info["longitude"])
            __coords = __lat + "°N" + "," + " " + __lon + "°E"

            # Set widget values
            widget.set("public_ip", __info["public_ip"])
            widget.set("country_name", __info["country"])
            widget.set("country_code", __info["country_code"])
            widget.set("city_name", __info["city_name"])
            widget.set("coordinates", __coords)

            # Update widget values
            core.event.trigger("update", [widget.module.id], redraw_only=True)

        # Wait __interval seconds before checking for default route changes again
        time.sleep(__interval)

class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.publicip))

        self.__thread = None

        # Immediate update (override default) when left click on widget
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__click_update)

        # By default show: <ip> (<2 letter country code>)
        self._format = self.parameter("format", "{ip} ({country_code})")

    def publicip(self, widget):
        return self._format.format(
            ip=widget.get("public_ip", "-"),
            country_name=widget.get("country_name", "-"),
            country_code=widget.get("country_code", "-"),
            city_name=widget.get("city_name", "-"),
            coordinates=widget.get("coordinates", "-"),
        )

    def __click_update(self, event):
        util.location.reset()

    def update(self):
        if self.__thread is not None and self.__thread.is_alive():
            return
        self.__thread = threading.Thread(
            target=update_publicip_information, args=(self,)
        )
        self.__thread.start()

    def state(self, widget):
        return widget.get("state", None)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
