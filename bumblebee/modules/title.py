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
        try:
            self._i3 = i3ipc.Connection()
            self._full_title = self._i3.get_tree().find_focused().name
        except Exception:
            self._full_title = "n/a"

    def focused_title(self, widget):
        title = self._full_title[0:self.parameter("max", 64)]
        if title != self._full_title:
            title = self._full_title[0:self.parameter("max", 64) - 3]
            title = "{}...".format(title)

        return title

    def update(self, widgets):
        """Update current title."""
        try:
            self._full_title = self._i3.get_tree().find_focused().name
        except Exception:
            self._full_title = "n/a"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
