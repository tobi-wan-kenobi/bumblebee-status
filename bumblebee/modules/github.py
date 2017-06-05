# pylint: disable=C0111,R0903

"""Displays the unread GitHub notifications for a GitHub user

Requires the following executable:
    * curl

Parameters:
    * github.token: GitHub user access token
    * github.interval: Interval in minutes
"""

import time
import json
import bumblebee.input
import bumblebee.output
import bumblebee.engine

try:
    import requests
except ImportError:
    pass

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.github)
                                    )
        self._count = 0
        self._interval = int(self.parameter("interval", "5"))
        self._nextcheck = 0

    def github(self, _):
        return str(self._count)

    def update(self, widgets):
        if self._nextcheck < int(time.time()):
            self._nextcheck = int(time.time()) + self._interval * 60
            token = self.parameter("token", "")

            if not token:
                self._count = 0
                return
              
            notifications = requests.get("https://api.github.com/notifications", headers={"Authorization":"token {}".format(token)}).text
            unread = 0
            for notification in json.loads(notifications):
                if "unread" in notification and notification["unread"]:
                    unread += 1
            self._count = unread

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
