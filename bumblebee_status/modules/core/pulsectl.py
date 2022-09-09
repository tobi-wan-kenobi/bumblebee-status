# pylint: disable=C0111,R0903

import pulsectl

import core.module
import core.widget
import core.input
import core.event

import util.format

class Module(core.module.Module):
    def __init__(self, config, theme, type):
        super().__init__(config, theme, core.widget.Widget(self.display))
        self.background = True

        self.__type = type
        self.__volume = "n/a"
        self.__muted = False

        self.__change = util.format.asint(
            self.parameter("percent_change", "2%").strip("%"), 0, 100
        )

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

        self.process(None)

    def display(self, _):
        return f"{int(self.__volume*100)}%"

    def toggle_mute(self, _):
        with pulsectl.Pulse(self.id + "vol") as pulse:
            dev = pulse.sink_list()[0] if self.__type == "sink" else pulse.source_list()[1]
            pulse.mute(dev, not self.__muted)

    def change_volume(self, amount):
        with pulsectl.Pulse(self.id + "vol") as pulse:
            dev = pulse.sink_list()[0] if self.__type == "sink" else pulse.source_list()[1]
            vol = dev.volume
            vol.value_flat += amount
            pulse.volume_set(dev, vol)

    def increase_volume(self, _):
        self.change_volume(self.__change/100.0)

    def decrease_volume(self, _):
        self.change_volume(-self.__change/100.0)

    def process(self, _):
        with pulsectl.Pulse(self.id + "proc") as pulse:
            dev = pulse.sink_list()[0] if self.__type == "sink" else pulse.source_list()[1]
            self.__volume = dev.volume.value_flat
            self.__muted = dev.mute
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
