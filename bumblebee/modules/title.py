# pylint: disable=C0111,R0903

"""Displays focused i3 window title.

Requirements:
    * i3ipc

Parameters:
    * title.max : Maximum character length for title before truncating. Defaults to 64.
    * title.placeholder : Placeholder text to be placed if title was truncated. Defaults to "...".
    * title.scroll : Boolean flag for scrolling title. Defaults to False
"""

import threading

try:
    import i3ipc
except ImportError:
    pass

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

from bumblebee.output import scrollable

_no_title = "n/a"

class Module(bumblebee.engine.Module):
    """Window title module."""

    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine,
            config
        )

        # parsing of parameters
        self._scroll = bumblebee.util.asbool(self.parameter("scroll", False))
        self._max = int(self.parameter("max", 64))
        self._placeholder = self.parameter("placeholder", "...")

        # set output of the module
        self.widgets(bumblebee.output.Widget(full_text=
            self._scrolling_focused_title if self._scroll else self._focused_title))

        # create a connection with i3ipc
        try:
            self._i3 = i3ipc.Connection()
            # event is called both on focus change and title change
            self._i3.on("window", lambda _p_i3, _p_e: self._pollTitle())
            # begin listening for events
            threading.Thread(target=self._i3.main).start()
        except:
            pass

        # initialize the first title
        self._pollTitle()

    def _focused_title(self, widget):
        return self._title

    @scrollable
    def _scrolling_focused_title(self, widget):
        return self._full_title

    def _pollTitle(self):
        """Updating current title."""
        try:
            self._full_title = self._i3.get_tree().find_focused().name
        except:
            self._full_title = _no_title
        if self._full_title is None:
            self._full_title = _no_title

        if not self._scroll:
            # cut the text if it is too long
            if len(self._full_title) > self._max:
                self._title = self._full_title[0:self._max - len(self._placeholder)]
                self._title = "{}{}".format(self._title, self._placeholder)
            else:
                self._title = self._full_title

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
