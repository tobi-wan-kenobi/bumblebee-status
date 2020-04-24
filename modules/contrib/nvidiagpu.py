# -*- coding: utf-8 -*-

"""Displays GPU name, temperature and memory usage.

Parameters:
   * nvidiagpu.format: Format string (defaults to "{name}: {temp}°C %{usedmem}/{totalmem} MiB")
                       Available values are: {name} {temp} {mem_used} {mem_total} {fanspeed} {clock_gpu} {clock_mem}

Requires nvidia-smi
"""

import subprocess
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config, bumblebee.output.Widget(full_text=self.utilization))
        self._utilization = "Not found: 0 0/0"

    def utilization(self, widget):
        return self._utilization

    def update(self, widgets):
        sp = subprocess.Popen(['nvidia-smi', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_str = sp.communicate()
        out_list = out_str[0].decode("utf-8").split('\n')

        title = ""
        usedMem = ""
        totalMem = ""
        temp = ""
        name = "not found"
        clockMem = ""
        clockGpu = ""
        fanspeed = ""
        for item in out_list:
            try:
                key, val = item.split(':')
                key, val = key.strip(), val.strip()
                if title == "Clocks":
                    if key == "Graphics":
                        clockGpu = val.split(" ")[0]
                    elif key == "Memory":
                        clockMem = val.split(" ")[0]
                if title == "FB Memory Usage":
                    if key == "Total":
                        totalMem = val.split(" ")[0]
                    elif key == "Used":
                        usedMem = val.split(" ")[0]
                elif key == "GPU Current Temp":
                    temp = val.split(" ")[0]
                elif key == "Product Name":
                    name = val
                elif key == "Fan Speed":
                    fanspeed = val.split(" ")[0]

            except:
                title = item.strip()

        str_format = self.parameter("format", '{name}: {temp}°C {mem_used}/{mem_total} MiB')
        self._utilization = str_format.format(
                name = name,
                temp = temp,
                mem_used = usedMem,
                mem_total = totalMem,
                clock_gpu = clockGpu,
                clock_mem = clockMem,
                fanspeed = fanspeed,
            )
