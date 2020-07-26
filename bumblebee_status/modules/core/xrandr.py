# pylint: disable=C0111,R0903

"""Shows a widget for each connected screen and allows the user to enable/disable screens.

Parameters:
    * xrandr.overwrite_i3config: If set to 'true', this module assembles a new i3 config
      every time a screen is enabled or disabled by taking the file '~/.config/i3/config.template'
      and appending a file '~/.config/i3/config.<screen name>' for every screen.
    * xrandr.autoupdate: If set to 'false', does *not* invoke xrandr automatically. Instead, the
      module will only refresh when displays are enabled or disabled (defaults to true)
    * xrandr.exclude: Comma-separated list of display name prefixes to exclude
    * xrandr.autotoggle: Boolean flag to automatically enable new displays (defaults to false)
    * xrandr.autotoggle_side: Which side to put autotoggled displays on ('right' or 'left', defaults to 'right')

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
except Exception:
    pass


RESOLUTION_REGEX = re.compile(r"\d+x\d+\+(\d+)\+\d+")


class DisplayInfo:
    def __init__(self, name, resolution, connected, added, removed):
        self.name = name
        self.active = resolution is not None
        self.connected = connected
        self.added = added
        self.removed = removed

        self.position = int(resolution.group(1)) if self.active else sys.maxsize
        self.state = "on" if self.active else "off"

    def __str__(self):
        return "DisplayInfo(name={}, active={}, connected={}, added={}, removed={}, position={}, state={})".format(
            self.name,
            self.active,
            self.connected,
            self.added,
            self.removed,
            self.position,
            self.state,
        )

    def __repr__(self):
        return str(self)


class Module(core.module.Module):
    @core.decorators.every(seconds=5)  # takes up to 5s to detect a new screen
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self._exclude = tuple(util.format.aslist(self.parameter("exclude")))
        self._autoupdate = util.format.asbool(self.parameter("autoupdate", True))
        self._autotoggle = util.format.asbool(self.parameter("autotoggle", False))
        self._autotoggle_side = self.parameter("autotoggle_side", "right")

        self._connected_displays = []
        self._active_displays = []
        self._initialized = False

        try:
            i3.Subscription(self._output_update, "output")
        except Exception:
            pass

    def _output_update(self, *_):
        self.update(force=True)

    def _query_displays(self):
        displays = []

        for line in util.cli.execute("xrandr -q").split("\n"):
            # disconnected or connected
            if "connected" not in line:
                continue

            name = line.split(" ", 2)[0]
            resolution = RESOLUTION_REGEX.search(line)
            active = resolution is not None

            connected = "disconnected" not in line
            added = connected and not active and name not in self._connected_displays
            removed = not connected and active and name in self._active_displays

            displays.append(DisplayInfo(name, resolution, connected, added, removed))

        self._connected_displays = [
            display.name for display in displays if display.connected
        ]
        self._active_displays = [display.name for display in displays if display.active]

        return displays

    def update(self, force=False):
        if not (self._autoupdate or force or not self._initialized):
            return

        self.clear_widgets()

        for display in self._query_displays():
            if display.name.startswith(self._exclude):
                continue

            if self._initialized and self._autotoggle:
                if display.added:
                    self._enable_display(display.name, self._autotoggle_side)
                elif display.removed:
                    self._disable_display(display.name)

            if not display.connected:
                continue

            widget = self.add_widget(full_text=display.name, name=display.name)
            core.input.register(widget, button=1, cmd=self._toggle)
            core.input.register(widget, button=3, cmd=self._toggle)

            widget.set("state", display.state)
            widget.set("pos", display.position)

        if not self._autoupdate:
            widget = self.add_widget(full_text="")
            widget.set("state", "refresh")
            core.input.register(widget, button=1, cmd=self.update)

        self._initialized = True

    def state(self, widget):
        return widget.get("state", "off")

    def _toggle_cmd(self):
        if util.format.asbool(self.parameter("overwrite_i3config", False)):
            return utility("toggle-display.sh")
        else:
            return "xrandr"

    def _disable_display(self, name):
        if len(self._active_displays) > 1:
            util.cli.execute("{} --output {} --off".format(self._toggle_cmd(), name))

    def _enable_display(self, name, side=None):
        # TODO: is there ever a case when there isn't a neighbor?
        command = "{} --output {} --auto".format(self._toggle_cmd(), name)
        if side and self._active_displays:
            neighbor_index = 0 if side == "left" else -1
            command += " --{}-of {}".format(side, self._active_displays[neighbor_index])

        util.cli.execute(command)

    def _toggle(self, event):
        widget = self.widget(widget_id=event["instance"])

        if widget.get("state") == "on":
            self._disable_display(widget.name)
        else:
            side = "left" if event["button"] == core.input.LEFT_MOUSE else "right"
            self._enable_display(widget.name, side)

        self.update(force=True)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
