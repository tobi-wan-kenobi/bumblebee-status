# pylint: disable=C0111,R0903

"""Displays volume and mute status and controls for PulseAudio devices. Use wheel up and down to change volume, left click mutes, right click opens pavucontrol.

**Please prefer this module over the "pulseaudio" module, which will eventually be deprecated

Aliases: pulseout (for outputs, such as headsets, speakers), pulsein (for microphones)

NOTE: Do **not** use this module directly, but rather use either pulseout or pulsein!
NOTE2: For the parameter names below, please also use pulseout or pulsein, instead of pulsectl

Parameters:
    * pulsectl.autostart: If set to 'true' (default is 'false'), automatically starts the pulsectl daemon if it is not running
    * pulsectl.percent_change: How much to change volume by when scrolling on the module (default is 2%)
    * pulsectl.limit: Upper limit for setting the volume (default is 0%, which means 'no limit')
    * pulsectl.showbars: 'true' for showing volume bars, requires --markup=pango;
      'false' for not showing volume bars (default)
    * pulsectl.showdevicename: If set to 'true' (default is 'false'), the currently selected default device is shown.
      Per default, the sink/source name returned by "pactl list sinks short" is used as display name.

      As this name is usually not particularly nice (e.g "alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo"),
      its possible to map the name to more a user friendly name.

      e.g to map "alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo" to the name "Headset", add the following
      bumblebee-status config entry: pulsectl.alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo=Headset

      Furthermore its possible to specify individual (unicode) icons for all sinks/sources. e.g in order to use the icon 🎧 for the
      "alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo" sink, add the following bumblebee-status config entry:
      pulsectl.icon.alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo=🎧
    * Per default a left mouse button click mutes/unmutes the device. In case you want to open a dropdown menu to change the current
      default device add the following config entry to your bumblebee-status config: pulsectl.left-click=select_default_device_popup

Requires the following Python module:
    * pulsectl
"""

import pulsectl

import core.module
import core.widget
import core.input
import core.event

import util.cli
import util.graph
import util.format

class Module(core.module.Module):
    def __init__(self, config, theme, type):
        super().__init__(config, theme, core.widget.Widget(self.display))
        self.background = True

        self.__type = type
        self.__volume = "n/a"
        self.__devicename = "n/a"
        self.__muted = False
        self.__showbars = util.format.asbool(self.parameter("showbars", False))
        self.__show_device_name = util.format.asbool(
            self.parameter("showdevicename", False)
        )

        self.__change = util.format.asint(
            self.parameter("percent_change", "2%").strip("%"), 0, 100
        )
        self.__limit = util.format.asint(self.parameter("limit", "0%").strip("%"), 0)

        events = [
            {
                "type": "mute",
                "action": self.toggle_mute,
                "button": core.input.LEFT_MOUSE
            },
            {
                "type": "volume",
                "action": self.increase_volume,
                "button": core.input.WHEEL_UP,
            },
            {
                "type": "volume",
                "action": self.decrease_volume,
                "button": core.input.WHEEL_DOWN,
            },
        ]

        for event in events:
            core.input.register(self, button=event["button"], cmd=event["action"])

        if util.format.asbool(self.parameter("autostart", False)):
            util.cli.execute("pulseaudio --start", ignore_errors=True)

        self.process(None)

    def display(self, _):
        res = f"{int(self.__volume*100)}%"
        if self.__showbars:
            res = f"{res} {util.graph.hbar(self.__volume*100)}"

        if self.__show_device_name:
            friendly_name = self.parameter(self.__devicename, self.__devicename)
            icon = self.parameter("icon." + self.__devicename, "")
            res = (
                icon + " " + friendly_name + " | " + res
                if icon != ""
                else friendly_name + " | " + res
            )
        return res

    def toggle_mute(self, _):
        with pulsectl.Pulse(self.id + "vol") as pulse:
            dev = self.get_device(pulse)
            pulse.mute(dev, not self.__muted)

    def change_volume(self, amount):
        with pulsectl.Pulse(self.id + "vol") as pulse:
            dev = self.get_device(pulse)
            vol = dev.volume
            vol.value_flat += amount
            if self.__limit > 0 and vol.value_flat > self.__limit/100:
                vol.value_flat = self.__limit/100
            pulse.volume_set(dev, vol)

    def increase_volume(self, _):
        self.change_volume(self.__change/100.0)

    def decrease_volume(self, _):
        self.change_volume(-self.__change/100.0)

    def get_device(self, pulse):
        devs = pulse.sink_list() if self.__type == "sink" else pulse.source_list()
        default = pulse.server_info().default_sink_name if self.__type == "sink" else pulse.server_info().default_source_name

        for dev in devs:
            if dev.name == default:
                return dev
        return devs[0] # fallback



    def process(self, _):
        with pulsectl.Pulse(self.id + "proc") as pulse:
            dev = self.get_device(pulse)
            self.__volume = dev.volume.value_flat
            self.__muted = dev.mute
            self.__devicename = dev.name
        core.event.trigger("update", [self.id], redraw_only=True)
        core.event.trigger("draw")

    def update(self):
        with pulsectl.Pulse(self.id) as pulse:
            pulse.event_mask_set(self.__type)
            pulse.event_callback_set(self.process)
            pulse.event_listen()

    def state(self, _):
        if self.__muted:
            return ["warning", "muted"]
        return ["unmuted"]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
