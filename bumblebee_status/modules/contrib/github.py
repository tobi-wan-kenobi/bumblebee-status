# pylint: disable=C0111,R0903

"""
Displays the unread GitHub notifications count for a GitHub user using the following reasons:

    * https://developer.github.com/v3/activity/notifications/#notification-reasons

Uses `xdg-open` or `x-www-browser` to open web-pages.

Requires the following library:
    * requests

Parameters:
    * github.token: GitHub user access token, the token needs to have the 'notifications' scope.
    * github.interval: Interval in minutes between updates, default is 5.
    * github.reasons: Comma separated reasons to be parsed (e.g.: github.reasons=mention,team_mention,review_requested)

contributed by:
    * v1 - `yvesh <https://github.com/yvesh>`_ - many thanks!
    * v2 - `cristianmiranda <https://github.com/cristianmiranda>`_ - many thanks!
"""

import shutil
import requests

import core.module
import core.widget
import core.decorators
import core.input

import util.format


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.github))

        self.background = True
        self.__count = 0
        self.__label = ""
        self.__requests = requests.Session()
        self.__requests.headers.update(
            {"Authorization": "token {}".format(self.parameter("token", ""))}
        )

        self.__reasons = []
        reasons = self.parameter("reasons", "")
        if reasons:
            self.__reasons = util.format.aslist(reasons)

        cmd = "xdg-open"
        if not shutil.which(cmd):
            cmd = "x-www-browser"

        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd="{} https://github.com/notifications".format(cmd),
        )

    def github(self, _):
        return str(self.__label)

    def update(self):
        try:
            url = "https://api.github.com/notifications"
            notifications = self.__requests.get(url)

            total = self.__getTotalUnreadNotificationsCount(notifications)
            self.__count = total
            self.__label = str(total)

            counts = []
            if len(self.__reasons) > 0:
                for reason in self.__reasons:
                    unread = self.__getUnreadNotificationsCountByReason(
                        notifications, reason
                    )
                    counts.append(str(unread))

                self.__label += " - "
                self.__label += "/".join(counts)

        except Exception as err:
            self.__label = "n/a"

    def __getUnreadNotificationsCountByReason(self, notifications, reason):
        return len(
            list(
                filter(
                    lambda notification: notification["unread"]
                    and notification["reason"] == reason,
                    notifications.json(),
                )
            )
        )

    def __getTotalUnreadNotificationsCount(self, notifications):
        return len(
            list(
                filter(
                    lambda notification: notification["unread"], notifications.json()
                )
            )
        )

    def state(self, widget):
        state = []

        if self.__count > 0:
            state.append("warning")

        return state


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
