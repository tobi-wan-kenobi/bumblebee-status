"""Displays public IP address
"""

import core.module
import core.widget
import core.decorators

import util.location


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.public_ip))

        self.__ip = ""

    def public_ip(self, widget):
        return self.__ip

    def update(self):
        try:
            self.__ip = util.location.public_ip()
        except Exception:
            self.__ip = "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
