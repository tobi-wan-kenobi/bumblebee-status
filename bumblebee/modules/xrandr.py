import bumblebee.module
import re
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
            m = re.search(r'\d+x\d+\+\d+\+\d+', line)
            self._state = "on" if m else "off"
            widgets.append(bumblebee.output.Widget(self, screen))

        return widgets

    def state(self, widget):
        return self._state

    def warning(self, widget):
        return False

    def critical(self, widget):
        return False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
