"""Displays and changes the current keyboard layout

Requires the following executable:
    * xkb-switch
"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.current_layout)
        super(Module, self).__init__(engine, config, widget)
        engine.input.register_callback(
            self,
            button=bumblebee.input.LEFT_MOUSE,
            cmd=self._next_keymap)
        self._current_layout = self._get_current_layout()

    def current_layout(self, __):
        return self._current_layout

    def _next_keymap(self, event):
        try:
            bumblebee.util.execute("xkb-switch -n")
        except RuntimeError:
            pass

    def _get_current_layout(self):
        try:
            res = bumblebee.util.execute("xkb-switch")
            return res.split("\n")[0]
        except RuntimeError:
            return ["n/a"]

    def update(self, __):
        self._current_layout = self._get_current_layout()
