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
    def __init__(self, parent=None, leave=True):

        if not parent:
            self._root = tk.Tk()
            self._root.withdraw()
            self._menu = tk.Menu(self._root, tearoff=0)
            self._menu.bind("<FocusOut>", self._on_focus_out)
        else:
            self._root = parent.root()
            self._root.withdraw()
            self._menu = tk.Menu(self._root, tearoff=0)
            self._menu.bind("<FocusOut>", self._on_focus_out)
        if leave:
            self._menu.bind("<Leave>", self._on_focus_out)

    def root(self):
        return self._root

    def menu(self):
        return self._menu

    def _on_focus_out(self, event=None):
        self._root.destroy()

    def _on_click(self, callback):
        self._root.destroy()
        callback()

    def add_cascade(self, menuitem, submenu):
        self._menu.add_cascade(label=menuitem, menu=submenu.menu())

    def add_menuitem(self, menuitem, callback):
        self._menu.add_command(label=menuitem, command=functools.partial(self._on_click, callback))

    def show(self, event, offset_x=0, offset_y=0):
        try:
            self._menu.tk_popup(event['x'] + offset_x, event['y'] + offset_y)
        finally:
            self._menu.grab_release()
        self._root.mainloop()
