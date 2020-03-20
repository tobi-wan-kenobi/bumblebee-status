"""Displays bluetooth status. Left mouse click launches manager app,
right click toggles bluetooth. Needs dbus-send to toggle bluetooth state and
python-dbus to count the number of connections

Parameters:
    * bluetooth.manager : application to launch on click (blueman-manager)
"""


import os
import re
import subprocess
import dbus
import dbus.mainloop.glib
import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util
import bumblebee.popup
import logging


class Module(bumblebee.engine.Module):
    """Bluetooth module."""

    def __init__(self, engine, config):
        """Initialize."""
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(
                                         full_text=self.status))

        self.manager = self.parameter("manager", "blueman-manager")
        self._status = "Off"
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self._bus = dbus.SystemBus()

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd=self.manager)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
                                           cmd=self._toggle)

    def status(self, widget):
        """Get status."""
        return self._status

    def update(self, widgets):
        """Update current state."""
        state = len(subprocess.run(['bluetoothctl', 'list'], stdout=subprocess.PIPE).stdout)
        if state > 0:
            connected_devices = self.get_connected_devices()
            self._status = "On - {}".format(connected_devices)
        else:
            self._status = "Off"
            adapters_cmd = 'rfkill list | grep Bluetooth'
            if not len(subprocess.run(adapters_cmd, shell=True, stdout=subprocess.PIPE).stdout):
                self._status = "No Adapter Found"
        return

    def manager(self, widget):
        """Launch manager."""
        bumblebee.util.execute(self.manager)

    def _toggle(self, widget=None):
        """Toggle bluetooth state."""
        if "On" in self._status:
            state = "false"
        else:
            state = "true"

        cmd = "dbus-send --system --print-reply --dest=org.blueman.Mechanism /org/blueman/mechanism org.blueman.Mechanism.SetRfkillState boolean:%s" % state 

        logging.debug('bt: toggling bluetooth')
        bumblebee.util.execute(cmd)

    def state(self, widget):
        """Get current state."""
        state = []

        if self._status == "No Adapter Found":
            state.append("critical")
        elif self._status == "On - 0":
            state.append("warning")
        elif "On" in self._status and not(self._status == "On - 0"):
            state.append("ON")
        else:
            state.append("critical")
        return state

    def get_connected_devices(self):
        devices = 0
        objects = dbus.Interface(
            self._bus.get_object("org.bluez", "/"),
            "org.freedesktop.DBus.ObjectManager"
        ).GetManagedObjects()
        for path, interfaces in objects.items():
            if "org.bluez.Device1" in interfaces:
                if dbus.Interface(
                    self._bus.get_object("org.bluez", path),
                    "org.freedesktop.DBus.Properties"
                ).Get(
                    "org.bluez.Device1", "Connected"
                ):
                    devices += 1
        return devices
