# -*- coding: UTF-8 -*-

"""Displays sensor temperature and CPU frequency

Parameters:

    * sensors2.chip: 'sensors -u' compatible filter for chip to display (default to empty - show all chips)
    * sensors2.showcpu: Enable or disable CPU frequency display (default: true)
    * sensors2.showtemp: Enable or disable temperature display (default: true)
    * sensors2.showfan: Enable or disable fan display (default: true)
    * sensors2.showother: Enable or display 'other' sensor readings (default: false)
    * sensors2.showname: Enable or disable show of sensor name (default: false)
    * sensors2.chip_include: Comma-separated list of chip to include (defaults to '' will include all by default, example: 'coretemp,bat')
    * sensors2.chip_exclude:Comma separated list of chip to exclude (defaults to '' will exclude none by default)
    * sensors2.field_include: Comma separated list of chip to include (defaults to '' will include all by default, example: 'temp,fan')
    * sensors2.field_exclude: Comma separated list of chip to exclude (defaults to '' will exclude none by default)
    * sensors2.chip_field_exclude: Comma separated list of chip field to exclude (defaults to '' will exclude none by default, example: 'coretemp-isa-0000.temp1,coretemp-isa-0000.fan1')
    * sensors2.chip_field_include: Comma-separated list of adaper field to include (defaults to '' will include all by default)
"""

import re

import core.module
import core.widget

import util.cli
import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.__chip = self.parameter("chip", "")
        self.__data = {}
        self.__update()

        self.__create_widgets()

    def update(self):
        self.__update()
        for widget in self.widgets():
            self.__update_widget(widget)

    def state(self, widget):
        widget_type = widget.get("type", "")
        try:
            data = self.__data[widget.get("adapter")][widget.get("package")][
                widget.get("field")
            ]
            if "crit" in data and float(data["input"]) > float(data["crit"]):
                return ["critical", widget_type]
            if "max" in data and float(data["input"]) > float(data["max"]):
                return ["warning", widget_type]
        except:
            pass
        return [widget_type]

    def __create_widgets(self):
        show_temp = util.format.asbool(self.parameter("showtemp", True))
        show_fan = util.format.asbool(self.parameter("showfan", True))
        show_other = util.format.asbool(self.parameter("showother", False))
        include_chip = tuple(
            filter(len, util.format.aslist(self.parameter("chip_include", "")))
        )
        exclude_chip = tuple(
            filter(len, util.format.aslist(self.parameter("chip_exclude", "")))
        )
        include_field = tuple(
            filter(len, util.format.aslist(self.parameter("field_include", "")))
        )
        exclude_field = tuple(
            filter(len, util.format.aslist(self.parameter("field_exclude", "")))
        )
        include_chip_field = tuple(
            filter(len, util.format.aslist(self.parameter("chip_field_include", "")))
        )
        exclude_chip_field = tuple(
            filter(len, util.format.aslist(self.parameter("chip_field_exclude", "")))
        )

        if util.format.asbool(self.parameter("showcpu", True)):
            widget = self.add_widget(full_text=self.__cpu)
            widget.set("type", "cpu")

        for adapter in self.__data:
            if include_chip or exclude_chip:
                if include_chip:
                    if all([chip not in adapter for chip in include_chip]):
                        continue
                else:
                    if any([chip in adapter for chip in exclude_chip]):
                        continue

            if include_chip_field:
                try:
                    if all(
                        [i.split(".")[0] not in adapter for i in include_chip_field]
                    ):
                        continue
                except:
                    pass

            for package in self.__data[adapter]:
                if util.format.asbool(self.parameter("showname", False)):
                    widget = self.add_widget(full_text=package)
                    widget.set("data", self.__data[adapter][package])
                    widget.set("package", package)
                    widget.set("field", "")
                    widget.set("adapter", adapter)
                for field in self.__data[adapter][package]:

                    if include_field or exclude_field:
                        if include_field:
                            if all(
                                [included not in field for included in include_field]
                            ):
                                continue
                        else:
                            if any([excluded in field for excluded in exclude_field]):
                                continue

                    try:
                        if include_chip_field or exclude_chip_field:
                            if include_chip_field:
                                if all(
                                    [
                                        i.split(".")[1] not in field
                                        for i in include_chip_field
                                        if i.split(".")[0] in adapter
                                    ]
                                ):
                                    continue
                            else:
                                if any(
                                    [
                                        i.split(".")[1] in field
                                        for i in exclude_chip_field
                                        if i.split(".")[0] in adapter
                                    ]
                                ):
                                    continue
                    except:
                        pass

                    widget = None
                    if "temp" in field and show_temp:
                        # seems to be a temperature
                        widget = self.add_widget()
                        widget.set("type", "temp")
                    if "fan" in field and show_fan:
                        # seems to be a fan
                        widget = self.add_widget()
                        widget.set("type", "fan")
                    elif show_other:
                        # everything else
                        widget = self.add_widget()
                        widget.set("type", "other")
                    if widget:
                        widget.set("package", package)
                        widget.set("field", field)
                        widget.set("adapter", adapter)

    def __update_widget(self, widget):
        if widget.get("field", "") == "":
            return  # nothing to do
        data = self.__data[widget.get("adapter")][widget.get("package")][
            widget.get("field")
        ]
        if "temp" in widget.get("field"):
            widget.full_text("{:0.01f}°C".format(data["input"]))
        elif "fan" in widget.get("field"):
            widget.full_text("{:0.0f}RPM".format(data["input"]))
        else:
            widget.full_text("{:0.0f}".format(data["input"]))

    def __update(self):
        output = util.cli.execute(
            "sensors -u {}".format(self.__chip), ignore_errors=True
        )
        self.__data = self.__parse(output)

    def __parse(self, data):
        output = {}
        package = ""
        adapter = None
        chip = None
        for line in data.split("\n"):
            if "Adapter" in line:
                # new adapter
                line = line.replace("Adapter: ", "")
                output[chip + " " + line] = {}
                adapter = chip + " " + line
            chip = line  # default - line before adapter is always the chip
            if not adapter:
                continue
            key, value = (line.split(":") + ["", ""])[:2]
            if not line.startswith(" "):
                # assume this starts a new package
                if package in output[adapter] and output[adapter][package] == {}:
                    del output[adapter][package]
                output[adapter][key] = {}
                package = key
            else:
                # feature for this chip
                try:
                    name, variant = (key.strip().split("_", 1) + ["", ""])[:2]
                    if not name in output[adapter][package]:
                        output[adapter][package][name] = {}
                    if variant:
                        output[adapter][package][name][variant] = {}
                    output[adapter][package][name][variant] = float(value)
                except Exception as e:
                    pass
        return output

    def __cpu(self, _):
        mhz = None
        try:
            output = open(
                "/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq"
            ).read()
            mhz = int(float(output) / 1000.0)
        except:
            output = open("/proc/cpuinfo").read()
            m = re.search(r"cpu MHz\s+:\s+(\d+)", output)
            if m:
                mhz = int(m.group(1))
            else:
                m = re.search(r"BogoMIPS\s+:\s+(\d+)", output)
                if m:
                    return "{} BogoMIPS".format(int(m.group(1)))
        if not mhz:
            return "n/a"

        if mhz < 1000:
            return "{} MHz".format(mhz)
        else:
            return "{:0.01f} GHz".format(float(mhz) / 1000.0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
