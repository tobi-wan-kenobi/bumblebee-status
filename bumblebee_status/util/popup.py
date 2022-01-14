"""Pop-up menus."""

import logging

import tkinter as tk

import functools


class menu(object):
    """Draws a hierarchical popup menu

    :param parent: If given, this menu is a leave of the "parent" menu
    :param leave: If set to True, close this menu when mouse leaves the area (defaults to True)
    """

    def __init__(self, parent=None, leave=True):
        self.running = True

        self.parent = parent

        self._root = parent.root() if parent else tk.Tk()
        self._root.withdraw()
        self._menu = tk.Menu(self._root, tearoff=0)
        self._menu.bind("<FocusOut>", self.__on_focus_out)

        if leave:
            self._menu.bind("<Leave>", self.__on_focus_out)
        elif not parent:
            self.add_menuitem("close", self.__on_focus_out)
            self.add_separator()

        self._menu.bind("<ButtonRelease-1>", self.release)

    """Returns the root node of this menu

    :return: root node
    """

    def root(self):
        return self._root

    """Returns the menu

    :return: menu
    """

    def menu(self):
        return self._menu

    def __on_focus_out(self, event=None):
        self.running = False
        self._root.destroy()

    def __on_click(self, callback):
        self._root.destroy()
        callback()

    def release(self, event=None):
        self.running=False
        if self.parent:
            self.parent.release(event)

    """Adds a cascading submenu to the current menu

    :param menuitem: label to display for the submenu
    :param submenu: submenu to show
    """

    def add_cascade(self, menuitem, submenu):
        self._menu.add_cascade(label=menuitem, menu=submenu.menu())

    """Adds an item to the current menu

    :param menuitem: label to display for the entry
    :param callback: method to invoke on click
    """

    def add_menuitem(self, menuitem, callback):
        self._menu.add_command(
            label=menuitem, command=functools.partial(self.__on_click, callback)
        )

    """Adds a separator to the menu in the current location"""

    def add_separator(self):
        self._menu.add_separator()

    """Shows this menu

    :param event: i3wm event that triggered the menu (dict that contains "x" and "y" fields)
    :param offset_x: x-axis offset from mouse position for the menu (defaults to 0)
    :param offset_y: y-axis offset from mouse position for the menu (defaults to 0)
    """

    def show(self, event, offset_x=0, offset_y=0):
        try:
            self._menu.tk_popup(event["x"] + offset_x, event["y"] + offset_y)
        finally:
            self._menu.grab_release()

        while self.running == True:
            try:
                self._root.update_idletasks()
                self._root.update()
            except:
                self.running = False
        try:
            self._root.destroy()
        except:
            pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
