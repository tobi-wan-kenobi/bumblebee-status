# pylint: disable=C0111,R0903

"""Shows when a key is pressed

Parameters:
    * keys.keys: Comma-separated list of keys to monitor (defaults to "")
"""

import core.module
import core.widget
import core.decorators
import core.event

import util.format

from pynput.keyboard import Listener

NAMES = {
    "Key.cmd": "cmd",
    "Key.ctrl": "ctrl",
    "Key.shift": "shift",
    "Key.alt": "alt",
}

class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self._listener = Listener(on_press=self._key_press, on_release=self._key_release)

        self._keys = util.format.aslist(self.parameter("keys", "Key.cmd,Key.ctrl,Key.alt,Key.shift"))

        for k in self._keys:
            self.add_widget(name=k, full_text=self._display_name(k), hidden=True)
        self._listener.start()

    def _display_name(self, key):
        return NAMES.get(key, key)

    def _key_press(self, key):
        key = str(key)
        if not key in self._keys: return
        self.widget(key).hidden = False
        core.event.trigger("update", [self.id], redraw_only=False)

    def _key_release(self, key):
        key = str(key)
        if not key in self._keys: return
        self.widget(key).hidden = True
        core.event.trigger("update", [self.id], redraw_only=False)
    
    def state(self, widget):
        return widget.name

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
