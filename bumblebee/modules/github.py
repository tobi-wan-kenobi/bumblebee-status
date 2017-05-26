# pylint: disable=C0111,R0903

"""Displays the unread GitHub notifications for a GitHub user

Requires the following executable:
    * curl

Parameters:
    * github.token: GitHub user access token
    * github.interval: Interval in minutes
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import re
import time

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.github)
        )
        self._count = 0
        self._interval = int(self.parameter("interval", "5"))
        self._nextcheck = 0

    def github(self, widget):
        return self._count

    def update(self, widgets):
        if self._nextcheck < int(time.time()):
            self._nextcheck = int(time.time()) + self._interval * 60
            token = self.parameter("token", "")

            if not token:
                 self._count = 0
                 return

            result = bumblebee.util.execute("curl -s https://api.github.com/notifications\?access_token\=" + token)

            pattern = 'unread'
            lines = '\n'.join(re.findall(r'^.*%s.*?$'%pattern,result,flags=re.M))

            self._count = len(lines.split('\n'))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
