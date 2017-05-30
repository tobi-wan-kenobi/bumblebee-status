"""Displays public IP address

Parameter:
    * Test
    * Test
"""

try:
    from urllib2 import urlopen
except ImportError:
    pass

import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.public_ip)
        )

        self._ip = ""


    def public_ip(self, widget):
        return self._ip

    def update(self, widgets):
        try:
            self._ip = urlopen("http://ip.42.pl/raw").read()
        except Exception:
            self._ip = "Not Connected"

