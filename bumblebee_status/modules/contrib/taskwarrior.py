"""Displays the number of pending tasks in TaskWarrior.

Requires the following library:
    * taskw

Parameters:
    * taskwarrior.taskrc : path to the taskrc file (defaults to ~/.taskrc)


contributed by `chdorb <https://github.com/chdorb>`_ - many thanks!
"""

from taskw import TaskWarrior

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__pending_tasks = "0"

    def update(self):
        """Return a string with the number of pending tasks from TaskWarrior."""
        try:
            taskrc = self.parameter("taskrc", "~/.taskrc")
            show_active = self.parameter("show_active", False)
            w = TaskWarrior(config_filename=taskrc)
            active_tasks = (
                w.filter_tasks({"start.any": "", "status": "pending"}) or None
            )
            if show_active and active_tasks:
                reporting_tasks = (
                    f"{active_tasks[0]['id']} - {active_tasks[0]['description']}"
                )
            else:
                reporting_tasks = len(w.filter_tasks({"status": "pending"}))
            self.__pending_tasks = reporting_tasks
        except:
            self.__pending_tasks = "n/a"

    @core.decorators.scrollable
    def output(self, _):
        """Format the task counter to output in bumblebee."""
        return "{}".format(self.__pending_tasks)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
