# pylint: disable=C0111,R0903

"""My TEST

Requires the following executable:
    * arandr
    * xrandr
"""

from functools import partial
import logging

import core.module
import core.widget
import core.input
import core.decorators
import util.cli
from util import popup
from util.cli import execute


log = logging.getLogger(__name__)


class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(''))

        self.manager = self.parameter("manager", "arandr")
        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd=self.popup,
        )

        core.input.register(self, button=core.input.RIGHT_MOUSE,
                            cmd=self.popup)

    def popup(self, widget):
        """Create Popup that allows the user to control their displays in one
        of three ways: launch arandr, select a pre-set screenlayout, toggle a
        display.
        """
        log.info("arandr showing popup")
        menu = popup.menu()
        menu.add_menuitem("arandr",
            callback=partial(execute, self.manager)
        )

        menu.show(widget, 0, 0)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
