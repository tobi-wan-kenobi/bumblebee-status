# pylint: disable=C0111,R0903

"""My TEST

Requires the following executable:
    * arandr
    * xrandr
"""

import core.module
import core.widget
import core.input
import core.decorators


class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(""))

        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd="arandr",
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
