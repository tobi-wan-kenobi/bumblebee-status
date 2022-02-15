# pylint: disable=C0111,R0903

"""Displays the name, IP address(es) and status of each available network interface.

Requires the following python module:
    * netifaces

Requires the following executable:
    * iw
    * (until and including 2.0.5: iwgetid)

Parameters:
    * nic.exclude: Comma-separated list of interface prefixes (supporting regular expressions) to exclude (defaults to 'lo,virbr,docker,vboxnet,veth,br,.*:avahi')
    * nic.include: Comma-separated list of interfaces to include
    * nic.states: Comma-separated list of states to show (prefix with '^' to invert - i.e. ^down -> show all devices that are not in state down)
    * nic.format: Format string (defaults to '{intf} {state} {ip} {ssid} {strength}')
    * nic.strength_warning: Integer to set the threshold for warning state (defaults to 50)
    * nic.strength_critical: Integer to set the threshold for critical state (defaults to 30)
"""

import re
import shutil
import netifaces
import subprocess

import core.module
import core.decorators
import util.cli
import util.format


class Module(core.module.Module):
    @core.decorators.every(seconds=5)
    def __init__(self, config, theme):
        widgets = []
        super().__init__(config, theme, widgets)
        self._exclude = util.format.aslist(
            self.parameter("exclude", "lo,virbr,docker,vboxnet,veth,br,.*:avahi")
        )
        self._include = util.format.aslist(self.parameter("include", ""))

        self._states = {"include": [], "exclude": []}
        for state in tuple(
            filter(len, util.format.aslist(self.parameter("states", "")))
        ):
            if state[0] == "^":
                self._states["exclude"].append(state[1:])
            else:
                self._states["include"].append(state)
        self._format = self.parameter("format", "{intf} {state} {ip} {ssid} {strength}")

        self._strength_threshold_critical = self.parameter("strength_critical", 30)
        self._strength_threshold_warning = self.parameter("strength_warning", 50)

        # Limits for the accepted dBm values of wifi strength
        self.__strength_dbm_lower_bound = -110
        self.__strength_dbm_upper_bound = -30

        self.iw = shutil.which("iw")
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

        # "strength" is none if interface type is not wlan
        strength = widget.get("strength")
        if self._iswlan(intf) and strength:
            if strength < self._strength_threshold_critical:
                states.append("critical")
            elif strength < self._strength_threshold_warning:
                states.append("warning")

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

    def _excluded(self, intf):
        for e in self._exclude:
            if re.match(e, intf):
                return True
        return False

    def _update_widgets(self, widgets):
        self.clear_widgets()
        interfaces = []
        for i in netifaces.interfaces():
            if not self._excluded(i):
                interfaces.append(i)
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

            strength_dbm = self.get_strength_dbm(intf)
            strength_percent = self.convert_strength_dbm_percent(strength_dbm)

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
                        strength=str(strength_percent) + "%" if strength_percent else "",
                        ssid=self.get_ssid(intf),
                    ).split()
                )
            )
            widget.set("intf", intf)
            widget.set("state", state)
            widget.set("strength", strength_percent)

    def get_ssid(self, intf):
        if not self._iswlan(intf) or self._istunnel(intf) or not self.iw:
            return ""

        iw_info = util.cli.execute("{} dev {} info".format(self.iw, intf))
        for line in iw_info.split("\n"):
            match = re.match(r"^\s+ssid\s(.+)$", line)
            if match:
                return match.group(1)

        return ""

    def get_strength_dbm(self, intf):
        if not self._iswlan(intf) or self._istunnel(intf) or not self.iw:
            return None

        with open("/proc/net/wireless", "r") as file:
            for line in file:
                if intf in line:
                    # Remove trailing . by slicing it off ;)
                    strength_dbm = line.split()[3][:-1]
                    return util.format.asint(strength_dbm,
                                minimum=self.__strength_dbm_lower_bound,
                                maximum=self.__strength_dbm_upper_bound)

        return None

    def convert_strength_dbm_percent(self, signal):
        return int(100 * ((signal + 100) / 70.0)) if signal else None


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
