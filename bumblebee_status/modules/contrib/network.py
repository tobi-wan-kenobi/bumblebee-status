"""
A module to show currently active network connection (ethernet or wifi)
and connection strength.
"""


import util.cli
import util.format

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    @core.decorators.every(seconds=10)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.network))
        self.__is_wireless = True
        self.__interface = None
        self.__message = None
        self.__signal = -110

        # Set up event handler for left mouse click
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd="nm-connection-editor")

    def network(self, widgets):
        # run ip route command, tokenize output
        cmd = "ip route get 8.8.8.8"
        std_out = util.cli.execute(cmd)
        route_str = " ".join(std_out.split())
        route_tokens = route_str.split(" ")

        # Attempt to extract a valid network interface device
        try:
             self.__interface = route_tokens[route_tokens.index("dev") + 1]  
        except ValueError:
            self.__interface = None

        # Check to see if the interface (if it exists) is wireless
        if self.__interface:
            with open("/proc/net/wireless", "r") as f:
                self.__is_wireless = self.__interface in f.read()
        f.close()

        # setup message to send to the user
        if self.__interface is None:
            self.__message = " No connection"
        elif self.__is_wireless:
            cmd = "iwgetid"
            iw_dat = util.cli.execute(cmd)
            has_ssid = "ESSID" in iw_dat
            ssid = iw_dat[iw_dat.index(":") + 2: -2] if has_ssid else "Unknown"

            # Get connection strength
            cmd = "iwconfig {}".format(self.__interface)
            config_dat = " ".join(util.cli.execute(cmd).split())
            config_tokens = config_dat.replace("=", " ").split()
            strength = config_tokens[config_tokens.index("level") + 1]
            self.__signal = util.format.asint(strength, minimum=-110, maximum=-30)

            self.__message = self.__generate_wireles_message(ssid, self.__signal)
        else:
            self.__signal = -30
            self.__message = " Ethernet" 

        return self.__message


    def state(self, widget):
        if self.__signal < -80:
            return "critical"
        if self.__signal < -65:
            return "warning"

        return None


    def __generate_wireles_message(self, ssid, strength):
        computed_strength = 100 * ((strength + 100) / 70.0)
        return " {} {}%".format(ssid, int(computed_strength))



