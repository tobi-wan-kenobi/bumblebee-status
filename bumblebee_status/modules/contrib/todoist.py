# pylint: disable=C0111,R0903

"""
Displays the nº of Todoist tasks that are due:

    * https://developer.todoist.com/rest/v2/#get-active-tasks

Uses `xdg-open` or `x-www-browser` to open web-pages.

Requires the following library:
    * requests

Errors:
    if the Todoist get active tasks query failed, the shown value is `n/a`

Parameters:
    * todoist.token: Todoist api token, you can get it in https://todoist.com/app/settings/integrations/developer.
    * todoist.filter: a filter statement defined by Todoist (https://todoist.com/help/articles/introduction-to-filters), eg: "!assigned to: others & (Overdue | due: today)"
"""

import shutil

import requests

import core.decorators
import core.input
import core.module
import core.widget

HOST_API = "https://api.todoist.com"
HOST_WEBSITE = "https://todoist.com/app/today"

TASKS_URL = f"{HOST_API}/rest/v2/tasks"


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.todoist))

        self.__user_id = None
        self.background = True
        self.__label = ""

        token = self.parameter("token", "")
        self.__filter = self.parameter("filter", "")

        self.__requests = requests.Session()
        self.__requests.headers.update({"Authorization": f"Bearer {token}"})

        cmd = "xdg-open"
        if not shutil.which(cmd):
            cmd = "x-www-browser"

        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd=f"{cmd} {HOST_WEBSITE}",
        )

    def todoist(self, _):
        return self.__label

    def update(self):
        try:
            self.__label = self.__get_pending_tasks()
        except Exception:
            self.__label = "n/a"

    def __get_pending_tasks(self) -> str:
        params = {"filter": self.__filter} if self.__filter else None

        response = self.__requests.get(TASKS_URL, params=params)
        data = response.json()

        return str(len(data))
