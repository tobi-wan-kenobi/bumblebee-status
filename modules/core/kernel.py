# pylint: disable=C0111,R0903

"""Shows Linux kernel version information"""

import platform

import core.module
import core.widget
import core.decorators

class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config):
        super().__init__(config, core.widget.Widget(self.full_text))

    def full_text(self, widgets):
        return platform.release()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
