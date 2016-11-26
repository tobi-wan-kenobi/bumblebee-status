import bumblebee.module
import bumblebee.util
import re
import os
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

        self._widgets = []

    def toggle(self, event, widget):
        path = os.path.dirname(os.path.abspath(__file__))
        toggle_cmd = "{}/../../bin/toggle-display.sh".format(path)

        if widget.get("state") == "on":
            bumblebee.util.execute("{} --output {} --off".format(toggle_cmd, widget.get("display")))
        else:
            neighbor = None
            for w in self._widgets:
                if w.get("state") == "on":
                    neighbor = w
                    if event.get("button") == 1:
                        break
    
            if neighbor == None:
                bumblebee.util.execute("{} --output {} --auto".format(toggle_cmd,
                    widget.get("display")))
            else:
                bumblebee.util.execute("{} --output {} --auto --{}-of {}".format(toggle_cmd,
                    widget.get("display"), "left" if event.get("button") == 1 else "right",
                    neighbor.get("display")))

    def widgets(self):
        process = subprocess.Popen([ "xrandr", "-q" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        widgets = []

        for line in output.split("\n"):
            if not " connected" in line:
                continue
            display = line.split(" ", 2)[0]
            m = re.search(r'\d+x\d+\+(\d+)\+\d+', line)

            widget = bumblebee.output.Widget(self, display, instance=display)
            widget.set("display", display)

            # not optimal (add callback once per interval), but since
            # add_callback() just returns if the callback has already
            # been registered, it should be "ok"
            self._output.add_callback(module=display, button=1,
                cmd=self.toggle)
            self._output.add_callback(module=display, button=3,
                cmd=self.toggle)
            if m:
                widget.set("state", "on")
                widget.set("pos", int(m.group(1)))
            else:
                widget.set("state", "off")
                widget.set("pos", sys.maxint)

            widgets.append(widget)

        widgets.sort(key=lambda widget : widget.get("pos"))

        self._widgets = widgets

        return widgets

    def state(self, widget):
        return widget.get("state", "off")

    def warning(self, widget):
        return False

    def critical(self, widget):
        return False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
