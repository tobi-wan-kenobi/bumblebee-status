# -*- coding: utf-8 -*-

"""Displays GPU name, temperature and memory usage.

Parameters:
   * nvidiagpu.format: Format string (defaults to '{name}: {temp}°C %{usedmem}/{totalmem} MiB')
     Available values are: {name} {temp} {mem_used} {mem_total} {fanspeed} {clock_gpu} {clock_mem}

Requires nvidia-smi

contributed by `RileyRedpath <https://github.com/RileyRedpath>`_ - many thanks!
"""

import core.module
import core.widget

import util.cli
import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.utilization))

        self.__utilization = "Not found: 0 0/0"

    def utilization(self, widget):
        return self.__utilization

    def hidden(self):
        return "not found" in self.__utilization

    def update(self):
        sp = util.cli.execute("nvidia-smi -q", ignore_errors=True)

        title = ""
        usedMem = ""
        totalMem = ""
        temp = ""
        name = "not found"
        clockMem = ""
        clockGpu = ""
        fanspeed = ""
        for item in sp.split("\n"):
            try:
                key, val = item.split(":")
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

        str_format = self.parameter(
            "format", "{name}: {temp}°C {mem_used}/{mem_total} MiB"
        )
        self.__utilization = str_format.format(
            name=name,
            temp=temp,
            mem_used=usedMem,
            mem_total=totalMem,
            clock_gpu=clockGpu,
            clock_mem=clockMem,
            fanspeed=fanspeed,
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
