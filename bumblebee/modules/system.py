# -*- coding: utf-8 -*- 
# pylint: disable=C0111,R0903

""" system module

adds the possibility to
	* shutdown
	* reboot
the system.
	
Per default a confirmation dialog is shown before the actual action is performed.
	
Paramters:
	* system.confirm: show confirmation dialog before performing any action (default: true) 
"""

import logging
import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.popup_v2
import functools

try:
    import Tkinter as tk
    import tkMessageBox as tkmessagebox
except ImportError:
    # python 3
    try:
        import tkinter as tk
        from tkinter import messagebox as tkmessagebox
    except ImportError:
        logging.warning("failed to import tkinter - bumblebee popups won't work!")


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.text)
        )

        self._confirm = True
        if self.parameter("confirm", "true") == "false":
            self._confirm = False

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd=self.popup)

    def update(self, widgets):
        pass 

    def text(self, widget):
        return ""

    def _on_command(self, header, text, command):
        do_it = True
        if self._confirm:
            root = tk.Tk()
            root.withdraw()
            root.focus_set()
				
            do_it = tkmessagebox.askyesno(header, text)
            root.destroy()
		
        if do_it:
            bumblebee.util.execute(command) 


    def popup(self, widget):
        menu = bumblebee.popup_v2.PopupMenu()
        menu.add_menuitem("shutdown", callback=functools.partial(self._on_command, "Shutdown", "Shutdown?", "shutdown -h now"))
        menu.add_menuitem("reboot", callback=functools.partial(self._on_command, "Reboot", "Reboot?", "reboot"))
        menu.add_menuitem("log out", callback=functools.partial(self._on_command, "Log out", "Log out?",  "i3exit logout"))
        # don't ask for these
        menu.add_menuitem("switch user", callback=functools.partial(bumblebee.util.execute, "i3exit switch_user"))
        menu.add_menuitem("lock", callback=functools.partial(bumblebee.util.execute, "i3exit lock"))
        menu.add_menuitem("suspend", callback=functools.partial(bumblebee.util.execute, "i3exit suspend"))
        menu.add_menuitem("hibernate", callback=functools.partial(bumblebee.util.execute, "i3exit hibernate"))

        menu.show(widget)

    def state(self, widget):
        return []
