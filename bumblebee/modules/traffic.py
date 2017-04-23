# pylint: disable=C0111,R0903

"""Displays network IO for interfaces.

Parameters:
    * traffic.exclude: Comma-separated list of interface prefixes to exclude (defaults to "lo,virbr,docker,vboxnet,veth")
"""

import re
import psutil
import netifaces

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = []
        super(Module, self).__init__(engine, config, widgets)
        self._exclude = tuple(filter(len, self.parameter("exclude", "lo,virbr,docker,vboxnet,veth").split(",")))
        self._update_widgets(widgets)
        self._status = ""

    def state(self, widget):
        if "traffic.rx" in widget.name:
            return "rx"
        if "traffic.tx" in widget.name:
            return "tx"
        return self._status

    def update(self, widgets):
        self._update_widgets(widgets)

    def _update_widgets(self, widgets):
        interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]

        counters = psutil.net_io_counters(pernic=True)
        for interface in interfaces:
            if not interface: interface = "lo"
            rx = counters[interface].bytes_recv
            tx = counters[interface].bytes_sent

            name = "traffic-{}".format(interface)
            txname = "traffic.tx-{}".format(interface)
            rxname = "traffic.rx-{}".format(interface)

            widget = self.widget(name)
            if not widget:
                widget = bumblebee.output.Widget(name=name)
                widgets.append(widget)
                widget.full_text(interface)

            widget_rx = self.widget(rxname)
            widget_tx = self.widget(txname)
            if not widget_rx:
                widget_rx = bumblebee.output.Widget(name=rxname)
                widget_rx.set("theme.minwidth", "1000.00MB")
                widgets.append(widget_rx)
            if not widget_tx:
                widget_tx = bumblebee.output.Widget(name=txname)
                widget_tx.set("theme.minwidth", "1000.00MB")
                widgets.append(widget_tx)

            prev_rx = widget_rx.get("rx", 0)
            prev_tx = widget_tx.get("tx", 0)
            rxspeed = bumblebee.util.bytefmt(int(rx) - int(prev_rx))
            txspeed = bumblebee.util.bytefmt(int(tx) - int(prev_tx))

            widget_rx.full_text(rxspeed)
            widget_tx.full_text(txspeed)

            widget_rx.set("rx", rx)
            widget_tx.set("tx", tx)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
