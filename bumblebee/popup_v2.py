"""Pop-up menus."""

import logging

try:
    import Tkinter as tk
except ImportError:
    # python 3
    try:
        import tkinter as tk
    except ImportError:
        logging.warning("failed to import tkinter - bumblebee popups won't work!")

import functools


class PopupMenu(object):
    def __init__(self):
        self._root = tk.Tk()
        self._root.withdraw()
        self._menu = tk.Menu(self._root)
        self._menu.bind("<FocusOut>", self._on_focus_out)
        self._menu.bind("<Leave>", self._on_focus_out)

    def _on_focus_out(self, event=None):
        self._root.destroy()

    def _on_click(self, callback):
        self._root.destroy()
        callback()


    def add_menuitem(self, menuitem, callback):
        self._menu.add_command(label=menuitem, command=functools.partial(self._on_click, callback))

    def show(self, event):
        try:
            self._menu.tk_popup(event['x'], event['y'])
        finally:
            self._menu.grab_release()
        self._root.mainloop()
