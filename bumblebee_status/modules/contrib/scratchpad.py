# pylint: disable=C0111,R0903

"""Displays a count of windows on the scratchpad, Left click to launch a rofi window picker for scratchpads

Requirements:
    * i3ipc
    * python-rofi

contributed by `theymightbetim <https://github.com/theymightbetim>`
"""

import threading

try:
    import i3ipc
except ImportError:
    pass

import core.module
import core.widget
import core.input

from util.rofi import showScratchpads


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.__getTitle))
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=showScratchpads)

        self.__scratchpads = 0
        self.__title = f"{self.__scratchpads}"
        # create a connection with i3ipc
        self.__i3 = i3ipc.Connection()
        self.__pollScratchpads()
        # event is called both on fFocus change and title change, and on workspace change
        for event in ["window::move", "window::urgent"]:
            self.__i3.on(event, self.__pollScratchpads)
        # begin listening for events
        threading.Thread(target=self.__i3.main).start()

    def __getTitle(self, widget):
        return self.__title

    def __pollScratchpads(self, *args, **kwargs):
        root = self.__i3.get_tree()
        scratchpad = root.scratchpad()
        if not scratchpad:
            return

        leaves = getattr(scratchpad, "floating_nodes", [])

        count = len(leaves)

        if count != self.__scratchpads:
            self.__scratchpads = count
            self.__title = f"{self.__scratchpads}"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
