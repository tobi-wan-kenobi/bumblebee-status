"""Displays the status of Gentoo portage operations.

Parameters:
    * portage_status.logfile: logfile for portage (default is /var/log/emerge.log)

contributed by `andrewreisner <https://github.com/andrewreisner>`_ - many thanks!
"""

import os

import core.module
import core.widget


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))
        self.__logfile = self.parameter("logfile", "/var/log/emerge.log")
        self.clear()

    def clear(self):
        self.__action = ""
        self.__package = ""
        self.__status = ""

    def output(self, widget):
        return " ".join(
            [
                atom
                for atom in (self.__action, self.__package, self.__status)
                if atom != ""
            ]
        )

    def state(self, widgets):
        if self.__action == "":
            return "idle"
        return "active"

    def update(self):
        try:
            with open(self.__logfile, "rb") as f:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
                last_line = f.readline().decode()
                if "===" in last_line:
                    if "Unmerging..." in last_line:
                        self.__action = "Unmerging"
                        package_beg = last_line.find("(") + 1
                        package_end = last_line.find("-", last_line.find("/")) - 1
                        self.__package = last_line[package_beg : package_end + 1]
                    else:  # merging
                        status_beg = last_line.find("(")
                        status_end = last_line.find(")")
                        self.__status = last_line[status_beg : status_end + 1]
                        package_beg = last_line.find("(", status_end) + 1
                        package_end = (
                            package_beg
                            + last_line[package_beg:].find(
                                "-", last_line[package_beg:].find("/")
                            )
                            - 1
                        )
                        self.__package = last_line[package_beg : package_end + 1]
                        action_beg = status_end + 2
                        action_end = package_beg - 3
                        self.__action = last_line[action_beg : action_end + 1]
                else:
                    self.clear()
        except Exception:
            self.clear()
