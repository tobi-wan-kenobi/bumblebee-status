# pylint: disable=C0111,R0903

"""
Displays the GitLab todo count:

    * https://docs.gitlab.com/ee/user/todos.html
    * https://docs.gitlab.com/ee/api/todos.html

Uses `xdg-open` or `x-www-browser` to open web-pages.

Requires the following library:
    * requests

Errors:
    if the GitLab todo query failed, the shown value is `n/a`

Parameters:
    * gitlab.token: GitLab personal access token, the token needs to have the "read_api" scope.
    * gitlab.host: Host of the GitLab instance, default is "gitlab.com".
    * gitlab.actions: Comma separated actions to be parsed (e.g.: gitlab.actions=assigned,approval_required)
"""

import shutil

import requests

import core.decorators
import core.input
import core.module
import core.widget
import util


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.gitlab))

        self.background = True
        self.__label = ""
        self.__host = self.parameter("host", "gitlab.com")

        self.__actions = []
        actions = self.parameter("actions", "")
        if actions:
            self.__actions = util.format.aslist(actions)

        self.__requests = requests.Session()
        self.__requests.headers.update({"PRIVATE-TOKEN": self.parameter("token", "")})

        cmd = "xdg-open"
        if not shutil.which(cmd):
            cmd = "x-www-browser"

        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd="{cmd} https:/{host}//dashboard/todos".format(
                cmd=cmd, host=self.__host
            ),
        )

    def gitlab(self, _):
        return self.__label

    def update(self):
        try:
            url = "https://{host}/api/v4/todos".format(host=self.__host)
            response = self.__requests.get(url)
            todos = response.json()
            if self.__actions:
                todos = [t for t in todos if t["action_name"] in self.__actions]
            self.__label = str(len(todos))
        except Exception as e:
            self.__label = "n/a"

    def state(self, widget):
        state = []

        try:
            if int(self.__label) > 0:
                state.append("warning")
        except ValueError:
            pass
        return state

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
