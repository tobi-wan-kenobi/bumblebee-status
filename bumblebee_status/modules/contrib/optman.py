"""Displays currently active gpu by optimus-manager
Requires the following packages:

    * optimus-manager

"""

import core.module
import core.widget

import util.cli

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))
        self.__gpumode = ""

    def output(self, _):
        return "GPU: {}".format(self.__gpumode)

    def update(self):
        cmd = "optimus-manager --print-mode"
        output = util.cli.execute(cmd).strip()

        if "intel" in output:
            self.__gpumode = "Intel"
        elif "nvidia" in output:
            self.__gpumode = "Nvidia"
        elif "amd" in output:
            self.__gpumode = "AMD"
