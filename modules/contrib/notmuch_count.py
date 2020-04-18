# pylint: disable=C0111,R0903

"""Displays the result of a notmuch count query
   default : unread emails which path do not contained "Trash" (notmuch count "tag:unread AND NOT path:/.*Trash.*/")

Parameters:
    * notmuch_count.query: notmuch count query to show result 

Errors:
    if the notmuch query failed, the shown value is  -1

Dependencies:
    notmuch (https://notmuchmail.org/)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import os

class Module(bumblebee.engine.Module):


    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._notmuch_count_query = self.parameter("query", "tag:unread AND NOT path:/.*Trash.*/")
        self._notmuch_count = self.count_notmuch()


    def output(self, widget):
       self._notmuch_count = self.count_notmuch()
       return  str(self._notmuch_count)


    def state(self, widgets):
        if self._notmuch_count == 0:
            return "empty"
        return "items"


    def count_notmuch(self):
        try:
            notmuch_count_cmd = "notmuch count " + self._notmuch_count_query
            notmuch_count = int(bumblebee.util.execute(notmuch_count_cmd))
            return notmuch_count
        except Exception:
            return -1

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
