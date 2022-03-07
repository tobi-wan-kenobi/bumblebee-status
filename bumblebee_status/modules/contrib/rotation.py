# pylint: disable=C0111,R0903

"""Shows a widget for each connected screen and allows the user to loop through different orientations.

Requires the following executable:
    * xrandr
"""

import core.module
import core.input

import util.cli

possible_orientations = ["normal", "left", "inverted", "right"]


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

    def update(self):
        widgets = self.widgets()
        for line in util.cli.execute("xrandr -q").split("\n"):
            if not " connected" in line:
                continue
            display = line.split(" ", 2)[0]

            orientation = "normal"
            for curr_orient in possible_orientations:
                if (line.split(" ")).count(curr_orient) > 1:
                    orientation = curr_orient
                    break

            widget = self.widget(name=display)
            if not widget:
                widget = self.add_widget(full_text=display, name=display)
                core.input.register(
                    widget, button=core.input.LEFT_MOUSE, cmd=self.__toggle
                )
            widget.set("orientation", orientation)

    def state(self, widget):
        return widget.get("orientation", "normal")

    def __toggle(self, event):
        widget = self.widget_by_id(event["instance"])

        # compute new orientation based on current orientation
        idx = possible_orientations.index(widget.get("orientation"))
        idx = (idx + 1) % len(possible_orientations)
        new_orientation = possible_orientations[idx]

        widget.set("orientation", new_orientation)

        util.cli.execute(
            "xrandr --output {} --rotation {}".format(widget.name, new_orientation)
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
