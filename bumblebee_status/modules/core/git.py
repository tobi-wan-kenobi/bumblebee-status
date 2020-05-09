# pylint: disable=C0111,R0903

"""Print the branch and git status for the
currently focused window.

Requires:
    * xcwd
    * Python module 'pygit2'
"""

import os
import pygit2

import core.module

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.__error = False

    def hidden(self):
        return self.__error

    def update(self):
        state = {}
        self.clear_widgets()
        try:
            directory = util.cli.execute("xcwd").strip()
            directory = self.__get_git_root(directory)
            repo = pygit2.Repository(directory)

            self.add_widget(name="git.main", full_text=repo.head.shorthand)

            for filepath, flags in repo.status().items():
                if (
                    flags == pygit2.GIT_STATUS_WT_NEW
                    or flags == pygit2.GIT_STATUS_INDEX_NEW
                ):
                    state["new"] = True
                if (
                    flags == pygit2.GIT_STATUS_WT_DELETED
                    or flags == pygit2.GIT_STATUS_INDEX_DELETED
                ):
                    state["deleted"] = True
                if (
                    flags == pygit2.GIT_STATUS_WT_MODIFIED
                    or flags == pygit2.GIT_STATUS_INDEX_MODIFIED
                ):
                    state["modified"] = True
            self.__error = False
            if "new" in state:
                self.add_widget(name="git.new")
            if "modified" in state:
                self.add_widget(name="git.modified")
            if "deleted" in state:
                self.add_widget(name="git.deleted")

        except Exception as e:
            self.__error = True

    def state(self, widget):
        return widget.name.split(".")[1]

    def __get_git_root(self, directory):
        while len(directory) > 1:
            if os.path.exists(os.path.join(directory, ".git")):
                return directory
            directory = "/".join(directory.split("/")[0:-1])
        return "/"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
