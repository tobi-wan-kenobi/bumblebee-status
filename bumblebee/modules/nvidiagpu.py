#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Displays GPU name, temperature and memory usage.

Requires nvidia-smi
"""

import subprocess
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self,engine,config):
        super(Module,self).__init__(engine,config,bumblebee.output.Widget(full_text=self.utilization))
        self._utilization = "Not found: 0 0/0"

    def utilization(self,widget):
        return self._utilization

    def update(self,widgets):
        sp = subprocess.Popen(['nvidia-smi', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_str = sp.communicate()
        out_list = out_str[0].decode("utf-8").split('\n')

        title = ""
        usedMem = ""
        totalMem = ""
        temp = ""
        name = "not found"
        for item in out_list:
            try:
                key, val = item.split(':')
                key, val = key.strip(), val.strip()
                if title == "FB Memory Usage":
                    if key == "Total":
                        totalMem = val
                    elif key == "Used":
                        usedMem = val.split(" ")[0]
                elif key == "GPU Current Temp":
                    temp = val.split(" ")[0]
                elif key == "Product Name":
                    name = val
            except:
                title = item.strip()
        self._utilization = u"%s: %s°C %s/%s"%(name,temp,usedMem,totalMem)
