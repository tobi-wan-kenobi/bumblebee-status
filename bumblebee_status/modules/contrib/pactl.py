# pylint: disable=C0111,R0903

""" Displays the current default sink.

    Left click opens a popup menu that lists all available sinks and allows to change the default sink.

    Per default, this module uses the sink names returned by "pactl list sinks short"

    sample output of "pactl list sinks short":

    2	alsa_output.pci-0000_00_1f.3.analog-stereo	module-alsa-card.c	s16le 2ch 44100Hz	SUSPENDED
    3	alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo	module-alsa-card.c	s16le 2ch 44100Hz	SUSPENDE

    As "alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo" is not a particularly nice name, its possible to map the name to more a
    user friendly name. e.g to map "alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo" to the name "Headset", add the following
    bumblebee-status config entry: pactl.alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo=Headset

    The module also allows to specify individual (unicode) icons for all the sinks. e.g in order to use the icon 🎧 for the
    "alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo" sink, add the following bumblebee-status config entry:
    pactl.icon.alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo=🎧

    Requirements:
        * pulseaudio
        * pactl
"""

import logging
import functools

import core.module
import core.widget
import core.input

import util.cli
import util.popup


class Sink(object):
    def __init__(self, id, internal_name, friendly_name, icon):
        super().__init__()
        self.__id = id
        self.__internal_name = internal_name
        self.__friendly_name = friendly_name
        self.__icon = icon

    @property
    def id(self):
        return self.__id

    @property
    def internal_name(self):
        return self.__internal_name

    @property
    def friendly_name(self):
        return self.__friendly_name

    @property
    def icon(self):
        return self.__icon

    @property
    def display_name(self):
        display_name = (
            self.__icon + " " + self.__friendly_name
            if self.__icon != ""
            else self.__friendly_name
        )
        return display_name


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.default_sink))

        self.__default_sink = None

        res = util.cli.execute("pactl list sinks short")
        lines = res.splitlines()

        self.__sinks = []
        for line in lines:
            info = line.split("\t")
            try:
                friendly_name = self.parameter(info[1], info[1])
                icon = self.parameter("icon." + info[1], "")
                self.__sinks.append(Sink(info[0], info[1], friendly_name, icon))
            except:
                logging.exception("Couldn't parse sink")
                pass

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.popup)

    def __sink(self, internal_sink_name):
        for sink in self.__sinks:
            logging.info(sink.internal_name)
            if internal_sink_name == sink.internal_name:
                return sink
        return None

    def update(self):
        try:
            res = util.cli.execute("pactl info")
            lines = res.splitlines()
            self.__default_sink = None
            for line in lines:
                if not line.startswith("Default Sink:"):
                    continue
                internal_sink_name = line.replace("Default Sink: ", "")
                self.__default_sink = self.__sink(internal_sink_name)
                break
        except Exception as e:
            logging.exception("Could not get pactl info")
            self.__default_sink = None

    def default_sink(self, widget):
        if self.__default_sink is None:
            return "unknown"
        return self.__default_sink.display_name

    def __on_sink_selected(self, sink):
        try:
            util.cli.execute("pactl set-default-sink {}".format(sink.id))
            self.__default_sink = sink
        except Exception as e:
            logging.exception("Couldn't set default sink")

    def popup(self, widget):
        menu = util.popup.menu()

        for sink in self.__sinks:
            menu.add_menuitem(
                sink.friendly_name,
                callback=functools.partial(self.__on_sink_selected, sink),
            )
        menu.show(widget)

    def state(self, widget):
        return []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
