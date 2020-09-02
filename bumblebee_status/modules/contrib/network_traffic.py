#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Displays network traffic
   * No extra configuration needed

contributed by `izn <https://github.com/izn>`_ - many thanks!
"""

import psutil
import netifaces

import core.module
import core.widget

import util.format

WIDGET_NAME = "network_traffic"


class Module(core.module.Module):
    def __init__(self, config, theme):
        widgets = [
            core.widget.Widget(
                name="{0}.rx".format(WIDGET_NAME),
                full_text=self.download_rate,
            ),
            core.widget.Widget(
                name="{0}.tx".format(WIDGET_NAME),
                full_text=self.upload_rate,
            ),
        ]
        super().__init__(config, theme, widgets)

        self.widgets()[0].set("theme.minwidth", "0000000KiB/s")
        self.widgets()[1].set("theme.minwidth", "0000000KiB/s")

        try:
            self._bandwidth = BandwidthInfo()

            self._rate_recv = 0
            self._rate_sent = 0
            self._bytes_recv = self._bandwidth.bytes_recv()
            self._bytes_sent = self._bandwidth.bytes_sent()
        except Exception:
            """ We do not want do explode anything """
            pass

    def state(self, widget):
        """Return the widget state"""

        if widget.name == "{}.rx".format(WIDGET_NAME):
            return "rx"
        elif widget.name == "{}.tx".format(WIDGET_NAME):
            return "tx"

        return None

    def update(self):
        try:
            bytes_recv = self._bandwidth.bytes_recv()
            bytes_sent = self._bandwidth.bytes_sent()

            self._rate_recv = bytes_recv - self._bytes_recv
            self._rate_sent = bytes_sent - self._bytes_sent

            self._bytes_recv, self._bytes_sent = bytes_recv, bytes_sent
        except Exception:
            """ We do not want do explode anything """
            pass

    def download_rate(self, _):
        return "{}/s".format(util.format.byte(self._rate_recv))

    def upload_rate(self, _):
        return "{}/s".format(util.format.byte(self._rate_sent))


class BandwidthInfo(object):
    """Get received/sent bytes from network adapter"""

    def bytes_recv(self):
        """Return received bytes"""
        return self.bandwidth().bytes_recv

    def bytes_sent(self):
        """Return sent bytes"""
        return self.bandwidth().bytes_sent

    def bandwidth(self):
        """Return bandwidth information"""
        io_counters = self.io_counters()
        return io_counters[self.default_network_adapter()]

    @classmethod
    def default_network_adapter(cls):
        """Return default active network adapter"""
        gateway = netifaces.gateways()["default"]

        return gateway[netifaces.AF_INET][1]

    @classmethod
    def io_counters(cls):
        """Return IO counters"""
        return psutil.net_io_counters(pernic=True)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
