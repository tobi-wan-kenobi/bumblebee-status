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

#list of repositories the last one sould always be other
repos = ["community", "core", "extra", "other"]

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.updates)
        )
        self._count = 0

    def updates(self, widget):
        return '/'.join(map(lambda x: str(widget.get(x,0)), repos))

    def update(self, widgets):
        path = os.path.dirname(os.path.abspath(__file__))
        if self._count == 0:
            try:
                result = bumblebee.util.execute("{}/../../bin/pacman-updates".format(path))

                count = len(repos)*[0]

                for line in result.splitlines():
                    if line.startswith("http"):
                        for i in range(len(repos)-1):
                            if "/" + repos[i] + "/" in line:
                                count[i] += 1
                                break
                        else:
                            result[-1] += 1

                for i in range(len(repos)):
                    widgets[0].set(repos[i], count[i])

            except BaseException as a:
                raise a
 
        # TODO: improve this waiting mechanism a bit
        self._count += 1
        self._count = 0 if self._count > 300 else self._count

    def state(self, widget):
        sumUpdates = sum(map(lambda x: widget.get(x,0), repos))
        if sumUpdates > 0:
            return "critical"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
