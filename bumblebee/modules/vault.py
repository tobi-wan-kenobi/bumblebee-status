# pylint: disable=C0111,R0903

"""Copy passwords from a password store into the clipboard (currently supports only "pass")

Many thanks to [@bbernhard](https://github.com/bbernhard) for the idea!

Parameters:
    * vault.duration: Duration until password is cleared from clipboard (defaults to 30)
    * vault.location: Location of the password store (defaults to ~/.password-store)
    * vault.offx: x-axis offset of popup menu (defaults to 0)
    * vault.offy: y-axis offset of popup menu (defaults to 0)
"""


# TODO: 
# - support multiple backends by abstracting the menu structure into a tree
# - build the menu and the actions based on that abstracted tree
#

import os
import time
import threading
import bumblebee.util
import bumblebee.popup_v2
import bumblebee.input
import bumblebee.output
import bumblebee.engine

def build_menu(parent, current_directory, callback):
    with os.scandir(current_directory) as it:
        for entry in it:
            if entry.name.startswith("."): continue
            if entry.is_file():
                name = entry.name[:entry.name.rfind(".")]
                parent.add_menuitem(name, callback=lambda : callback(os.path.join(current_directory, name)))

            else:
                submenu = bumblebee.popup_v2.PopupMenu(parent, leave=False)
                build_menu(submenu, os.path.join(current_directory, entry.name), callback)
                parent.add_cascade(entry.name, submenu)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.text)
        )
        self._duration = int(self.parameter("duration", 30))
        self._offx = int(self.parameter("offx", 0))
        self._offy = int(self.parameter("offy", 0))
        self._path = os.path.expanduser(self.parameter("location", "~/.password-store/"))
        self._reset()
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
           cmd=self.popup)

    def popup(self, widget):
        menu = bumblebee.popup_v2.PopupMenu(leave=False)

        build_menu(menu, self._path, self._callback)
        menu.show(widget, offset_x=self._offx, offset_y=self._offy)

    def _reset(self):
        self._timer = None
        self._text = str(self.parameter("text", "<click-for-password>"))

    def _callback(self, secret_name):
        secret_name = secret_name.replace(self._path, "") # remove common path
        if self._timer:
            self._timer.cancel()
        # bumblebee.util.execute hangs for some reason
        os.system("PASSWORD_STORE_CLIP_TIME={} pass -c {} > /dev/null 2>&1".format(self._duration, secret_name))
        self._timer = threading.Timer(self._duration, self._reset)
        self._timer.start()
        self._start = int(time.time())
        self._text = secret_name

    def text(self, widget):
        if self._timer:
            return "{} ({}s)".format(self._text, self._duration - (int(time.time()) - self._start))
        return self._text

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
