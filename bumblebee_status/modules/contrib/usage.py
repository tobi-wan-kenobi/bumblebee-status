# pylint: disable=C0111,R0903

"""
Module for ActivityWatch (https://activitywatch.net/)
Displays the amount of time the system was used actively.

Requirements:
    * sqlite3 module for python
    * ActivityWatch

Errors:
    * when you get 'error: unable to open database file', modify the parameter 'database' to your ActivityWatch database file
    -> often found by running 'locate aw-server/peewee-sqlite.v2.db'

Parameters:
    * usage.database: path to your database file
    * usage.format: Specify what gets printed to the bar
    -> use 'HH', 'MM' or 'SS', they will get replaced by the number of hours, minutes and seconds, respectively

contributed by lasnikr (https://github.com/lasnikr)
"""

import sqlite3
import os

import core.module
import core.widget


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))
        self.__usage = ""

    def output(self, _):
        return "{}".format(self.__usage)

    def update(self):
        database_loc = self.parameter(
            "database", "~/.local/share/activitywatch/aw-server/peewee-sqlite.v2.db"
        )
        home = os.path.expanduser("~")

        database = sqlite3.connect(database_loc.replace("~", home))
        cursor = database.cursor()

        cursor.execute("SELECT key, id FROM bucketmodel")

        bucket_id = 1

        for tuple in cursor.fetchall():
            if "aw-watcher-afk" in tuple[1]:
                bucket_id = tuple[0]

        cursor.execute(
            f"SELECT duration, datastr FROM eventmodel WHERE bucket_id = {bucket_id} "
            + 'AND strftime("%Y,%m,%d", timestamp) = strftime("%Y,%m,%d", "now")'
        )

        duration = 0

        for tuple in cursor.fetchall():
            if '{"status": "not-afk"}' in tuple[1]:
                duration += tuple[0]

        hours = "%.0f" % (duration // 3600)
        minutes = "%.0f" % ((duration % 3600) // 60)
        seconds = "%.0f" % (duration % 60)

        formatting = self.parameter("format", "HHh, MMmin")
        self.__usage = (
            formatting.replace("HH", hours)
            .replace("MM", minutes)
            .replace("SS", seconds)
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
