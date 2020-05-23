# pylint: disable=C0111,R0903

"""My TEST

Requires the following executable:
    * arandr
    * xrandr
"""

import fnmatch
from functools import partial
import logging
import os

import core.module
import core.widget
import core.input
import core.decorators
import util.cli
from util import popup
from util.cli import execute


log = logging.getLogger(__name__)

__screenlayout_dir__ = os.path.expanduser("~/.screenlayout")

class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(''))

        self.manager = self.parameter("manager", "arandr")
        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd=self.popup,
        )

        core.input.register(self, button=core.input.RIGHT_MOUSE,
                            cmd=self.popup)

    def popup(self, widget):
        """Create Popup that allows the user to control their displays in one
        of three ways: launch arandr, select a pre-set screenlayout, toggle a
        display.
        """
        menu = popup.menu()
        menu.add_menuitem("arandr",
            callback=partial(execute, self.manager)
        )
        menu.add_separator()

        displays = Module._get_displays()
        layouts = Module._get_layouts()
        available_layouts = Module._prune_layouts(layouts, displays)
        log.debug("Available layouts:")
        log.debug(available_layouts)

        if len(available_layouts) > 0:
            for layout in available_layouts:
                sh = os.path.join(__screenlayout_dir__, layout)
                sh_name = os.path.splitext(layout)[0]
                cmd = self.parameter(sh_name, sh)
                menu.add_menuitem(sh_name,
                                  callback=partial(util.cli.execute, sh)
                )

        menu.show(widget, 0, 0)

    @staticmethod
    def _get_displays():
        """Queries xrandr and builds a dict of the displays and their state.

        The dict entries are key by the display and are bools (True if
        connected).
        """
        displays = {}
        for line in execute("xrandr -q").split("\n"):
            if not "connected" in line:
                continue
            parts = line.split(" ", 2)
            display = parts[0]
            displays[display] = True if parts[1] == "connected" else False

        return displays

    @staticmethod
    def _get_layouts():
        """Loads and parses the arandr screen layout scripts."""
        layouts = {}
        for filename in os.listdir(__screenlayout_dir__):
            if fnmatch.fnmatch(filename, '*.sh'):
                fullpath = os.path.join(__screenlayout_dir__, filename)
                with open(fullpath, "r") as file:
                    for line in file:
                        s_line = line.strip()
                        if not "xrandr" in s_line:
                            continue
                        displays_in_file = Module._parse_layout(line)
                        layouts[filename] = displays_in_file
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
                if need not in displays or not displays[need]:
                    still_valid = False
                    break
            if still_valid:
                available.append(layout)
        return available


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
