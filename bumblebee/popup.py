"""Pop-up menus."""

try:
    import Tkinter as tk
except ImportError:
    # python 3
    try:
        import tkinter as tk
    except ImportError:
        pass

import logging

class PopupMenu:
    """The popup-menu."""

    def __init__(self):
        """Initialize."""
        # menu widget
        self.root = tk.Tk()
        self.root.withdraw()
        self.menu = tk.Menu(self.root)

        # internal state
        self._item_count = 0
        self._clicked_item = None
        self._active = False

        # bind event of popup getting closed by clicking outside of its area
        self.menu.bind('<Unmap>',
                       lambda event: self.root.after_idle(
                           self._dismiss_callback))

    def add_menuitem(self, menuitem, callback=None):
        """Add menu items."""
        item_count = self._item_count

        def click_callback():
            # call internal callback with item index
            self._item_callback(item_count)

        # default to internal callback
        if callback is None:
            callback = click_callback
        self.menu.add_command(label=menuitem,
                              command=click_callback)

        # track item index
        self._item_count += 1

    def _item_callback(self, which_item):
        """Menu item click callback."""
        logging.debug('popup: item callback: {}'.format(which_item))
        self._clicked_item = which_item
        self.root.destroy()
        self._active = False

    def _dismiss_callback(self):
        """Menu dismissed."""
        logging.debug('popup: menu dismissed')
        if self._active is True:
            self._clicked_item = None
            self.root.destroy()

    def show(self, event):
        """Show popup."""
        self._clicked_item = None
        self.menu.tk_popup(event['x'], event['y']-50)
        self._active = True
        self.root.mainloop()
        return self._clicked_item


def create_and_show_menu(event, *menuitems):
    """Create a menu object and show."""
    menu_obj = PopupMenu()
    for menuitem in menuitems:
        menu_obj.add_menuitem(*menuitem)

    return menu_obj.show(event)
