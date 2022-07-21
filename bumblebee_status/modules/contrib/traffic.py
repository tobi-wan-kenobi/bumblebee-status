# pylint: disable=C0111,R0903

"""Displays network IO for interfaces.

Parameters:
    * traffic.exclude: Comma-separated list of interface prefixes to exclude (defaults to 'lo,virbr,docker,vboxnet,veth')
    * traffic.states: Comma-separated list of states to show (prefix with '^' to invert - i.e. ^down -> show all devices that are not in state down)
    * traffic.showname: If set to False, hide network interface name (defaults to True)
    * traffic.format: Format string for download/upload speeds.
      Defaults to '{:.2f}'
    * traffic.graphlen: Graph length in seconds. Positive even integer. Each
      char shows 2 seconds. If set, enables up/down traffic
      graphs

contributed by `meain <https://github.com/meain>`_ - many thanks!
"""

import re
import time
import psutil
import logging
import netifaces

import core.module

import util.format
import util.graph


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self._exclude = tuple(
            filter(
                len,
                util.format.aslist(
                    self.parameter("exclude", "lo,virbr,docker,vboxnet,veth")
                ),
            )
        )
        self._status = ""

        self._showname = util.format.asbool(self.parameter("showname", True))
        self._format = self.parameter("format", "{:.2f}")
        self._prev = {}
        self._states = {}
        self._lastcheck = 0
        self._states["include"] = []
        self._states["exclude"] = []
        for state in tuple(
            filter(len, util.format.aslist(self.parameter("states", "")))
        ):
            if state[0] == "^":
                self._states["exclude"].append(state[1:])
            else:
                self._states["include"].append(state)
        self._graphlen = int(self.parameter("graphlen", 0))
        if self._graphlen > 0:
            self._graphdata = {}
        self._first_run = True
        self._update_widgets()

    def state(self, widget):
        if "traffic.rx" in widget.name:
            return "rx"
        if "traffic.tx" in widget.name:
            return "tx"
        return self._status

    def update(self):
        try:
            self._update_widgets()
        except Exception as e:
            logging.exception(e)

    def create_widget(self, name, txt=None, attributes={}):
        widget = self.add_widget(name=name, full_text=txt)

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

    def get_minwidth_str(self):
        """
            computes theme.minwidth string
            based on traffic.format and traffic.graphlen parameters
        """
        minwidth_str = ""
        if self._graphlen > 0:
            graph_len = int(self._graphlen / 2)
            graph_prefix = "0" * graph_len
            minwidth_str += graph_prefix
        minwidth_str += "1000"
        try:
            length = int(re.match(r"{:\.(\d+)f}", self._format).group(1))
            if length > 0:
                minwidth_str += "." + "0" * length
        except AttributeError:
            # return default value
            return "1000.00KiB/s"
        finally:
            minwidth_str += "KiB/s"
        return minwidth_str

    def _update_widgets(self):
        interfaces = [
            i for i in netifaces.interfaces() if not i.startswith(self._exclude)
        ]

        self.clear_widgets()

        counters = psutil.net_io_counters(pernic=True)
        now = time.time()
        timediff = now - (self._lastcheck if self._lastcheck else now)
        if timediff <= 0:
            timediff = 1
        self._lastcheck = now
        for interface in interfaces:
            if self._graphlen > 0:
                if interface not in self._graphdata:
                    self._graphdata[interface] = {
                        "rx": [0] * self._graphlen,
                        "tx": [0] * self._graphlen,
                    }
            if not interface:
                interface = "lo"
            state = "down"
            if len(self.get_addresses(interface)) > 0:
                state = "up"
            elif util.format.asbool(self.parameter("hide_down", True)):
                continue

            if len(self._states["exclude"]) > 0 and state in self._states["exclude"]:
                continue
            if (
                len(self._states["include"]) > 0
                and state not in self._states["include"]
            ):
                continue

            data = {
                "rx": counters[interface].bytes_recv,
                "tx": counters[interface].bytes_sent,
            }

            name = "traffic-{}".format(interface)

            if self._showname:
                self.create_widget(name, interface)

            for direction in ["rx", "tx"]:
                name = "traffic.{}-{}".format(direction, interface)
                widget = self.create_widget(
                    name, attributes={"theme.minwidth": self.get_minwidth_str()},
                )
                prev = self._prev.get(name, 0)
                bspeed = (int(data[direction]) - int(prev)) / timediff
                speed = util.format.byte(bspeed, self._format)
                txtspeed = "{0}/s".format(speed)
                if self._graphlen > 0:
                    # skip first value returned by psutil, because it is
                    # giant and ruins the grapth ratio until it gets pushed
                    # out of saved list
                    if self._first_run is True:
                        self._first_run = False
                    else:
                        self._graphdata[interface][direction] = self._graphdata[
                            interface
                        ][direction][1:]
                        self._graphdata[interface][direction].append(bspeed)
                    txtspeed = "{}{}".format(
                        util.graph.braille(self._graphdata[interface][direction]),
                        txtspeed,
                    )
                widget.full_text(txtspeed)
                self._prev[name] = data[direction]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
