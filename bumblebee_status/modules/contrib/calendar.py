# pylint: disable=C0111,R0903

"""Extended version of datetime module which displays a small popup calendar and can open google calendar in the browser
Parameters:
    * calendar.format: strftime()-compatible formatting string
    * calendar.locale: locale to use rather than the system default
    * calendar.bg: background colors. default black.
    * calendar.fg: foreground colors. default white.
    * calendar.browserpath: path to broweser. default /usr/bin/firefox

"""

from __future__ import absolute_import
from bumblebee_status.modules.core.datetime import Module
import os

import core.module
import core.widget
import core.input
import datetime
import locale

def get_default_browser_linux():
    try:
        command = "xdg-settings get default-web-browser"
        process = os.popen(command)
        browser_id = process.read().strip()

        if browser_id:
            # Convert .desktop ID to a more user-friendly name (basic handling)
            if ".desktop" in browser_id:
                browser_name = browser_id.replace(".desktop", "")
                return browser_name

            # If it doesn't look like a .desktop id, return as is
            return browser_id
        else:
            return None
    except:
        return None
    
class Module(Module):
    def __init__(self, config, theme, dtlibrary=None):
        super().__init__(config, theme)

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.display_calendar
        )
        
    def display_calendar(self, widget):
        default_browser = get_default_browser_linux()
        import tkinter as tk
        from tkcalendar import Calendar

        root = tk.Tk()
        window_width = 300
        window_height = 205

        bg = self.parameter("bg", "black")
        fg = self.parameter("fg", "white")
        root.configure(bg=bg)

        # Get screen width
        screen_width = root.winfo_screenwidth()
        x = screen_width - window_width
        y = 20

        # Set the geometry of the window
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        root.title(f"{month} {year}")

        def close_window():
            root.destroy()

        close_button = tk.Button(
            root, text="X", bg="black", fg="white", command=close_window
        )
        close_button.place(x=290, y=0, width=10, height=10)

        # Calendar widget

        cal = Calendar(
            root,
            background=bg,
            foreground=fg,
            disabledbackground=bg,
            bordercolor=bg,
            headersbackground=bg,
            headersforeground=fg,
            normalbackground=bg,
            normalforeground=fg,
            weekendbackground=bg,
            weekendforeground=fg,
            othermonthforeground="grey",
            othermonthbackground=bg,
            othermonthwebackground=bg,
            othermonthweforground="grey",
            showweeknumbers=False,
        )
        cal.place(x=0, y=10, width=300, height=200)

        def key_listener(event):
            if event.keysym == "Escape":
                close_window()
            if event.keysym == "Return":
                import subprocess

                selected_date = cal.selection_get()
                browser_path = self.parameter("browserpath", "/usr/bin/firefox")
                url = f"https://calendar.google.com/calendar/u/0/r/day/{selected_date.strftime('%Y/%m/%d')}"
                subprocess.Popen([browser_path, url], stdout=subprocess.DEVNULL)
                close_window()
                return self.full_text

        root.bind("<KeyRelease>", key_listener)
        root.mainloop()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
