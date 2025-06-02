# pylint: disable=C0111,R0903

"""Print the branch and git status for the
currently focused window.

Requires:
    * xcwd
    * Python module 'pygit2'

Parameters:
    * git.draw_order: String to specify draw order of the widgets; Options are "ltr" for left to right, and "rtl" for right to left (defaults to "ltr")
"""

import os
import pygit2

import core.module

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self._draw_order = self.parameter("draw_order", "ltr")
        if self._draw_order not in [ "ltr", "rtl" ]:
            self.__error = True
        else:
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

            for info in self._get_widget_infos(repo):
                self.add_widget(name=info[0], full_text=info[1])
            
            self.__error = False
        
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

    def _get_widget_infos(self, repo):
        widget_infos = [ ("git.main", repo.head.shorthand) ]
        state = {}
        for _, flags in repo.status().items():
            if flags & (pygit2.GIT_STATUS_WT_NEW | pygit2.GIT_STATUS_INDEX_NEW):
                state["new"] = True
            if flags & (pygit2.GIT_STATUS_WT_DELETED | pygit2.GIT_STATUS_INDEX_DELETED):
                state["deleted"] = True
            if flags & (pygit2.GIT_STATUS_WT_MODIFIED | pygit2.GIT_STATUS_INDEX_MODIFIED):
                state["modified"] = True
        
        if "new" in state:
            widget_infos.append(("git.new", ""))
        if "modified" in state:
            widget_infos.append(("git.modified", ""))
        if "deleted" in state:
            widget_infos.append(("git.deleted", ""))

        if self._draw_order == "ltr":
            return widget_infos
        elif self._draw_order == "rtl":
            return reversed(widget_infos)

        raise RuntimeError("Draw order is not specified correctly")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
