# pylint: disable=C0111,R0903

"""Displays focused i3 window title.

Requirements:
    * i3ipc

Parameters:
    * title.max : Maximum character length for title before truncating. Defaults to 64.
    * title.placeholder : Placeholder text to be placed if title was truncated. Defaults to "...".
"""

try:
    import i3ipc
except ImportError:
    pass

import textwrap
import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    """Window title module."""

    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine,
            config,
            bumblebee.output.Widget(full_text=self.focused_title)
        )
        self._i3 = i3ipc.Connection()
        self._full_title = self._i3.get_tree().find_focused().name

    def focused_title(self):
        """Truncates and returns proper-length title."""
        return textwrap.shorten(
            self._full_title,
            width=float(self.parameter("max", 64)),
            placeholder=self.parameter("placeholder", "...")
        )

    def update(self, widgets):
        """Update current title."""
        self._full_title = self._i3.get_tree().find_focused().name

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
