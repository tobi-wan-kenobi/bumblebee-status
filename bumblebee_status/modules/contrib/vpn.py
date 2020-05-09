# pylint: disable=C0111,R0903

""" Displays the VPN profile that is currently in use.

    Left click opens a popup menu that lists all available VPN profiles and allows to establish
    a VPN connection using that profile.

    Prerequisites:
         * tk python library (usually python-tk or python3-tk, depending on your distribution)
         * nmcli needs to be installed and configured properly.
           To quickly test, whether nmcli is working correctly, type 'nmcli -g NAME,TYPE,DEVICE con' which
           lists all the connection profiles that are configured. Make sure that your VPN profile is in that list!

           e.g: to import a openvpn profile via nmcli:
           `sudo nmcli connection import type openvpn file </path/to/your/openvpn/profile.ovpn>`

contributed by `bbernhard <https://github.com/bbernhard>`_ - many thanks!
"""

import logging
import functools

import core.module
import core.widget
import core.input

import util.cli
import util.popup


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.vpn_status))

        self.__connected_vpn_profile = None
        self.__selected_vpn_profile = None

        res = util.cli.execute("nmcli -g NAME,TYPE c")
        lines = res.splitlines()

        self.__vpn_profiles = []
        for line in lines:
            info = line.split(":")
            try:
                if self.__isvpn(info[1]):
                    self.__vpn_profiles.append(info[0])
            except:
                pass

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.popup)

    def __isvpn(self, connection_type):
        return connection_type in ["vpn", "wireguard"]

    def update(self):
        try:
            res = util.cli.execute("nmcli -g NAME,TYPE,DEVICE con")
            lines = res.splitlines()
            self.__connected_vpn_profile = None
            for line in lines:
                info = line.split(":")
                if self.__isvpn(info[1]) and info[2] != "":
                    self.__connected_vpn_profile = info[0]

        except Exception as e:
            logging.exception("Could not get VPN status")
            self.__connected_vpn_profile = None

    def vpn_status(self, widget):
        if self.__connected_vpn_profile is None:
            return "off"
        return self.__connected_vpn_profile

    def __on_vpndisconnect(self):
        try:
            util.cli.execute(
                "nmcli c down '{vpn}'".format(vpn=self.__connected_vpn_profile)
            )
            self.__connected_vpn_profile = None
        except Exception as e:
            logging.exception("Could not disconnect VPN connection")

    def __on_vpnconnect(self, name):
        self.__selected_vpn_profile = name

        try:
            util.cli.execute(
                "nmcli c up '{vpn}'".format(vpn=self.__selected_vpn_profile)
            )
            self.__connected_vpn_profile = name
        except Exception as e:
            logging.exception("Could not establish VPN connection")
            self.__connected_vpn_profile = None

    def popup(self, widget):
        menu = util.popup.menu()

        if self.__connected_vpn_profile is not None:
            menu.add_menuitem("Disconnect", callback=self.__on_vpndisconnect)
        for vpn_profile in self.__vpn_profiles:
            if (
                self.__connected_vpn_profile is not None
                and self.__connected_vpn_profile == vpn_profile
            ):
                continue
            menu.add_menuitem(
                vpn_profile,
                callback=functools.partial(self.__on_vpnconnect, vpn_profile),
            )
        menu.show(widget)

    def state(self, widget):
        return []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
