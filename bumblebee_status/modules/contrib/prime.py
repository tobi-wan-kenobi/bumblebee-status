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
    * prime.nvidiastring: String to use when nvidia is selected (defaults to 'intel')
    * prime.intelstring: String to use when intel is selected (defaults to 'intel')

Requires the following executables:
    * sudo
    * prime-select

contributed by `jeffeb3 <https://github.com/jeffeb3>`_ - many thanks!
"""

import core.module
import core.widget
import core.input

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.query))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__chooseNvidia)
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.__chooseIntel)

        self.nvidiastring = self.parameter("nvidiastring", "nv")
        self.intelstring = self.parameter("intelstring", "it")

    def __chooseNvidia(self, event):
        util.cli.execute("sudo prime-select nvidia")

    def __chooseIntel(self, event):
        util.cli.execute("sudo prime-select intel")

    def query(self, widget):
        try:
            res = util.cli.execute("prime-select query")
        except RuntimeError:
            return "n/a"

        for line in res.split("\n"):
            if not line:
                continue
            if "nvidia" in line:
                return self.nvidiastring
            if "intel" in line:
                return self.intelstring
        return "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
