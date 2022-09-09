# pylint: disable=C0111,R0903

import pulsectl

import core.module
import core.widget
import core.decorators
import core.input
import core.event

class Module(core.module.Module):
    def __init__(self, config, theme, type):
        super().__init__(config, theme, core.widget.Widget(self.display))
        self.background = True

        self.__type = type
        self.__volume = "n/a"
        self.__muted = False

        self.process(None)

    def display(self, _):
        return f"{int(self.__volume*100)}%"

    def process(self, _):
        with pulsectl.Pulse(self.id + "proc") as pulse:
            dev = pulse.sink_list()[0] if self.__type == "sink" else pulse.source_list()[0]
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
