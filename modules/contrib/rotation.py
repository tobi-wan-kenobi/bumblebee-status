# pylint: disable=C0111,R0903

"""Shows a widget for each connected screen and allows the user to loop through different orientations.

Requires the following executable:
    * xrandr
"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

possible_orientations = ["normal", "left", "inverted", "right"]

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = []
        self._engine = engine
        super(Module, self).__init__(engine, config, widgets)
        self.update_widgets(widgets)

    def update_widgets(self, widgets):
        for line in bumblebee.util.execute("xrandr -q").split("\n"):
            if not " connected" in line:
                continue
            display = line.split(" ", 2)[0]

            orientation = "normal"
            for curr_orient in possible_orientations:
                if((line.split(" ")).count(curr_orient) > 1):
                    orientation = curr_orient
                    break

            widget = self.widget(display)
            if not widget:
                widget = bumblebee.output.Widget(full_text=display, name=display)
                self._engine.input.register_callback(widget, button=bumblebee.input.LEFT_MOUSE, cmd=self._toggle)
            widget.set("orientation", orientation)
            widgets.append(widget)

    def update(self, widgets):
        if len(widgets) <= 0:
            self.update_widgets(widgets)

    def state(self, widget):
        return widget.get("orientation", "normal")

    def _toggle(self, event):
        widget = self.widget_by_id(event["instance"])

        # compute new orientation based on current orientation
        idx = possible_orientations.index(widget.get("orientation"))
        idx = (idx + 1) % len(possible_orientations)
        new_orientation = possible_orientations[idx]

        widget.set("orientation", new_orientation)

        bumblebee.util.execute("xrandr --output {} --rotation {}".format(widget.name, new_orientation))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
