# pylint: disable=C0111,R0903

"""Displays network IO for interfaces.

Parameters:
    * traffic.exclude: Comma-separated list of interface prefixes to exclude (defaults to "lo,virbr,docker,vboxnet,veth")
    * traffic.states: Comma-separated list of states to show (prefix with "^" to invert - i.e. ^down -> show all devices that are not in state down)
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
        self._status = ""

        self._prev = {}
        self._states = {}
        self._states["include"] = []
        self._states["exclude"] = []
        for state in tuple(filter(len, self.parameter("states", "").split(","))):
            if state[0] == "^":
                self._states["exclude"].append(state[1:])
            else:
                self._states["include"].append(state)
        self._update_widgets(widgets)

    def state(self, widget):
        if "traffic.rx" in widget.name:
            return "rx"
        if "traffic.tx" in widget.name:
            return "tx"
        return self._status

    def update(self, widgets):
        self._update_widgets(widgets)

    def create_widget(self, widgets, name, txt=None, attributes={}):
        widget = bumblebee.output.Widget(name=name)
        widget.full_text(txt)
        widgets.append(widget)

        for key in attributes:
            widget.set(key, attributes[key])

        return widget

    def get_addresses(self, intf):
        retval = []
        try:
            for ip in netifaces.ifaddresses(intf).get(netifaces.AF_INET, []):
                if ip.get("addr", "") != "":
                    retval.append(ip.get("addr"))
        except Exception:
            return []
        return retval

    def _update_widgets(self, widgets):
        interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]

        del widgets[:]

        counters = psutil.net_io_counters(pernic=True)
        for interface in interfaces:
            if not interface: interface = "lo"
            state = "down"
            if len(self.get_addresses(interface)) > 0:
                state = "up"

            if len(self._states["exclude"]) > 0 and state in self._states["exclude"]: continue
            if len(self._states["include"]) > 0 and state not in self._states["include"]: continue

            data = {
                "rx": counters[interface].bytes_recv,
                "tx": counters[interface].bytes_sent,
            }

            name = "traffic-{}".format(interface)

            self.create_widget(widgets, name, interface)

            for direction in ["rx", "tx"]:
                name = "traffic.{}-{}".format(direction, interface)
                widget = self.create_widget(widgets, name, attributes={"theme.minwidth": "1000.00MB"})
                prev = self._prev.get(name, 0)
                speed = bumblebee.util.bytefmt(int(data[direction]) - int(prev))
                widget.full_text(speed)
                self._prev[name] = data[direction]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
