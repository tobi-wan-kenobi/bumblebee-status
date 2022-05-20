# -*- coding: utf-8 -*-
# pylint: disable=C0111,R0903

""" system module

adds the possibility to
	* shutdown
	* reboot

the system.
	
Per default a confirmation dialog is shown before the actual action is performed.
	
Parameters:
	* system.confirm: show confirmation dialog before performing any action (default: true) 
        * system.reboot: specify a reboot command (defaults to 'reboot')
        * system.shutdown: specify a shutdown command (defaults to 'shutdown -h now')
        * system.logout: specify a logout command (defaults to 'i3exit logout')
        * system.switch_user: specify a command for switching the user (defaults to 'i3exit switch_user')
        * system.lock: specify a command for locking the screen (defaults to 'i3exit lock')
        * system.suspend: specify a command for suspending (defaults to 'i3exit suspend')
        * system.hibernate: specify a command for hibernating (defaults to 'i3exit hibernate')

Requirements:
	tkinter (python3-tk package on debian based systems either you can install it as python package)

contributed by `bbernhard <https://github.com/bbernhard>`_ - many thanks!
"""

import logging
import functools

try:
    import tkinter as tk
    from tkinter import messagebox as tkmessagebox
except ImportError:
    logging.warning("failed to import tkinter - bumblebee popups won't work!")

import core.module
import core.widget
import core.input
import core.decorators

import util.cli
import util.popup
import util.format


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))

        self.__confirm = util.format.asbool(self.parameter("confirm", True))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.popup)

    def text(self, widget):
        return ""

    def __on_command(self, header, text, command):
        do_it = True
        if self.__confirm:
            root = tk.Tk()
            root.withdraw()
            root.focus_set()

            do_it = tkmessagebox.askyesno(header, text)
            root.destroy()

        if do_it:
            util.cli.execute(command)

    def popup(self, widget):
        popupcmd = self.parameter("popupcmd", "");
        if (popupcmd != ""):
            util.cli.execute(popupcmd)
            return

        menu = util.popup.menu()
        reboot_cmd = self.parameter("reboot", "reboot")
        shutdown_cmd = self.parameter("shutdown", "shutdown -h now")
        logout_cmd = self.parameter("logout", "i3exit logout")
        switch_user_cmd = self.parameter("switch_user", "i3exit switch_user")
        lock_cmd = self.parameter("lock", "i3exit lock")
        suspend_cmd = self.parameter("suspend", "i3exit suspend")
        hibernate_cmd = self.parameter("hibernate", "i3exit hibernate")

        menu.add_menuitem(
            "shutdown",
            callback=functools.partial(
                self.__on_command, "Shutdown", "Shutdown?", shutdown_cmd
            ),
        )
        menu.add_menuitem(
            "reboot",
            callback=functools.partial(
                self.__on_command, "Reboot", "Reboot?", reboot_cmd
            ),
        )
        menu.add_menuitem(
            "log out",
            callback=functools.partial(
                self.__on_command, "Log out", "Log out?", logout_cmd
            ),
        )
        # don't ask for these
        menu.add_menuitem(
            "switch user", callback=functools.partial(util.cli.execute, switch_user_cmd)
        )
        menu.add_menuitem(
            "lock", callback=functools.partial(util.cli.execute, lock_cmd)
        )
        menu.add_menuitem(
            "suspend", callback=functools.partial(util.cli.execute, suspend_cmd)
        )
        menu.add_menuitem(
            "hibernate", callback=functools.partial(util.cli.execute, hibernate_cmd)
        )

        menu.show(widget, 0, 0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
