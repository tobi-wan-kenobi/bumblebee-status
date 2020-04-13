# pylint: disable=C0111,R0903

"""Displays APT package update information (<to upgrade>/<to remove >)
Requires the following debian packages:
    * python-parse
    * aptitude

"""

import threading
from parse import *

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

APT_CHECK_PATH = ("aptitude full-upgrade --simulate --assume-yes")
PATTERN = "{} packages upgraded, {} newly installed, {} to remove and {} not upgraded."

def parse_result(to_parse):
    # We want to line with the iforamtion about package upgrade
    line_to_parse = to_parse.split("\n")[-4]

    result = parse(PATTERN, line_to_parse)

    return int(result[0]), int(result[2])

def get_apt_check_info(widget):
    try:
        res = bumblebee.util.execute(APT_CHECK_PATH)
        widget.set("error", None)
    except (RuntimeError, FileNotFoundError) as e:
        widget.set("error", "unable to query APT: {}".format(e))
        return

    to_upgrade = 0
    to_remove = 0
    try:
        to_upgrade, to_remove = parse_result(res)
    except  e:
        widget.set("error", "parse error: {}".format(e))
        return

    widget.set("to_upgrade", to_upgrade)
    widget.set("to_remove", to_remove)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.updates)
        super(Module, self).__init__(engine, config, widget)
        self.interval_factor(60)
        self.interval(30)

    def updates(self, widget):
        result = []
        if widget.get("error"):
            return widget.get("error")
        for t in ["to_upgrade", "to_remove"]:
            result.append(str(widget.get(t, 0)))
        return "/".join(result)

    def update(self, widgets):
        thread = threading.Thread(target=get_apt_check_info, args=(widgets[0],))
        thread.start()

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
