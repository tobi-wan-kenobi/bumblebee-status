# -*- coding: UTF-8 -*-

# smart function inspired by py-SMART https://github.com/freenas/py-SMART
# under Copyright (C) 2015 Marc Herndon and GPL2

"""Displays HDD smart status of different drives or all drives

Requires the following executables:
    * sudo
    * smartctl

Parameters:
    * smartstatus.display: how to display (defaults to 'combined', other choices: 'combined_singles', 'separate' or 'singles')
    * smartstatus.drives: in the case of singles which drives to display, separated comma list value, multiple accepted (defaults to 'sda', example:'sda,sdc')
    * smartstatus.show_names: boolean in the form of "True" or "False" to show the name of the drives in the form of sda, sbd, combined or none at all. 
"""

import os

import shutil

import core.module
import core.decorators

import util.cli
import util.format


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.devices = self.list_devices()
        self.display = self.parameter("display", "combined")
        self.drives = self.parameter("drives", "sda")
        self.show_names = util.format.asbool(self.parameter("show_names", True))
        self.create_widgets()

    def create_widgets(self):
        if self.display == "combined" or self.display == "combined_singles":
            widget = self.add_widget()
            widget.set("device", "combined")
            widget.set("assessment", self.combined())
            self.output(widget)
        else:
            for device in self.devices:
                if self.display == "singles" and device not in self.drives:
                    continue
                widget = self.add_widget()
                widget.set("device", device)
                widget.set("assessment", self.smart(device))
                self.output(widget)

    def update(self):
        for widget in self.widgets():
            device = widget.get("device")
            if device == "combined":
                widget.set("assessment", self.combined())
                self.output(widget)
            else:
                widget.set("assessment", self.smart(device))
                self.output(widget)

    def output(self, widget):
        device = widget.get("device")
        assessment = widget.get("assessment")
        if self.show_names:
            widget.full_text("{}: {}".format(device, assessment))
        else:
            widget.full_text("{}".format(assessment))

    def state(self, widget):
        states = []
        assessment = widget.get("assessment")
        if assessment == "Pre-fail":
            states.append("warning")
        if assessment == "Fail":
            states.append("critical")
        return states

    def combined(self):
        for device in self.devices:
            if self.display == "combined_singles" and device not in self.drives:
                    continue
            result = self.smart(device)
            if result == "Fail":
                return "Fail"
            if result == "Pre-fail":
                return "Pre-fail"
        return "OK"

    def list_devices(self):
        for (root, folders, files) in os.walk("/dev"):
            if root == "/dev":
                devices = {
                    "".join(filter(lambda i: i.isdigit() == False, file))
                    for file in files
                    if "sd" in file
                }
                nvme = {
                    file for file in files if ("nvme0n" in file and "p" not in file)
                }
                devices.update(nvme)
                return devices

    def smart(self, disk_name):
        smartctl = shutil.which("smartctl")
        assessment = None

        output = util.cli.execute(
            "sudo {} --health {}".format(smartctl, os.path.join("/dev/", disk_name))
        )
        output = output.split("\n")
        line = output[4]
        if "SMART" in line:
            if any([i in line for i in ["PASSED", "OK"]]):
                assessment = "OK"
            else:
                assessment = "Fail"

        if assessment == "OK":
            output = util.cli.execute(
                "sudo {} -A {}".format(smartctl, os.path.join("/dev/", disk_name))
            )
            output = output.split("\n")
            for line in output:
                if "Pre-fail" in line:
                    assessment = "Pre-fail"
        return assessment


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
