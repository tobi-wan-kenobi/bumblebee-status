"""
A module to show currently active network connection (ethernet or wifi) and connection strength if the connection is wireless.

Dependencies: nm-connection-editor if users would like a graphical
network manager when left-clicking the module
"""


import util.cli
import util.format

import core.module
import core.widget
import core.input

import netifaces
import socket


class Module(core.module.Module):
    @core.decorators.every(seconds=10)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.network))
        self.__is_wireless = False
        self.__is_connected = False
        self.__interface = None
        self.__message = None
        self.__signal = -110

    # Get network information to display to the user
    def network(self, widgets):
        # Determine whether there is an internet connection
        try:
            socket.create_connection(("1.1.1.1", 53))
            self.__is_connected = True
        except:
            self.__is_connected = False

        # Attempt to extract a valid network interface device
        self.__interface = netifaces.gateways()["default"][netifaces.AF_INET][1]

        # Check to see if the interface (if connected to the internet) is wireless
        if self.__is_connected:
            with open("/proc/net/wireless", "r") as f:
                self.__is_wireless = self.__interface in f.read()
            f.close()

        # setup message to send to the user
        if not self.__is_connected:
            self.__message = "No connection"
        elif not self.__is_wireless:
            # Assuming that if user is connected via non-wireless means that it will be ethernet
            self.__signal = -30
            self.__message = "Ethernet"
        else:
            # We have a wireless connection
            iw_dat = util.cli.execute("iwgetid")
            has_ssid = "ESSID" in iw_dat
            signal = self.__compute_signal(self.__interface)
            self.__signal = util.format.asint(signal, minimum=-110, maximum=-30)

            ssid = (
                iw_dat[iw_dat.index(":") + 1 :].replace('"', "").strip()
                if has_ssid
                else "Unknown"
            )
            self.__message = self.__generate_wireles_message(ssid, self.__signal)

        return self.__message

    # State determined by signal strength
    def state(self, widget):
        if self.__compute_strength(self.__signal) < 50:
            return "critical"
        if self.__compute_strength(self.__signal) < 75:
            return "warning"

        return None

    # manually done for better granularity / ease of parsing strength data
    def __generate_wireles_message(self, ssid, signal):
        computed_strength = self.__compute_strength(signal)
        return "{} {}%".format(ssid, int(computed_strength))

    def __compute_strength(self, signal):
        return 100 * ((signal + 100) / 70.0)

    # get signal strength in decibels/milliwat
    def __compute_signal(self, interface):
        # Get connection strength
        cmd = "iwconfig {}".format(interface)
        config_dat = " ".join(util.cli.execute(cmd).split())
        config_tokens = config_dat.replace("=", " ").split()
        signal = config_tokens[config_tokens.index("level") + 1]

        return signal
