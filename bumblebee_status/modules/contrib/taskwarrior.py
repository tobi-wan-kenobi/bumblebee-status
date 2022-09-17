"""Displays the number of pending tasks in TaskWarrior.

Requires the following library:
    * taskw

Parameters:
    * taskwarrior.taskrc : path to the taskrc file (defaults to ~/.taskrc)
    * taskwarrior.show_active: true/false(default) to show the active task ID and description when one is active, otherwise show the total number pending.


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
        self.__status = "stopped"

    def update(self):
        """Return a string with the number of pending tasks from TaskWarrior
        or the descripton of an active task.

        if show.active is set in the config, show the description of the
        current active task, otherwise the number of pending tasks will be displayed.
        """
        try:
            taskrc = self.parameter("taskrc", "~/.taskrc")
            show_active = self.parameter("show_active", False)
            w = TaskWarrior(config_filename=taskrc)
            active_tasks = (
                w.filter_tasks({"start.any": "", "status": "pending"}) or None
            )
            if show_active and active_tasks:
                # this is using the first element of the list, if there happen
                # to be other active tasks, they won't be displayed.
                reporting_tasks = (
                    f"{active_tasks[0]['id']} - {active_tasks[0]['description']}"
                )
                self.__status = "active"
            else:
                reporting_tasks = len(w.filter_tasks({"status": "pending"}))
                self.__status = "stopped"
            self.__pending_tasks = reporting_tasks
        except:
            self.__pending_tasks = "n/a"
            self.__status = "stopped"

    @core.decorators.scrollable
    def output(self, _):
        """Format the task counter to output in bumblebee."""
        return "{}".format(self.__pending_tasks)

    def state(self, widget):
        """Return the set status to reflect state"""
        return self.__status


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
