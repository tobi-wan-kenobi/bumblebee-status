#pylint: disable=C0111,R0903

"""Opens a random xkcd comic in the browser."""

import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                bumblebee.output.Widget(full_text="xkcd")
        )
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                cmd="xdg-open https://c.xkcd.com/random/comic/"
        )
