# pylint: disable=C0111,R0903

"""Displays APT package update information (<toupgrade>/<security>)
Requires the following debian packages:
    * update-notifier-common

"""

import threading

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

APT_CHECK_PATH = "/usr/lib/update-notifier/apt_check.py"

def get_apt_check_info(widget):
    try:
        res = bumblebee.util.execute(APT_CHECK_PATH)
    except RuntimeError:
        pass

    all_pkg = 0
    security = 0

    res_array = res.split(';')

    try:
        s = res_array[0]
        if s.isdigit(): all_pkg = int(s)

        s = res_array[1]
        if s.isdigit(): security = int(s)
    except:
        pass

    widget.set("all_pkg", all_pkg)
    widget.set("security", security)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.updates)
        super(Module, self).__init__(engine, config, widget)
        self.interval(30)

    def updates(self, widget):
        result = []
        for t in ["all_pkg", "security"]:
            result.append(str(widget.get(t, 0)))
        return "/".join(result)

    def update(self, widgets):
        thread = threading.Thread(target=get_apt_check_info, args=(widgets[0],))
        thread.start()

    def state(self, widget):
        cnt = 0
        ret = "good"
        for t in ["all_pkg", "security"]:
            cnt += widget.get(t, 0)
        if cnt > 50 or widget.get("security", 0) > 0:
            ret = "critical"
        elif cnt > 0:
            ret = "warning"

        return ret

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
