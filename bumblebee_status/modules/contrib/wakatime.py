# pylint: disable=C0111,R0903

"""
Displays the WakaTime daily/weekly/monthly times:

    * https://wakatime.com/developers#stats

Uses `xdg-open` or `x-www-browser` to open web-pages.

Requires the following library:
    * requests

Errors:
    if the Wakatime status query failed, the shown value is `n/a`

Parameters:
    * wakatime.token: Wakatime secret api key, you can get it in https://wakatime.com/settings/account.
    * wakatime.range: Range of the output, default is "Today". Can be one of “Today”, “Yesterday”, “Last 7 Days”, “Last 7 Days from Yesterday”, “Last 14 Days”, “Last 30 Days”, “This Week”, “Last Week”, “This Month”, or “Last Month”.
    * wakatime.format: Format of the output, default is "digital"
        Valid inputs are:
          * "decimal" -> 1.37
          * "digital" -> 1:22
          * "seconds" -> 4931.29
          * "text" -> 1 hr 22 mins
          * "%H:%M:%S" -> 01:22:31 (or any other valid format)
"""

import base64
import shutil
import time

import requests

import core.decorators
import core.input
import core.module
import core.widget

HOST_API = "https://wakatime.com"
SUMMARIES_URL = f"{HOST_API}/api/v1/users/current/summaries"
UTF8 = "utf-8"
FORMAT_PARAMETERS = ["decimal", "digital", "seconds", "text"]


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.wakatime))

        self.background = True
        self.__label = ""

        self.__output_format = self.parameter("format", "digital")
        self.__range = self.parameter("range", "Today")

        self.__requests = requests.Session()

        token = self.__encode_to_base_64(self.parameter("token", ""))
        self.__requests.headers.update({"Authorization": f"Basic {token}"})

        cmd = "xdg-open"
        if not shutil.which(cmd):
            cmd = "x-www-browser"

        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd=f"{cmd} {HOST_API}/dashboard",
        )

    def wakatime(self, _):
        return self.__label

    def update(self):
        try:
            self.__label = self.__get_waka_time(self.__range)
        except Exception:
            self.__label = "n/a"

    def __get_waka_time(self, since_date: str) -> str:
        response = self.__requests.get(f"{SUMMARIES_URL}?range={since_date}")

        data = response.json()
        grand_total = data["cumulative_total"]

        if self.__output_format in FORMAT_PARAMETERS:
            return str(grand_total[self.__output_format])
        else:
            total_seconds = int(grand_total["seconds"])
            return time.strftime(self.__output_format, time.gmtime(total_seconds))

    @staticmethod
    def __encode_to_base_64(s: str) -> str:
        return base64.b64encode(s.encode(UTF8)).decode(UTF8)
