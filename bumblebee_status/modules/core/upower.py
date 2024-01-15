# pylint: disable=C0111,R0903

"""Displays battery level for upower devices


Requirements:
    * dbus Python module
    * dbus-compatible power devices

Parameters:
    * cpu.warning : Warning threshold in % of power remaining (defaults to 20%)
    * cpu.critical: Critical threshold in % of power remaining (defaults to 10%)
"""

import core.module
import core.widget
import core.input

import util.format

import dbus


class Module(core.module.Module):
    def __init__(self, config, theme):
        widgets = []
        super().__init__(config, theme, widgets)

        self._bus = dbus.SystemBus()
        self._proxy = self._bus.get_object(
            "org.freedesktop.UPower", "/org/freedesktop/UPower"
        )
        self._manager = dbus.Interface(self._proxy, "org.freedesktop.UPower")

        self._update_widgets(widgets)

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="gnome-system-monitor"
        )

    def update(self):
        self._update_widgets(self.widgets())

    def _update_widgets(self, widgets):
        self.clear_widgets()

        for dev in self._manager.EnumerateDevices():
            proxy = self._bus.get_object("org.freedesktop.UPower", dev)
            props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")

            try:
                name = props.Get("org.freedesktop.UPower.Device", "Model")
                perc = props.Get("org.freedesktop.UPower.Device", "Percentage")
                widget = self.widget(name)
                if not widget:
                    widget = self.add_widget(name=name)
                    widget.full_text("{} {:.0f}%".format(name, perc))
                    widget.set("percentage", float(perc))
            except Exception as e:
                continue

    def state(self, widget):
        perc = widget.get("percentage", 0.0)
        if perc < float(self.parameter("critical", 10)):
            return ["critical"]
        if perc < float(self.parameter("warning", 20)):
            return ["warning"]
        return []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
