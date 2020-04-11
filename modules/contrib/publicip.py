"""Displays public IP address

Requires the following python packages:
    * requests

Parameters:
    * publicip.region: us-central (default), us-east, us-west, uk, de, pl, nl
    * publicip.service: web address that returns plaintext ip address (ex. 'http://l2.io/ip')
"""

from requests import get

import core.module
import core.widget
import core.decorators

class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config):
        super().__init__(config, core.widget.Widget(self.public_ip))

        self.__avail__regions = {'us-east':'http://checkip.amazonaws.com',
                               'us-central':'http://checkip.amazonaws.com',
                               'us-west':'http://ipv4bot.whatismyipaddress.com',
                               'pl':'http://ip.42.pl/raw',
                               'de':'http://myexternalip.com/raw',
                               'nl':'http://tnx.nl/ip',
                               'uk':'http://ident.me'}
        self.__region = self.parameter('region', 'us-central')
        self.__service = self.parameter('service', '')
        self.__ip = ''


    def public_ip(self, widget):
        return self.__ip

    def update(self):
        try:
            if self.__service:
                self.address = self.__service
            else:
                self.address = self.__avail__regions[self.__region]
            self.__ip = get(self.address).text.rstrip()
        except Exception:
            self.__ip = 'n/a'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
