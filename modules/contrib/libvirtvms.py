"""Displays count of running libvirt VMs.

Required the following python packages:
        * libvirt

contributed by `maxpivo <https://github.com/maxpivo>`_ - many thanks!
"""

import sys
import libvirt

import core.module
import core.widget
import core.input
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(seconds=10)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.status))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd="virt-manager")

    def status(self, _):
        conn = libvirt.openReadOnly(None)
        if conn == None:
            return "Failed to open connection to the hypervisor"
        return "VMs %s" % (conn.numOfDomains())


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
