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


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.publicip))

        self.__previous_default_route = None
        self.__current_default_route = None
        self.background = True

        # Immediate update (override default) when left click on widget
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__click_update)

        # By default show: <ip> (<2 letter country code>)
        self._format = self.parameter("format", "{ip} ({country_code})")

        self.__monitor = threading.Thread(target=self.monitor, args=())
        self.__monitor.start()

    def monitor(self):
        current_default_route = None
        default_route = None
        while threading.main_thread().is_alive():
            current_default_route = netifaces.gateways()["default"][2]
            if current_default_route != default_route:
                self.update()
            time.sleep(1)

    def publicip(self, widget):
        if widget.get("public_ip") == None:
            return "n/a"
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
        widget = self.widget()

        try:
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
        except:
            widget.set("public_ip", None)

    def state(self, widget):
        return widget.get("state", None)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
