# pylint: disable=C0111,R0903

"""Displays update information per repository for pacman."

Requires the following executables:
    * fakeroot
    * pacman
"""

import os
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.updates)
        )
        self._count = 0
        self._out = ""

    def updates(self, widget):
        return self._out

    def update(self, widgets):
        path = os.path.dirname(os.path.abspath(__file__))
        if self._count == 0:
            self._out = "?/?/?/?"
            try:
                result = bumblebee.util.execute("{}/../../bin/pacman-updates".format(path))
                self._community = 0
                self._core = 0
                self._extra = 0
                self._other = 0

                for line in result.splitlines():
                    if line.startswith("http"):
                        if "community" in line:
                            self._community += 1
                            continue
                        if "core" in line:
                            self._core += 1;
                            continue
                        if "extra" in line:
                            self._extra += 1
                            continue
                        self._other += 1
                self._out = str(self._core)+"/"+str(self._extra)+"/"+str(self._community)+"/"+str(self._other)
            except RuntimeError:
                self._out = "?/?/?/?"
 
        # TODO: improve this waiting mechanism a bit
        self._count += 1
        self._count = 0 if self._count > 300 else self._count

    def sumUpdates(self):
        return self._core + self._community + self._extra + self._other 
    
    def state(self, widget):
        if self.sumUpdates() > 0:
            return "critical"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
