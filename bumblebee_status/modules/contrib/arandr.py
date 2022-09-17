# pylint: disable=C0111,R0903

"""Enables handy interaction with arandr for display management.  Left-clicking
will execute arandr for interactive display management.  Right-clicking will
bring up a context- and state-sensitive menu that will allow you to switch to a
saved screen layout as well as toggle on/off individual connected displays.

Parameters:
    * No configuration parameters

Requires the following python modules:
    * tkinter

Requires the following executable:
    * arandr
    * xrandr

contributed by `zerorust <https://github.com/zerorust>`_ - many thanks!
"""

import fnmatch
from functools import partial
import logging
import os
import re

import core.module
import core.widget
import core.input
import core.decorators
from util import popup
from util.cli import execute


log = logging.getLogger(__name__)

__screenlayout_dir__ = os.path.expanduser("~/.screenlayout")


class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(''))

        self.manager = self.parameter("manager", "arandr")
        self.toggle_cmd = "xrandr"
        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd=self.popup,
        )

        core.input.register(self, button=core.input.RIGHT_MOUSE,
                            cmd=self.popup)

    @staticmethod
    def activate_layout(layout_path):
        log.debug("activating layout")
        log.debug(layout_path)
        execute(layout_path, ignore_errors=True)

    def popup(self, widget):
        """Create Popup that allows the user to control their displays in one
        of three ways: launch arandr, select a pre-set screenlayout, toggle a
        display.
        """
        menu = popup.menu()
        menu.add_menuitem(
            "arandr",
            callback=partial(execute, self.manager, ignore_errors=True)
        )
        menu.add_separator()

        displays = Module._get_displays()
        log.debug(displays)
        layouts = Module._get_layouts()
        available_layouts = Module._prune_layouts(layouts, displays)
        log.debug("Available layouts:")
        log.debug(available_layouts)

        if len(available_layouts) > 0:
            for layout in available_layouts:
                sh = os.path.join(__screenlayout_dir__, layout)
                sh_name = os.path.splitext(layout)[0]
                menu.add_menuitem(sh_name,
                                  callback=partial(self.activate_layout, sh))

        menu.add_separator()
        count_on = 0
        for display, state in displays.items():
            if state[1]:
                count_on += 1
        for display, state in displays.items():
            if not state[0]:
                continue
            on_off = "On" if state[1] else "Off"
            menu_line = "{}: {}".format(display, on_off)
            menu.add_menuitem(menu_line,
                              callback=partial(self.toggle_display, display,
                                               state[1], count_on))

        menu.show(widget, 0, 0)

    def toggle_display(self, display, current_state, count_on):
        """Toggle a display on or off based on its current state."""
        if current_state:
            log.debug("toggling off {}".format(display))
            if count_on == 1:
                log.info("attempted to turn off last display")
                return
            execute("{} --output {} --off".format(self.toggle_cmd, display), ignore_errors=True)
        else:
            log.debug("toggling on {}".format(display))
            execute(
                "{} --output {} --auto".format(self.toggle_cmd, display),
                ignore_errors=True
            )

    @staticmethod
    def _get_displays():
        """Queries xrandr and builds a dict of the displays and their state.

        The dict entries are key by the display and are bools (True if
        connected).
        """
        displays = {}
        for line in execute("xrandr -q", ignore_errors=True).split("\n"):
            if "connected" not in line:
                continue
            is_on = bool(re.search(r"\d+x\d+\+(\d+)\+\d+", line))
            parts = line.split(" ", 2)
            display = parts[0]
            displays[display] = (
                (True, is_on) if parts[1] == "connected" else (False, is_on)
            )

        return displays

    @staticmethod
    def _get_layouts():
        """Loads and parses the arandr screen layout scripts."""
        layouts = {}
        try:
            for filename in os.listdir(__screenlayout_dir__):
                if fnmatch.fnmatch(filename, '*.sh'):
                    fullpath = os.path.join(__screenlayout_dir__, filename)
                    with open(fullpath, "r") as file:
                        for line in file:
                            s_line = line.strip()
                            if "xrandr" not in s_line:
                                continue
                            displays_in_file = Module._parse_layout(line)
                            layouts[filename] = displays_in_file
        except Exception as e:
            log.error(str(e))
        return layouts

    @staticmethod
    def _parse_layout(line):
        """Parses a single xrandr line to find what displays are active in the
        command.  Returns them as a list.
        """
        active_displays = []
        to_check = line[7:].split("--output ")
        for check in to_check:
            if not check or "off" in check:
                continue
            active_displays.append(check.split(" ")[0])
        return active_displays

    @staticmethod
    def _prune_layouts(layouts, displays):
        """Return a list of layouts whose displays are actually connected."""
        available = []
        for layout, needs in layouts.items():
            still_valid = True
            for need in needs:
                if need not in displays or not displays[need][0]:
                    still_valid = False
                    break
            if still_valid:
                available.append(layout)
        return available


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
