import bumblebee.module
import re
import sys
import subprocess

def description():
    return "Shows all connected screens"

def parameters():
    return [
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._state = "off"

    def widgets(self):
        process = subprocess.Popen([ "xrandr", "-q" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        widgets = []

        # TODO: sort by position
        for line in output.split("\n"):
            if not " connected" in line:
                continue
            screen = line.split(" ", 2)[0]
            m = re.search(r'\d+x\d+\+(\d+)\+\d+', line)

            widget = bumblebee.output.Widget(self, screen)
            if m:
                self._state = "on"
                widget.set("pos", int(m.group(1)))
            else:
                self._state = "off"
                widget.set("pos", sys.maxint());

            widgets.append(widget)

        widgets.sort(key=lambda widget : widget.get("pos"))

        return widgets

    def state(self, widget):
        return self._state

    def warning(self, widget):
        return False

    def critical(self, widget):
        return False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
