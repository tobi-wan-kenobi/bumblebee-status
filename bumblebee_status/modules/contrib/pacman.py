# pylint: disable=C0111,R0903

"""Displays update information per repository for pacman.

Parameters:
    * pacman.sum: If you prefer displaying updates with a single digit (defaults to 'False')

Requires the following executables:
    * fakeroot
    * pacman

contributed by `Pseudonick47 <https://github.com/Pseudonick47>`_ - many thanks!
"""

import os
import threading

import core.module
import core.widget
import core.decorators

import util.cli
import util.format

from bumblebee_status.discover import utility

# list of repositories.
# the last one should always be other
repos = ["core", "extra", "community", "multilib", "testing", "other"]


def get_pacman_info(widget, path):
    cmd = utility("pacman-updates")
    result = util.cli.execute(cmd, ignore_errors=True)

    count = len(repos) * [0]

    for line in result.splitlines():
        if line.startswith(("http", "rsync")):
            for i in range(len(repos) - 1):
                if "/" + repos[i] + "/" in line:
                    count[i] += 1
                    break
            else:
                result[-1] += 1

    for i in range(len(repos)):
        widget.set(repos[i], count[i])
    core.event.trigger("update", [widget.module.id], redraw_only=True)


class Module(core.module.Module):
    @core.decorators.every(minutes=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.updates))

    def updates(self, widget):
        if util.format.asbool(self.parameter("sum")):
            return str(sum(map(lambda x: widget.get(x, 0), repos)))
        return "/".join(map(lambda x: str(widget.get(x, 0)), repos))

    def update(self):
        path = os.path.dirname(os.path.abspath(__file__))
        thread = threading.Thread(target=get_pacman_info, args=(self.widget(), path))
        thread.start()

    def state(self, widget):
        weightedCount = sum(
            map(lambda x: (len(repos) - x[0]) * widget.get(x[1], 0), enumerate(repos))
        )

        if weightedCount < 10:
            return "good"

        return self.threshold_state(weightedCount, 100, 150)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
