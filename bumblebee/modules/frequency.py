# pylint: disable=C0111,R0903

"""Displays CPU frequency.
"""

import subprocess 
import bumblebee.input
import bumblebee.output
import bumblebee.engine

 
class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.frequency)
        )
        self._frequency = 0
        
    def frequency(self, widget):
        return self._frequency

    def getFrequency(self):
        cmd = "cpupower frequency-info  | grep \"Hz\" | grep \"current CPU\" | xargs |  cut -d ' ' -f 4-5"
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").rstrip()

    def update(self, widgets):
        self._frequency = self.getFrequency()        



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
