# pylint: disable=C0111,R0903

"""Displays focused i3 window title.

Requirements:
    * i3ipc

Parameters:
    * title.max : Maximum character length for title before truncating. Defaults to 64.
    * title.placeholder : Placeholder text to be placed if title was truncated. Defaults to '...'.
    * title.scroll : Boolean flag for scrolling title. Defaults to False
    * title.short : Boolean flag for short title. Defaults to False


contributed by `UltimatePancake <https://github.com/UltimatePancake>`_ - many thanks!
"""

import threading

try:
    import i3ipc
except ImportError:
    pass

no_title = "n/a"

import core.module
import core.decorators

import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        # parsing of parameters
        self.__scroll = util.format.asbool(self.parameter("scroll", False))
        self.__short = util.format.asbool(self.parameter("short", False))
        self.__max = int(self.parameter("max", 64))
        self.__placeholder = self.parameter("placeholder", "...")
        self.__title = ""

        # set output of the module
        self.add_widget(
            full_text=self.__scrolling_focused_title
            if self.__scroll
            else self.__focused_title
        )

        # create a connection with i3ipc
        self.__i3 = i3ipc.Connection()
        # event is called both on focus change and title change
        self.__i3.on("window", lambda __p_i3, __p_e: self.__pollTitle())
        # begin listening for events
        threading.Thread(target=self.__i3.main).start()

        # initialize the first title
        self.__pollTitle()

    def __focused_title(self, widget):
        return self.__title

    @core.decorators.scrollable
    def __scrolling_focused_title(self, widget):
        return self.__full_title

    def __pollTitle(self):
        """Updating current title."""
        try:
            focused = self.__i3.get_tree().find_focused().name
            self.__full_title = focused.split(
                "-")[-1].strip() if self.__short else focused
        except:
            self.__full_title = no_title
        if self.__full_title is None:
            self.__full_title = no_title

        if not self.__scroll:
            # cut the text if it is too long
            if len(self.__full_title) > self.__max:
                self.__title = self.__full_title[
                    0 : self.__max - len(self.__placeholder)
                ]
                self.__title = "{}{}".format(self.__title, self.__placeholder)
            else:
                self.__title = self.__full_title


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
