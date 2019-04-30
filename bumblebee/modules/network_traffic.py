"""Displays network traffic
"""

import psutil
import netifaces
import bytefmt

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.utilization)
        )

        self._default_adapter = netifaces.gateways()['default'][netifaces.AF_INET][1]

        self._download_tx, self._upload_tx = self.network_tx()

    def utilization(self, widget):
        return "{0} {1}".format(
            bytefmt.humanize(self._final_download_tx),
            bytefmt.humanize(self._final_upload_tx)
        )

    def update(self, widgets):
        download_tx, upload_tx = self.network_tx() 
        
        self._final_download_tx = (download_tx - self._download_tx)
        self._final_upload_tx = (upload_tx - self._upload_tx)

        self._download_tx, self._upload_tx = download_tx, upload_tx

    def network_tx(self):
        io_counters = psutil.net_io_counters(pernic=True)
        network = io_counters[self._default_adapter]

        return network.bytes_recv, network.bytes_sent


