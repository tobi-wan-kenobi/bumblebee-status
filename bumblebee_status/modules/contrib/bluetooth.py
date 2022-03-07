"""Displays bluetooth status (Bluez). Left mouse click launches manager app `blueman-manager`,
right click toggles bluetooth. Needs dbus-send to toggle bluetooth state.

Parameters:
    * bluetooth.device : the device to read state from (default is hci0)
    * bluetooth.manager : application to launch on click (blueman-manager)
    * bluetooth.dbus_destination : dbus destination (defaults to org.blueman.Mechanism)
    * bluetooth.dbus_destination_path : dbus destination path (defaults to /)
    * bluetooth.right_click_popup : use popup menu when right-clicked (defaults to True)

contributed by `brunosmmm <https://github.com/brunosmmm>`_ - many thanks!
"""


import os
import re
import logging

import core.module
import core.widget
import core.input

import util.cli
import util.format
import util.popup


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.status))

        device = self.parameter("device", "hci0")
        self.manager = self.parameter("manager", "blueman-manager")
        self._path = "/sys/class/bluetooth/{}".format(device)
        self._status = "Off"

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.manager)

        # determine whether to use pop-up menu or simply toggle the device on/off
        right_click_popup = util.format.asbool(
            self.parameter("right_click_popup", True)
        )

        if right_click_popup:
            core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.popup)
        else:
            core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self._toggle)

    def status(self, widget):
        """Get status."""
        return self._status

    def update(self):
        """Update current state."""
        if not os.path.exists(self._path):
            self._status = "?"
            return

        # search for whichever rfkill directory available
        try:
            dirnames = next(os.walk(self._path))[1]
            for dirname in dirnames:
                m = re.match(r"rfkill[0-9]+", dirname)
                if m is not None:
                    with open(os.path.join(self._path, dirname, "state"), "r") as f:
                        state = int(f.read())
                        if state == 1:
                            self._status = "On"
                        else:
                            self._status = "Off"
                    return

        except IOError:
            self._status = "?"

    def popup(self, widget):
        """Show a popup menu."""
        menu = util.popup.PopupMenu()
        if self._status == "On":
            menu.add_menuitem("Disable Bluetooth")
        elif self._status == "Off":
            menu.add_menuitem("Enable Bluetooth")
        else:
            return

        # show menu and get return code
        ret = menu.show(widget)
        if ret == 0:
            # first (and only) item selected.
            self._toggle()

    def _toggle(self, widget=None):
        """Toggle bluetooth state."""
        if self._status == "On":
            state = "false"
        else:
            state = "true"

        dst = self.parameter("dbus_destination", "org.blueman.Mechanism")
        dst_path = self.parameter("dbus_destination_path", "/")

        cmd = (
            "dbus-send --system --print-reply --dest={}"
            " {} org.blueman.Mechanism.SetRfkillState"
            " boolean:{}".format(dst, dst_path, state)
        )

        logging.debug("bt: toggling bluetooth")
        util.cli.execute(cmd, ignore_errors=True)

    def state(self, widget):
        """Get current state."""
        state = []

        if self._status == "?":
            state = ["unknown"]
        elif self._status == "On":
            state = ["ON"]
        else:
            state = ["OFF"]

        return state


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
