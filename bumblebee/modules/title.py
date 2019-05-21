# pylint: disable=C0111,R0903

"""Displays focused i3 window title.

Requirements:
    * i3ipc

Parameters:
    * title.max : Maximum character length for title before truncating. Defaults to 64.
    * title.placeholder : Placeholder text to be placed if title was truncated. Defaults to "...".
    * title.scroll : Boolean flag for scrolling title. Defaults to False
"""

try:
    import i3ipc
except ImportError:
    pass

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

from bumblebee.output import scrollable

no_title = "n/a"

class Module(bumblebee.engine.Module):
    """Window title module."""

    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine,
            config,
            bumblebee.output.Widget(full_text=self.get_title)
        )
        try:
            self._i3 = i3ipc.Connection()
            self._full_title = self._i3.get_tree().find_focused().name
        except Exception:
            self._full_title = no_title

    def get_title(self, widget):
        if bumblebee.util.asbool(self.parameter("scroll", False)):
            return self.scrolling_focused_title(widget)
        else:
            return self.focused_title(widget)

    def focused_title(self, widget):
        max = int(self.parameter("max", 64))
        title = self._full_title[0:max]
        placeholder = self.parameter("placeholder", "...")
        if title != self._full_title:
            title = self._full_title[0:max - len(placeholder)]
            title = "{}{}".format(title, placeholder)

        return title

    @scrollable
    def scrolling_focused_title(self, widget):
        return self._full_title

    def update(self, widgets):
        """Update current title."""
        try:
            self._full_title = self._i3.get_tree().find_focused().name
        except Exception:
            self._full_title = no_title

        if self._full_title is None:
            self._full_title = no_title

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
