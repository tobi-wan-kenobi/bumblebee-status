#pylint: disable=C0111,R0903

"""Opens a random xkcd comic in the browser."""

import core.module
import core.widget
import core.input
import core.decorators

class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config):
        super().__init__(config, core.widget.Widget('xkcd'))
        core.input.register(self, button=core.input.LEFT_MOUSE,
            cmd="xdg-open https://c.xkcd.com/random/comic/"
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
