"""Display information about the currently running emerge process.

Requires the following executable:
    * emerge

Parameters:
    * emerge_status.format: Format string (defaults to '{current}/{total} {action} {category}/{pkg}')

This code is based on emerge_status module from p3status [1] original created by AnwariasEu.

[1] https://github.com/ultrabug/py3status/blob/master/py3status/modules/emerge_status.py 
"""

import re
import copy

import core.module
import core.widget
import core.decorators

import util.cli
import util.format


class Module(core.module.Module):
    @core.decorators.every(seconds=10)
    def __init__(self, config, theme):
        super().__init__(config, theme, [])
        self.__format = self.parameter(
            "format", "{current}/{total} {action} {category}/{pkg}"
        )
        self.__ret_default = {
            "action": "",
            "category": "",
            "current": 0,
            "pkg": "",
            "total": 0,
        }

    def update(self):
        response = {}
        ret = copy.deepcopy(self.__ret_default)
        if self.__emerge_running():
            ret = self.__get_progress()

            widget = self.widget("status")
            if not widget:
                widget = self.add_widget(name="status")

            if ret["total"] == 0:
                widget.full_text("emrg calculating...")
            else:
                widget.full_text(
                    " ".join(
                        self.__format.format(
                            current=ret["current"],
                            total=ret["total"],
                            action=ret["action"],
                            category=ret["category"],
                            pkg=ret["pkg"],
                        ).split()
                    )
                )
        else:
            self.clear_widgets()

    def __emerge_running(self):
        """
        Check if emerge is running.
        Returns true if at least one instance of emerge is running.
        """
        try:
            util.cli.execute("pgrep emerge")
            return True
        except Exception:
            return False

    def __get_progress(self):
        """
        Get current progress of emerge.
        Returns a dict containing current and total value.
        """
        input_data = []
        ret = {}

        # traverse emerge.log from bottom up to get latest information
        last_lines = util.cli.execute("tail -50 /var/log/emerge.log")
        input_data = last_lines.split("\n")
        input_data.reverse()

        for line in input_data:
            if "*** terminating." in line:
                # copy content of ret_default, not only the references
                ret = copy.deepcopy(self.__ret_default)
                break
            else:
                status_re = re.compile(
                    r"\((?P<cu>[\d]+) of (?P<t>[\d]+)\) "
                    r"(?P<a>[a-zA-Z/]+( [a-zA-Z]+)?) "
                    r"\((?P<ca>[\w\-]+)/(?P<p>[\w.]+)"
                )
                res = status_re.search(line)
                if res is not None:
                    ret["action"] = res.group("a").lower()
                    ret["category"] = res.group("ca")
                    ret["current"] = res.group("cu")
                    ret["pkg"] = res.group("p")
                    ret["total"] = res.group("t")
                    break
        return ret


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
