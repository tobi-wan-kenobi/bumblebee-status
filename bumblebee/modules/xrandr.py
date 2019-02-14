# pylint: disable=C0111,R0903

"""Shows a widget for each connected screen and allows the user to enable/disable screens.

Parameters:
    * xrandr.overwrite_i3config: If set to 'true', this module assembles a new i3 config
        every time a screen is enabled or disabled by taking the file "~/.config/i3/config.template"
        and appending a file "~/.config/i3/config.<screen name>" for every screen.
    * xrandr.autoupdate: If set to 'false', does *not* invoke xrandr automatically. Instead, the
        module will only refresh when displays are enabled or disabled (defaults to true)

Requires the following python module:
    * (optional) i3 - if present, the need for updating the widget list is auto-detected

Requires the following executable:
    * xrandr
"""

import os
import re
import sys

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

try:
    import i3
except:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = []
        self._engine = engine
        super(Module, self).__init__(engine, config, widgets)
        self._autoupdate = bumblebee.util.asbool(self.parameter("autoupdate", True))
        self._needs_update = True

        try:
            i3.Subscription(self._output_update, "output")
        except:
            pass

    def _output_update(self, event, data, _):
        self._needs_update = True

    def update_widgets(self, widgets):
        new_widgets = []

        if self._autoupdate == False and self._needs_update == False:
            return

        self._needs_update = False

        for line in bumblebee.util.execute("xrandr -q").split("\n"):
            if not " connected" in line:
                continue
            display = line.split(" ", 2)[0]
            m = re.search(r'\d+x\d+\+(\d+)\+\d+', line)

            widget = self.widget(display)
            if not widget:
                widget = bumblebee.output.Widget(full_text=display, name=display)
                self._engine.input.register_callback(widget, button=1, cmd=self._toggle)
                self._engine.input.register_callback(widget, button=3, cmd=self._toggle)
            new_widgets.append(widget)
            widget.set("state", "on" if m else "off")
            widget.set("pos", int(m.group(1)) if m else sys.maxsize)

        while len(widgets) > 0:
            del widgets[0]
        for widget in new_widgets:
            widgets.append(widget)

        if self._autoupdate == False:
            widget = bumblebee.output.Widget(full_text="")
            widget.set("state", "refresh")
            self._engine.input.register_callback(widget, button=1, cmd=self._refresh)
            widgets.append(widget)

    def update(self, widgets):
        self.update_widgets(widgets)

    def state(self, widget):
        return widget.get("state", "off")

    def _refresh(self, event):
        self._needs_update = True

    def _toggle(self, event):
        self._needs_update = True
        path = os.path.dirname(os.path.abspath(__file__))

        if bumblebee.util.asbool(self.parameter("overwrite_i3config", False)) == True:
            toggle_cmd = "{}/../../bin/toggle-display.sh".format(path)
        else:
            toggle_cmd = "xrandr"

        widget = self.widget_by_id(event["instance"])

        if widget.get("state") == "on":
            bumblebee.util.execute("{} --output {} --off".format(toggle_cmd, widget.name))
        else:
            first_neighbor = next((widget for widget in self.widgets() if widget.get("state") == "on"), None)
            last_neighbor = next((widget for widget in reversed(self.widgets()) if widget.get("state") == "on"), None)

            neighbor = first_neighbor if event["button"] == bumblebee.input.LEFT_MOUSE else last_neighbor

            if neighbor is None:
                bumblebee.util.execute("{} --output {} --auto".format(toggle_cmd, widget.name))
            else:
                bumblebee.util.execute("{} --output {} --auto --{}-of {}".format(toggle_cmd, widget.name,
                    "left" if event.get("button") == bumblebee.input.LEFT_MOUSE else "right",
                    neighbor.name))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
