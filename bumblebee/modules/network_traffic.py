"""Displays network traffic
"""

import psutil
import netifaces

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config)

        self._bandwidth = BandwidthInfo()

        self._download_tx = self._bandwidth.bytes_recv()
        self._upload_tx = self._bandwidth.bytes_sent()

    def update(self, widgets):
        download_tx = self._bandwidth.bytes_recv()
        upload_tx = self._bandwidth.bytes_sent()

        download_rate = (download_tx - self._download_tx)
        upload_rate = (upload_tx - self._upload_tx)

        self.update_widgets(widgets, download_rate, upload_rate)

        self._download_tx, self._upload_tx = download_tx, upload_tx

    def update_widgets(self, widgets, download_rate, upload_rate):
        del widgets[:]

        widgets.extend((
            TrafficWidget(download_rate, ''),
            TrafficWidget(upload_rate, '')
        ))


class BandwidthInfo:
    def __init__(self):
        io_counters = self.io_counters()
        self.network = io_counters[self.default_network_adapter()]

    def bytes_recv(self):
        return self.bandwidth().bytes_recv

    def bytes_sent(self):
        return self.bandwidth().bytes_sent

    def bandwidth(self):
        io_counters = self.io_counters()
        return io_counters[self.default_network_adapter()]

    def default_network_adapter(self):
        gateways = netifaces.gateways()
        return gateways['default'][netifaces.AF_INET][1]

    def io_counters(self):
        return psutil.net_io_counters(pernic=True)


class TrafficWidget:
    def __new__(self, text, icon):
        widget = bumblebee.output.Widget()
        widget.set('theme.minwidth', '00000000KiB/s')
        widget.full_text(self.humanize(text, icon))

        return widget

    @staticmethod
    def humanize(text, icon):
        humanized_byte_format = bumblebee.util.bytefmt(text)
        return '{0} {1}/s'.format(icon, humanized_byte_format)
