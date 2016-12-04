# pylint: disable=C0111,R0903

"""Test module"""

import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine):
        super(Module, self).__init__(engine)

    def widgets(self):
        return []

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
