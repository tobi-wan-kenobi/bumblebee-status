# pylint: disable=C0111,R0903

"""Displays DNF package update information (<security>/<bugfixes>/<enhancements>/<other>)

Requires the following executable:
    * dnf

"""

import core.event
import core.module
import core.widget
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(minutes=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.updates))

        self.background = True

    def updates(self, widget):
        result = []
        for t in ["security", "bugfixes", "enhancements", "other"]:
            result.append(str(widget.get(t, 0)))
        return "/".join(result)

    def update(self):
        widget = self.widget()
        res = util.cli.execute("dnf updateinfo", ignore_errors=True)

        security = 0
        bugfixes = 0
        enhancements = 0
        other = 0
        for line in res.split("\n"):
            if not line.startswith(" "):
                continue
            elif "ecurity" in line:
                for s in line.split():
                    if s.isdigit():
                        security += int(s)
            elif "ugfix" in line:
                for s in line.split():
                    if s.isdigit():
                        bugfixes += int(s)
            elif "hancement" in line:
                for s in line.split():
                    if s.isdigit():
                        enhancements += int(s)
            else:
                for s in line.split():
                    if s.isdigit():
                        other += int(s)

        widget.set("security", security)
        widget.set("bugfixes", bugfixes)
        widget.set("enhancements", enhancements)
        widget.set("other", other)


    def state(self, widget):
        cnt = 0
        for t in ["security", "bugfixes", "enhancements", "other"]:
            cnt += widget.get(t, 0)
        if cnt == 0:
            return "good"
        if cnt > 50 or widget.get("security", 0) > 0:
            return "critical"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
