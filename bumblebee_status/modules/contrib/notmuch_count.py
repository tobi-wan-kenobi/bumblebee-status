# pylint: disable=C0111,R0903

"""Displays the result of a notmuch count query
   default : unread emails which path do not contained 'Trash' (notmuch count 'tag:unread AND NOT path:/.*Trash.*/')

Parameters:
    * notmuch_count.query: notmuch count query to show result 

Errors:
    if the notmuch query failed, the shown value is  -1

Dependencies:
    notmuch (https://notmuchmail.org/)

contributed by `abdoulayeYATERA <https://github.com/abdoulayeYATERA>`_ - many thanks!
"""

import os

import core.module
import core.widget

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__notmuch_count_query = self.parameter(
            "query", "tag:unread AND NOT path:/.*Trash.*/"
        )

    def output(self, widget):
        return self.__notmuch_count

    def state(self, widgets):
        if self.__notmuch_count == 0:
            return "empty"
        return "items"

    def update(self):
        try:
            self.__notmuch_count = util.cli.execute(
                "notmuch count {}".format(self.__notmuch_count_query)
            ).strip()
        except Exception:
            self.__notmuch_count = "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
