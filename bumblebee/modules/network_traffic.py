#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Displays network traffic
   * No extra configuration needed
"""

import psutil
import netifaces

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

WIDGET_NAME = 'network_traffic'

class Module(bumblebee.engine.Module):
    """Bumblebee main module """

    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config)

        try:
            self._bandwidth = BandwidthInfo()

            self._bytes_recv = self._bandwidth.bytes_recv()
            self._bytes_sent = self._bandwidth.bytes_sent()
        except Exception:
            """ We do not want do explode anything """
            pass

    @classmethod
    def state(cls, widget):
        """Return the widget state"""

        if widget.name == '{}.rx'.format(WIDGET_NAME):
            return 'rx'
        elif widget.name == '{}.tx'.format(WIDGET_NAME):
            return 'tx'

        return None

    def update(self, widgets):
        try:
            bytes_recv = self._bandwidth.bytes_recv()
            bytes_sent = self._bandwidth.bytes_sent()

            download_rate = (bytes_recv - self._bytes_recv)
            upload_rate = (bytes_sent - self._bytes_sent)

            self.update_widgets(widgets, download_rate, upload_rate)

            self._bytes_recv, self._bytes_sent = bytes_recv, bytes_sent
        except Exception:
            """ We do not want do explode anything """
            pass

    @classmethod
    def update_widgets(cls, widgets, download_rate, upload_rate):
        """Update tx/rx widgets with new rates"""
        del widgets[:]

        widgets.extend((
            TrafficWidget(text=download_rate, direction='rx'),
            TrafficWidget(text=upload_rate, direction='tx')
        ))


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
        gateway = netifaces.gateways()['default']

        if not gateway:
            raise 'No default gateway found'

        return gateway[netifaces.AF_INET][1]

    @classmethod
    def io_counters(cls):
        """Return IO counters"""
        return psutil.net_io_counters(pernic=True)

class TrafficWidget(object):
    """Create a traffic widget with humanized bytes string with proper icon (up/down)"""
    def __new__(cls, text, direction):
        widget = bumblebee.output.Widget(name='{0}.{1}'.format(WIDGET_NAME, direction))
        widget.set('theme.minwidth', '0000000KiB/s')
        widget.full_text(cls.humanize(text))

        return widget

    @staticmethod
    def humanize(text):
        """Return humanized bytes"""
        humanized_byte_format = bumblebee.util.bytefmt(text)
        return '{0}/s'.format(humanized_byte_format)
