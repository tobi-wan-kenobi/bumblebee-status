"""
Displays information about the public IP address associated with the default route:
    * Public IP address
    * Country Name
    * Country Code
    * City Name
    * Geographic Coordinates

Left mouse click on the widget forces immediate update.
Any change to the default route will cause the widget to update.

Requirements:
    * netifaces

Parameters:
    * publicip.format: Format string (defaults to ‘{ip} ({country_code})’)
    * Available format strings - ip, country_name, country_code, city_name, coordinates

Examples:
    * bumblebee-status -m publicip -p publicip.format="{ip} ({country_code})"
    * bumblebee-status -m publicip -p publicip.format="{ip} which is in {city_name}"
    * bumblebee-status -m publicip -p publicip.format="Your packets are right here: {coordinates}"

contributed by `tfwiii <https://github.com/tfwiii>` - many thanks!
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
import logging

log = logging.getLogger(__name__)


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
        default_route = None
        interfaces = None
        # Initially set to True to force an info update on first pass
        information_changed = True

        self.update()

        while threading.main_thread().is_alive():
            # Look for any changes in the netifaces default route information
            try:
                current_default_route = netifaces.gateways()["default"][2]
            except:
                # error reading out default gw -> assume none exists
                current_default_route = None
            if current_default_route != default_route:
                default_route = current_default_route
                information_changed = True

            # netifaces does not check ALL routing tables which might lead to false negatives
            # (ref: http://linux-ip.net/html/routing-tables.html) so additionally... look for
            # any changes in the netifaces interfaces information which might also be an inticator
            # of a change of route/external IP
            if not information_changed: # Only check if no routing table change found
                try:
                    current_interfaces = netifaces.interfaces()
                except:
                    # error reading interfaces information -> assume none exists
                    current_interfaces = None
                if current_interfaces != interfaces:
                    interfaces = current_interfaces
                    information_changed = True

            # Update either routing or interface information has changed
            if information_changed:
                information_changed = False
                self.update()

            # Throttle the calls to netifaces
            time.sleep(1)

    def publicip(self, widget):
        if widget.get("public_ip") is None:
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
        except Exception as ex:
            widget.set("public_ip", None)
            logging.error(str(ex))

    def state(self, widget):
        return widget.get("state", None)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
