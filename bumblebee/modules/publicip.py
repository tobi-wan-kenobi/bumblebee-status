"""Displays public IP address

Requires the following python packages:
    * requests

Parameters:
    * publicip.region: us-central (default), us-east, us-west, uk, de, pl, nl 
    * publicip.service: web address that returns plaintext ip address (ex. "http://l2.io/ip")
"""

try:
    from requests import get
except ImportError:
    pass

import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.public_ip)
        )
        self._avail_regions = {"us-east":"http://l2.io/ip", 
                               "us-central":"http://whatismyip.akamai.com",
                               "us-west":"http://ipv4bot.whatismyipaddress.com",
                               "pl":"http://ip.42.pl/raw",
                               "de":"http://myexternalip.com/raw",
                               "nl":"http://tnx.nl/ip",
                               "uk":"http://ident.me"}
        self._region = self.parameter("region", "us-central")
        self._service = self.parameter("service", "")
        self._ip = ""


    def public_ip(self, widget):
        return self._ip

    def update(self, widgets):
        try:
            if self._service:
                self.address = self._service
            else:
                self.address = self._avail_regions[self._region]
            self._ip = get(self.address).text.rstrip()
        except Exception:
            self._ip = "No Connection"

