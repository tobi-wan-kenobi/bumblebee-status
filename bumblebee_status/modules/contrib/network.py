"""
A module to show currently active network connection (ethernet or wifi)
and connection strength.
"""


import util.cli
import util.format

import core.module
import core.widget


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.network))
        self._is_wireless = True
        self._interface = None
        self._message = None
        self.__signal = -110

    def network(self, widgets):
        # run ip route command, tokenize output
        cmd = "ip route get 8.8.8.8"
        std_out = util.cli.execute(cmd)
        route_str = " ".join(std_out.split())
        route_tokens = route_str.split(" ")

        # Attempt to extract a valid network interface device
        try:
            self._interface = route_tokens[route_tokens.index("dev") + 1]
        except ValueError:
            self._interface = None

        # Check to see if the interface (if it exists) is wireless
        if self._interface:
            with open("/proc/net/wireless", "r") as f:
                self._is_wireless = self._interface in f.read()
        f.close()

        # setup message to send to the user
        if self._interface is None:
            self._message = "Not connected to a network"
        elif self._is_wireless:
            cmd = "iwgetid"
            iw_dat = util.cli.execute(cmd)
            has_ssid = "ESSID" in iw_dat
            ssid = iw_dat[iw_dat.index(":") + 2: -2] if has_ssid else "Unknown"

            # Get connection strength
            cmd = "iwconfig {}".format(self._interface)
            config_dat = " ".join(util.cli.execute(cmd).split())
            config_tokens = config_dat.replace("=", " ").split()
            strength = config_tokens[config_tokens.index("level") + 1]
            self.__signal = util.format.asint(strength, minimum=-110, maximum=-30)

            self._message = self.__generate_wireless_message(ssid, self.__signal)
        else:
            self._message = self._message

        return self._message


    def state(self, widget):
        if self.__signal < -65:
            return "warning"
        if self.__signal < -80:
            return "critical"
        return None


    def __generate_wireless_message(self, ssid, strength):
        computed_strength = 100 * ((strength + 100) / 70.0)
        if computed_strength < 30:
            return ssid + " poor"
        if computed_strength < 50:
            return ssid + " fair"
        if computed_strength < 75:
            return ssid + " good"

        return ssid + " excellent"

