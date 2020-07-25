# pylint: disable=C0111,R0903

"""Copy passwords from a password store into the clipboard (currently supports only 'pass')

Many thanks to [@bbernhard](https://github.com/bbernhard) for the idea!

Requires the following executable:
    * pass (aka password-store)

Parameters:
    * vault.duration: Duration until password is cleared from clipboard (defaults to 30)
    * vault.location: Location of the password store (defaults to ~/.password-store)
    * vault.offx: x-axis offset of popup menu (defaults to 0)
    * vault.offy: y-axis offset of popup menu (defaults to 0)
    * vault.text: Text to display on the widget (defaults to <click-for-password>)

Many thanks to `bbernhard <https://github.com/bbernhard>`_ for the idea!
"""


# TODO:
# - support multiple backends by abstracting the menu structure into a tree
# - build the menu and the actions based on that abstracted tree
#

import os
import time
import threading

import core.module
import core.widget
import core.input
import core.event

import util.cli
import util.popup


def generate_callback(callback, path, name):
    return lambda: callback(os.path.join(path, name))

def build_menu(parent, current_directory, callback):
    with os.scandir(current_directory) as it:
        for entry in it:
            if entry.name.startswith("."):
                continue
            if entry.is_file():
                name = entry.name[: entry.name.rfind(".")]
                parent.add_menuitem(
                    name,
                    callback=generate_callback(callback, current_directory, name),
                )

            else:
                submenu = util.popup.menu(parent, leave=False)
                build_menu(
                    submenu, os.path.join(current_directory, entry.name), callback
                )
                parent.add_cascade(entry.name, submenu)


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))

        self.__duration = int(self.parameter("duration", 30))
        self.__offx = int(self.parameter("offx", 0))
        self.__offy = int(self.parameter("offy", 0))
        self.__path = os.path.expanduser(
            self.parameter("location", "~/.password-store/")
        )
        self.__reset()
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.popup)

    def popup(self, widget):
        menu = util.popup.menu(leave=False)

        build_menu(menu, self.__path, self.__callback)
        menu.show(widget, offset_x=self.__offx, offset_y=self.__offy)

    def __reset(self):
        self.__timer = None
        self.__text = str(self.parameter("text", "<click-for-password>"))

    def __callback(self, secret_name):
        secret_name = secret_name.replace(self.__path, "")  # remove common path
        if self.__timer:
            self.__timer.cancel()
        env = os.environ
        env["PASSWORD_STORE_CLIP_TIME"] = str(self.__duration)
        res = util.cli.execute(
            "pass show -c {}".format(secret_name),
            wait=False,
            env=env,
            ignore_errors=True,
        )
        self.__timer = threading.Timer(self.__duration, self.__reset)
        self.__timer.start()
        self.__start = int(time.time())
        self.__text = secret_name

    def text(self, widget):
        if self.__timer:
            return "{} ({}s)".format(
                self.__text, self.__duration - (int(time.time()) - self.__start)
            )
        return self.__text


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
