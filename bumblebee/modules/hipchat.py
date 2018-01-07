"""Displays the unread messages count for an HipChat user

Requires the following library:
    * requests

Parameters:
    * hipchat.token: HipChat user access token, the token needs to have the 'View Messages' scope.
    * hipchat.interval: Refresh interval in minutes (defaults to 5)
"""

import functools
import bumblebee.input
import bumblebee.output
import bumblebee.engine

try:
    import requests
except ImportError:
    pass

HIPCHAT_API_URL = "https://www.hipchat.com/v2/readstate?expand=items.unreadCount"

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.output)
                                    )
        self._count = 0
        self.interval(5)

        self._requests = requests.Session()
        self._requests.headers.update({"Authorization":"Bearer {}".format(self.parameter("token", ""))})

        immediate_update = functools.partial(self.update, immediate=True)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=immediate_update)

    def output(self, _):
        return str(self._count)

    def update(self, _, immediate=False):
        try:
            self._count = 0
            items = self._requests.get(HIPCHAT_API_URL).json().get('items')
            self._count = sum([item.get('unreadCount').get('count') for item in items])

        except Exception:
            self._count = "n/a"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
