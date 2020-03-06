# pylint: disable=C0111,R0903

"""Shows Linux kernel version information"""

import platform

import core.module
import core.widget

class Module(core.module.Module):
    def __init__(self, config=None):
        super().__init__(config, core.widget.Widget(platform.release()))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
