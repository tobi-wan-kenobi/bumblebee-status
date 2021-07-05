"""
A module to show currently active network connection (ethernet or wifi)
and connection strength.
"""

import subprocess
import os

import core.module
import core.widget


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.network))
        self._is_wireless = True
        self._interface = None
        self._message = None

    def network(self, widgets):
        # start subprocess to get networked data
        std_out = os.popen("ip route get 8.8.8.8")
        route_str = " ".join(std_out.read().split())
        route_tokens = route_str.split(" ")

        try:
            self._interface = route_tokens[route_tokens.index("dev") + 1] + ":"
        except ValueError:
            self._interface = None

        with open("/proc/net/wireless", "r") as f:
            if self._interface:
                self._is_wireless = self._interface in f.read()

        # setup message to send to bar
        if self._interface is None:
            self._message = "Not connected to a network"
        elif self._is_wireless:
            self._message = "Connected to WiFi"
        else:
            # self._message = "Connected to Ethernet"
            self._message = self._message
            

        return self._message



