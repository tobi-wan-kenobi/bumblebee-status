# pylint: disable=C0111,R0903

""" Displays the VPN profile that is currently in use.

    Left click opens a popup menu that lists all available VPN profiles and allows to establish
    a VPN connection using that profile.

    Prerequisites:
         * tk python library (usually python-tk or python3-tk, depending on your distribution)
         * nmcli needs to be installed and configured properly.
           To quickly test, whether nmcli is working correctly, type "nmcli -g NAME,TYPE,DEVICE con" which
           lists all the connection profiles that are configured. Make sure that your VPN profile is in that list!

           e.g: to import a openvpn profile via nmcli:
               sudo nmcli connection import type openvpn file </path/to/your/openvpn/profile.ovpn>
"""

import logging
import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.popup_v2
import functools

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.vpn_status)
        )

        self._connected_vpn_profile = None
        self._selected_vpn_profile = None

        res = bumblebee.util.execute("nmcli -g NAME,TYPE c")
        lines = res.splitlines()

        self._vpn_profiles = []
        for line in lines:
            info = line.split(':')
            try:
                if self._isvpn(info[1]):
                    self._vpn_profiles.append(info[0])
            except:
                pass

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd=self.popup)

    def _isvpn(self, connection_type):
        return connection_type in ["vpn", "wireguard"]

    def update(self, widgets):
        try:
            res = bumblebee.util.execute("nmcli -g NAME,TYPE,DEVICE con")
            lines = res.splitlines()
            self._connected_vpn_profile = None
            for line in lines:
                info = line.split(':')
                if self._isvpn(info[1]) and info[2] != "":
                    self._connected_vpn_profile = info[0]

        except Exception as e:
            logging.exception("Couldn't get VPN status")
            self._connected_vpn_profile = None

    def vpn_status(self, widget):
        if self._connected_vpn_profile is None:
            return "off"
        return self._connected_vpn_profile

    def _on_vpn_disconnect(self):
        try:
            bumblebee.util.execute("nmcli c down \"{vpn}\""
                                   .format(vpn=self._connected_vpn_profile))
            self._connected_vpn_profile = None
        except Exception as e:
            logging.exception("Couldn't disconnect VPN connection")

    def _on_vpn_connect(self, name):
        self._selected_vpn_profile = name

        try:
            bumblebee.util.execute("nmcli c up \"{vpn}\""
                                   .format(vpn=self._selected_vpn_profile))
            self._connected_vpn_profile = name
        except Exception as e:
            logging.exception("Couldn't establish VPN connection")
            self._connected_vpn_profile = None

    def popup(self, widget):
        menu = bumblebee.popup_v2.PopupMenu()

        if self._connected_vpn_profile is not None:
            menu.add_menuitem("Disconnect", callback=self._on_vpn_disconnect)
        for vpn_profile in self._vpn_profiles:
            if self._connected_vpn_profile is not None and self._connected_vpn_profile == vpn_profile:
                continue
            menu.add_menuitem(vpn_profile, callback=functools.partial(self._on_vpn_connect, vpn_profile))
        menu.show(widget)

    def state(self, widget):
        return []
