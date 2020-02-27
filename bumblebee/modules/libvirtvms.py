"""Displays count of running libvirt VMs.
Required the following python packages:
        * libvirt
        * sys
"""
import sys
import libvirt
import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.status)
            )
        self._status = self.status
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="virt-manager")

    def update(self, widgets):
        self._status = self.status

    def status(self, _):
        conn = None
        conn = libvirt.openReadOnly(None)
        if conn == None:
            print ('Failed to open connection to the hypervisor')
        return "VMs %s" % (conn.numOfDomains())
