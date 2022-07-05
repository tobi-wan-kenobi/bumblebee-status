"""
Displays public IP address and, optionally, Country Name, Country Code & City Name
Maximum refresh interval should be 5 minutes to avoid free SLA breach from providers
Note: 1 request/5 minutes is 8640 requests/month
Provider information contained in core.location
Left mouse click forces immediate update

Parameters (Default in brackets)_
ip (True) 		Public IP address
country_name (False) 	Display name of country associated with the IP
country_code (False)	Display country code of country associated with the IP
city_name (False) 	Display name of city associated with the IP
coordinates (False) 	Display name of city associated with the IP
all (False) 		Display all information associate with the IP

Examples
By default only the public IP is shown
bumblebee-status -m publicip

To also include the country name...
bumblebee-status -m publicip -p publicip.country_name=True

To include all ava

"""

import core.module
import core.widget
import core.decorators
import core.input
import util.format
import util.location


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.public_ip))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__click_update)

        self.__ip = ""			# Public IP address
        self.__country_name = ""	# Country name associated with public IP address
        self.__country_code = ""	# Country code associated with public IP address
        self.__city_name = ""		# City name associated with public IP address
        self.__coordinates = ""		# Coordinated assoicated with public IP address

        # Handle failure to get IP information
        self.__ip_error = False

        # Process option paramaters
        self.__show_ip = util.format.asbool(
            self.parameter("ip", True)
        )
        self.__show_country_name = util.format.asbool(
            self.parameter("country_name", False)
        )
        self.__show_country_code = util.format.asbool(
            self.parameter("country_code", False)
        )
        self.__show_city_name = util.format.asbool(self.parameter("city_name", False))
        self.__show_coordinates = util.format.asbool(
            self.parameter("coordinates", False)
        )
        self.__show_all = util.format.asbool(self.parameter("all", False))

    def __click_update(self, event):
        util.location.reset()

    def public_ip(self, widget):
        __output = ""

        if self.__ip:
            if self.__show_ip or self.__show_all:
                __output = self.__ip
            self.__ip_error = False
        else:
            self.__ip_error = True
            __output = "Error Getting IP"

        if not self.__ip_error:
            if self.__show_country_name or self.__show_all:
                if self.__country_name:
                    __output += " " + self.__country_name
                else:
                    __output += " " + "?"

            if self.__show_country_code or self.__show_all:
                if self.__country_code:
                    __output += " " + "(" + self.__country_code + ")"
                else:
                    __output += " " + "(?)"

            if self.__show_city_name or self.__show_all:
                if self.__city_name:
                    __output += " " + self.__city_name
                else:
                    __output += " " + "?"

            if self.__show_coordinates or self.__show_all:
                if self.__coordinates:
                    __output += " " + self.__coordinates
                else:
                    __output += " " + "?"

        return __output

    def update(self):
        try:
            self.__ip = util.location.public_ip()
        except Exception:
            self.__ip = None

        if self.__show_country_name or self.__show_all:
            try:
                self.__country_name = util.location.country_name()
            except Exception:
                self.__country_name = None

        if self.__show_country_code or self.__show_all:
            try:
                self.__country_code = util.location.country_code()
            except Exception:
                self.__country_code = None

        if self.__show_city_name or self.__show_all:
            try:
                self.__city_name = util.location.city_name()
            except Exception:
                self.__city_name = None

        if self.__show_coordinates or self.__show_all:
            try:
                __tmp = util.location.coordinates()
                __lat = "{:.2f}".format(__tmp[0])
                __lon = "{:.2f}".format(__tmp[1])
                __output = __lat + "°N" + "," + " " + __lon + "°E"
                self.__coordinates = __output
            except Exception:
                self.__city_name = None


# vim: tabstop=7 expandtab shiftwidth=4 softtabstop=4
