"""Displays currently active gpu by optimus-manager
Requires the following packages:

    * optimus-manager

"""

import subprocess

import core.module
import core.widget


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))
        self.__gpumode = ""

    def output(self, _):
        return "GPU: {}".format(self.__gpumode)

    def update(self):
        cmd = ["optimus-manager", "--print-mode"]
        output = (
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
            .communicate()[0]
            .decode("utf-8")
            .lower()
        )

        if "intel" in output:
            self.__gpumode = "Intel"
        elif "nvidia" in output:
            self.__gpumode = "Nvidia"
        elif "amd" in output:
            self.__gpumode = "AMD"
