# pylint: disable=C0111,R0903

"""Displays the unread GitHub notifications for a GitHub user

Requires the following library:
    * requests

Parameters:
    * github.token: GitHub user access token, the token needs to have the 'notifications' scope.
    * github.interval: Interval in minutes
"""

import time
import functools
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
        self._requests = requests.Session()
        self._requests.headers.update({"Authorization":"token {}".format(self.parameter("token", ""))})
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="x-www-browser https://github.com/notifications")
        immediate_update = functools.partial(self.update, immediate=True)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd=immediate_update)

    def github(self, _):
        return str(self._count)

    def update(self, _, immediate=False):
        if immediate or self._nextcheck < int(time.time()):
            self._nextcheck = int(time.time()) + self._interval * 60

            try:
                self._count = 0
                url = "https://api.github.com/notifications"
                while True:
                    notifications = self._requests.get(url)
                    self._count += len(filter(lambda notification: notification.get("unread", False), notifications.json()))
                    next_link = notifications.links.get('next')
                    if next_link is not None:
                        url = next_link.get('url')
                    else:
                        break

            except Exception:
                self._count = "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
