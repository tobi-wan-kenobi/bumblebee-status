# pylint: disable=C0111,R0903

"""Displays the unread GitHub notifications for a GitHub user

Requires the following library:
    * requests

Parameters:
    * github.token: GitHub user access token, the token needs to have the 'notifications' scope.
    * github.interval: Interval in minutes between updates, default is 5.
"""

import shutil
import requests

import core.module
import core.widget
import core.decorators
import core.input

class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config):
        super().__init__(config, core.widget.Widget(self.github))

        self.__count = 0
        self.__requests = requests.Session()
        self.__requests.headers.update({'Authorization':'token {}'.format(self.parameter('token', ''))})

        cmd = 'xdg-open'
        if not shutil.which(cmd):
            cmd = 'x-www-browser'


        core.input.register(self, button=core.input.LEFT_MOUSE,
            cmd='{} https://github.com/notifications'.format(cmd))
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.update)

    def github(self, _):
        return str(self.__count)

    def update(self):
        try:
            self.__count = 0
            url = 'https://api.github.com/notifications'
            while True:
                notifications = self.__requests.get(url)
                self.__count += len(list(filter(lambda notification: notification['unread'], notifications.json())))
                next_link = notifications.links.get('next')
                if next_link is not None:
                    url = next_link.get('url')
                else:
                    break

        except Exception:
            self.__count = 'n/a'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
