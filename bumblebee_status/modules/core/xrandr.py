# pylint: disable=C0111,R0903

"""Shows a widget for each connected screen and allows the user to enable/disable screens.

Parameters:
    * xrandr.overwrite_i3config: If set to 'true', this module assembles a new i3 config
      every time a screen is enabled or disabled by taking the file '~/.config/i3/config.template'
      and appending a file '~/.config/i3/config.<screen name>' for every screen.
    * xrandr.autoupdate: If set to 'false', does *not* invoke xrandr automatically. Instead, the
      module will only refresh when displays are enabled or disabled (defaults to true)
    * xrandr.exclude: Comma-separated list of display name prefixes to exclude

Requires the following python module:
    * (optional) i3 - if present, the need for updating the widget list is auto-detected

Requires the following executable:
    * xrandr
"""

import re
import sys

import core.module
import core.input
import core.decorators

from bumblebee_status.discover import utility

import util.cli
import util.format

try:
    import i3
except ModuleNotFoundError:
    pass


class Module(core.module.Module):
    @core.decorators.every(seconds=5)  # takes up to 5s to detect a new screen
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self._exclude = tuple(filter(len, self.parameter("exclude", "").split(",")))
        self._active_displays = []
        self._autoupdate = util.format.asbool(self.parameter("autoupdate", True))
        self._needs_update = True

        try:
            i3.Subscription(self._output_update, "output")
        except Exception:
            pass

    def _output_update(self, event, data, _):
        self._needs_update = True

    def update(self):
        if not self._autoupdate and not self._needs_update:
            return

        self.clear_widgets()
        self._active_displays.clear()

        self._needs_update = False

        for line in util.cli.execute("xrandr -q").split("\n"):
            if " connected" not in line:
                continue

            display = line.split(" ", 2)[0]
            resolution = re.search(r"\d+x\d+\+(\d+)\+\d+", line)

            if resolution:
                self._active_displays.append(display)

            if display.startswith(self._exclude):
                continue

            widget = self.widget(display)
            if not widget:
                widget = self.add_widget(full_text=display, name=display)
                core.input.register(widget, button=1, cmd=self._toggle)
                core.input.register(widget, button=3, cmd=self._toggle)
            widget.set("state", "on" if resolution else "off")
            widget.set("pos", int(resolution.group(1)) if resolution else sys.maxsize)

        if not self._autoupdate:
            widget = self.add_widget(full_text="")
            widget.set("state", "refresh")
            core.input.register(widget, button=1, cmd=self._refresh)

    def state(self, widget):
        return widget.get("state", "off")

    def _refresh(self, event):
        self._needs_update = True

    def _toggle(self, event):
        if util.format.asbool(self.parameter("overwrite_i3config", False)):
            toggle_cmd = utility("toggle-display.sh")
        else:
            toggle_cmd = "xrandr"

        widget = self.widget(widget_id=event["instance"])

        if widget.get("state") == "on":
            if len(self._active_displays) > 1:
                util.cli.execute("{} --output {} --off".format(toggle_cmd, widget.name))
        elif not self._active_displays:
            util.cli.execute("{} --output {} --auto".format(toggle_cmd, widget.name))
        else:
            if event["button"] == core.input.LEFT_MOUSE:
                side, neighbor = "left", self._active_displays[0]
            else:
                side, neighbor = "right", self._active_displays[-1]

            util.cli.execute(
                "{} --output {} --auto --{}-of {}".format(
                    toggle_cmd, widget.name, side, neighbor,
                )
            )

        self._refresh(event)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
