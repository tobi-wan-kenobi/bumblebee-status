import datetime
import bumblebee.module
import subprocess

def description():
    return "Displays the current song and artist playing in cmus"

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._title = "None"
        self._artist = "None"
        self._status = 0

    def widgets(self):
        self._process = subprocess.Popen(["cmus-remote", "-Q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._query, self._error = self._process.communicate()
        self._query = self._query.decode("utf-8").split("\n")
        if b'cmus is not running' in self._error:
            return bumblebee.output.Widget(self, "-")
        for line in self._query:
            if "status playing" in line:
                self._status = 1
            if "status paused" in line:
                self._status = 2
            if "status stopped" in line:
                self._status = 3
            else:
                if "tag title" in line:
                    self._title = line[10:]
                if "tag artist" in line:
                    self._artist = line[11:]

        return bumblebee.output.Widget(self, "{} - {}".format(
            self._artist,
            self._title)
        )
    def state(self, widget):
        if self._status == 1:
            return "playing"
        if self._status == 2:
            return "paused"
        if self._status == 3:
            return "stopped"
        return "default"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
