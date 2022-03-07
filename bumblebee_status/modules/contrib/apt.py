# pylint: disable=C0111,R0903

"""Displays APT package update information (<to upgrade>/<to remove >)
Requires the following packages:

    * aptitude

contributed by `qba10 <https://github.com/qba10>`_ - many thanks!
"""

import re
import threading

import core.module
import core.widget
import core.decorators
import core.input

import util.cli

PATTERN = "{} packages upgraded, {} newly installed, {} to remove and {} not upgraded."


def parse_result(to_parse):
    # We want the line with the package upgrade information
    line_to_parse = to_parse.split("\n")[-4]
    result = re.search(
        r"(.+) packages upgraded, (.+) newly installed, (.+) to remove", line_to_parse
    )

    return int(result.group(1)), int(result.group(3))


def get_apt_check_info(module):
    widget = module.widget()
    try:
        res = util.cli.execute("aptitude full-upgrade --simulate --assume-yes")
        widget.set("error", None)
    except (RuntimeError, FileNotFoundError) as e:
        widget.set("error", "unable to query APT: {}".format(e))
        return

    to_upgrade = 0
    to_remove = 0
    try:
        to_upgrade, to_remove = parse_result(res)
        widget.set("to_upgrade", to_upgrade)
        widget.set("to_remove", to_remove)
    except Exception as e:
        widget.set("error", "parse error: {}".format(e))

    core.event.trigger("update", [module.id], redraw_only=True)


class Module(core.module.Module):
    @core.decorators.every(minutes=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.updates))
        self.__thread = None
        core.input.register(self, button=core.input.RIGHT_MOUSE,
                            cmd=self.updates)

    def updates(self, widget):
        if widget.get("error"):
            return widget.get("error")
        return "{} to upgrade, {} to remove".format(
            widget.get("to_upgrade", 0), widget.get("to_remove", 0)
        )

    def update(self):
        if self.__thread and self.__thread.is_alive():
            return

        self.__thread = threading.Thread(target=get_apt_check_info, args=(self,))
        self.__thread.start()

    def state(self, widget):
        cnt = 0
        ret = "good"
        for t in ["to_upgrade", "to_remove"]:
            cnt += widget.get(t, 0)
        if cnt > 50:
            ret = "critical"
        elif cnt > 0:
            ret = "warning"
        if widget.get("error"):
            ret = "critical"

        return ret


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
