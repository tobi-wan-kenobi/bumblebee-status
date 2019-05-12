# pylint: disable=C0111,R0903

"""Displays the unread GitHub notifications for a GitHub user

Requires the following library:
    * requests

Parameters:
    * github.token: GitHub user access token, the token needs to have the 'notifications' scope.
    * github.interval: Interval in minutes between updates, default is 5.
"""

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
        self.interval(5)
        self._requests = requests.Session()
        self._requests.headers.update({"Authorization":"token {}".format(self.parameter("token", ""))})
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="x-www-browser https://github.com/notifications")
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=self.update)

    def github(self, _):
        return str(self._count)

    def update(self, _):
        try:
            self._count = 0
            url = "https://api.github.com/notifications"
            while True:
                notifications = self._requests.get(url)
                self._count += len(list(filter(lambda notification: notification['unread'], notifications.json())))
                next_link = notifications.links.get('next')
                if next_link is not None:
                    url = next_link.get('url')
                else:
                    break

        except Exception:
            self._count = "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
