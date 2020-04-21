# pylint: disable=C0111,R0903

"""Displays and changes the current selected prime video card

Left click will call 'sudo prime-select nvidia'
Right click will call 'sudo prime-select nvidia'

Running these commands without a password requires editing your sudoers file
(always use visudo, it's very easy to make a mistake and get locked out of your computer!)

sudo visudo -f /etc/sudoers.d/prime

Then put a line like this in there:

    user    ALL=(ALL) NOPASSWD: /usr/bin/prime-select

If you can't figure out the sudoers thing, then don't worry, it's still really useful.

Parameters:
    * prime.nvidiastring: String to use when nvidia is selected (defaults to "intel")
    * prime.intelstring: String to use when intel is selected (defaults to "intel")

Requires the following executable:
    * prime-select

"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.query)
        )
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._chooseNvidia)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd=self._chooseIntel)

        self.nvidiastring = self.parameter("nvidiastring", "nv")
        self.intelstring = self.parameter("intelstring", "it")

    def _chooseNvidia(self, event):
        bumblebee.util.execute("sudo prime-select nvidia")

    def _chooseIntel(self, event):
        bumblebee.util.execute("sudo prime-select intel")

    def _prev_keymap(self, event):
        self._set_keymap(-1)

    def query(self, widget):
        try:
            res = bumblebee.util.execute("prime-select query")
        except RuntimeError:
            return "n/a"

        for line in res.split("\n"):
            if not line: continue
            if "nvidia" in line:
                return self.nvidiastring
            if "intel" in line:
                return self.intelstring
        return "n/a"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
