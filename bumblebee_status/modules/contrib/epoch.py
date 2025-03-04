"""Displays the current epoch timestamp

* Requires: 
    * xclip for click to copy to clipboard

contributed by `theymightbetim <https://github.com/theymightbetim>`
"""

import core.module
import core.widget
import core.input

import time


class Module(core.module.Module):

    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.copy_to_clipboard
        )

    def full_text(self, widget):
        return int(time.time())

    def copy_to_clipboard(self, event):
        import subprocess

        epoch = str(int(time.time()))
        subprocess.Popen(["xclip", "-i"], stdin=subprocess.PIPE).communicate(
            epoch.encode("utf-8")
        )
