# pylint: disable=C0111,R0903

"""Displays the name, IP address(es) and status of each available network interface.

Requires the following python module:
    * netifaces

Parameters:
    * nic.exclude: Comma-separated list of interface prefixes to exclude (defaults to 'lo,virbr,docker,vboxnet,veth,br')
    * nic.include: Comma-separated list of interfaces to include
    * nic.states: Comma-separated list of states to show (prefix with '^' to invert - i.e. ^down -> show all devices that are not in state down)
    * nic.format: Format string (defaults to '{intf} {state} {ip} {ssid}')
"""

import shutil
import netifaces
import subprocess

import core.module
import core.decorators
import util.cli
import util.format


class Module(core.module.Module):
    @core.decorators.every(seconds=10)
    def __init__(self, config, theme):
        widgets = []
        super().__init__(config, theme, widgets)
        self._exclude = tuple(
            filter(
                len,
                self.parameter("exclude", "lo,virbr,docker,vboxnet,veth,br").split(","),
            )
        )
        self._include = self.parameter("include", "").split(",")

        self._states = {"include": [], "exclude": []}
        for state in tuple(
            filter(len, util.format.aslist(self.parameter("states", "")))
        ):
            if state[0] == "^":
                self._states["exclude"].append(state[1:])
            else:
                self._states["include"].append(state)
        self._format = self.parameter("format", "{intf} {state} {ip} {ssid}")
        self.iwgetid = shutil.which("iwgetid")
        self._update_widgets(widgets)

    def update(self):
        self._update_widgets(self.widgets())

    def state(self, widget):
        states = []

        if widget.get("state") == "down":
            states.append("critical")
        elif widget.get("state") != "up":
            states.append("warning")

        intf = widget.get("intf")
        iftype = "wireless" if self._iswlan(intf) else "wired"
        iftype = "tunnel" if self._istunnel(intf) else iftype

        states.append("{}-{}".format(iftype, widget.get("state")))

        return states

    def _iswlan(self, intf):
        # wifi, wlan, wlp, seems to work for me
        if intf.startswith("w"):
            return True
        return False

    def _istunnel(self, intf):
        return intf.startswith("tun") or intf.startswith("wg")

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
        self.clear_widgets()
        interfaces = [
            i for i in netifaces.interfaces() if not i.startswith(self._exclude)
        ]
        interfaces.extend([i for i in netifaces.interfaces() if i in self._include])

        for intf in interfaces:
            addr = []
            state = "down"
            for ip in self.get_addresses(intf):
                addr.append(ip)
                state = "up"

            if len(self._states["exclude"]) > 0 and state in self._states["exclude"]:
                continue
            if (
                len(self._states["include"]) > 0
                and state not in self._states["include"]
            ):
                continue

            widget = self.widget(intf)
            if not widget:
                widget = self.add_widget(name=intf)
            # join/split is used to get rid of multiple whitespaces (in case SSID is not available, for instance
            widget.full_text(
                " ".join(
                    self._format.format(
                        ip=", ".join(addr),
                        intf=intf,
                        state=state,
                        ssid=self.get_ssid(intf),
                    ).split()
                )
            )
            widget.set("intf", intf)
            widget.set("state", state)

    def get_ssid(self, intf):
        if self._iswlan(intf) and not self._istunnel(intf) and self.iwgetid:
            return util.cli.execute(
                "{} -r {}".format(self.iwgetid, intf), ignore_errors=True
            )
        return ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
