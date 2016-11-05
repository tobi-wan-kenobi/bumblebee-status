import re
import shlex
import subprocess

import bumblebee.module
import bumblebee.util

def usage():
    module = __name__.split(".")[-1]
    if module == "pasource":
        return "pasource"
    if module == "pasink":
        return "pasink"
    return "pulseaudio"

def notes():
    return "Invokes 'pactl' to retrieve information."
    pass

def description():
    module = __name__.split(".")[-1]
    if module == "pasink":
        return "Shows volume and mute status of the default PulseAudio Sink."
    if module == "pasource":
        return "Shows volume and mute status of the default PulseAudio Source."
    return "See 'pasource'."

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)

        self._module = self.__module__.split(".")[-1]
        self._left = 0
        self._right = 0
        self._mono = 0
        self._mute = False
        channel = "sink" if self._module == "pasink" else "source"

# TODO
#        output.add_callback(module=self.__module__, button=3,
#            cmd="pavucontrol")
#        output.add_callback(module=self.__module__, button=1,
#            cmd="pactl set-{}-mute @DEFAULT_{}@ toggle".format(channel, channel.upper()))
#        output.add_callback(module=self.__module__, button=4,
#            cmd="pactl set-{}-volume @DEFAULT_{}@ +2%".format(channel, channel.upper()))
#        output.add_callback(module=self.__module__, button=5,
#            cmd="pactl set-{}-volume @DEFAULT_{}@ -2%".format(channel, channel.upper()))

    def widgets(self):
        res = subprocess.check_output(shlex.split("pactl info"))
        channel = "sinks" if self._module == "pasink" else "sources"
        name = None
        for line in res.split("\n"):
            if line.startswith("Default Sink: ") and channel == "sinks":
                name = line[14:]
            if line.startswith("Default Source: ") and channel == "sources":
                name = line[16:]
        
        res = subprocess.check_output(shlex.split("pactl list {}".format(channel)))

        found = False
        for line in res.split("\n"):
            if "Name:" in line and found == True:
                break
            if name in line:
                found = True
            if "Mute:" in line and found == True:
                self._mute = False if " no" in line.lower() else True

            if "Volume:" in line and found == True:
                m = None
                if "mono" in line:
                    m = re.search(r'mono:.*\s*\/\s*(\d+)%', line)
                else:
                    m = re.search(r'left:.*\s*\/\s*(\d+)%.*right:.*\s*\/\s*(\d+)%', line)
                if not m: continue

                if "mono" in line:
                    self._mono = m.group(1)
                else:
                    self._left = m.group(1)
                    self._right = m.group(2)
        result = ""
        if self._mono > 0:
            result = "{}%".format(self._mono)
        elif self._left == self._right:
            result = "{}%".format(self._left)
        else:
            result="{}%/{}%".format(self._left, self._right)
        return bumblebee.output.Widget(self, result)

    def state(self, widget):
        return "muted" if self._mute is True else "unmuted"

    def warning(self, widget):
        return self._mute

    def critical(self, widget):
        return False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
