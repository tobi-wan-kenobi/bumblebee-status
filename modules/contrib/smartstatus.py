# -*- coding: UTF-8 -*-

# smart function inspired by py-SMART https://github.com/freenas/py-SMART
# under Copyright (C) 2015 Marc Herndon and GPL2

"""Displays HDD smart status of different drives or all drives

Parameters:
    * smartstatus.display: how to display (defaults to "combined", other choices: "seperate" or "singles")
    * smartstauts.drives: in the case of singles which drives to display, separated comma list value, multiple accepted (defaults to "sda", example:"sda,sdc")
"""

import os

import bumblebee.util
import bumblebee.output
import bumblebee.engine

from shutil import which
from subprocess import Popen, PIPE


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config, None)
        self.devices = self.list_devices()
        self.display = self.parameter('display', 'combined')
        self.drives = self.parameter('drives', 'sda')
        self.widgets(self.create_widgets())

    def create_widgets(self):
        widgets = []
        if self.display == 'combined':
            widget = bumblebee.output.Widget()
            widget.set('device', 'combined')
            widget.set('assessment', self.combined())
            self.output(widget)
            widgets.append(widget)
        else:
            for device in self.devices:
                if self.display == "singles" and device not in self.drives:
                    continue
                widget = bumblebee.output.Widget()
                widget.set('device', device)
                widget.set('assessment', self.smart(device))
                self.output(widget)
                widgets.append(widget)
        return widgets

    def update(self, widgets):
        for widget in widgets:
            device = widget.get('device')
            if device == 'combined':
                widget.set('assessment', self.combined())
                self.output(widget)
            else:
                widget.set('assessment', self.smart(device))
                self.output(widget)

    def output(self, widget):
        device = widget.get('device')
        assessment = widget.get('assessment')
        widget.full_text("{}: {}".format(device, assessment))

    def state(self, widget):
        states = []
        assessment = widget.get('assessment')
        if assessment == 'Pre-fail':
            states.append('warning')
        if assessment == 'Fail':
            states.append('critical')
        return states

    def combined(self):
        for device in self.devices:
            result = self.smart(device)
            if result == 'Fail':
                return 'Fail'
            if result == 'Pre-fail':
                return 'Pre-fail'
        return 'OK'

    def list_devices(self):
        for (root, folders, files) in os.walk('/dev'):
            if root == '/dev':
                devices = {"".join(filter(lambda i: i.isdigit() == False, file)) for file in files if 'sd' in file}
                nvme = {file for file in files if('nvme0n' in file and 'p' not in file)}
                devices.update(nvme)
                return devices

    def smart(self, disk_name):
        SMARTCTL_PATH = which('smartctl')
        assessment = None
        cmd = Popen(
            ['sudo', SMARTCTL_PATH, '--health', os.path.join('/dev/', disk_name)],
            stdout=PIPE,
            stderr=PIPE,
        )
        _stdout, _stderr = [i.decode('utf8') for i in cmd.communicate()]
        _stdout = _stdout.split('\n')
        line = _stdout[4]
        if 'SMART' in line:
            if any([i in line for i in ['PASSED', 'OK']]):
                assessment = 'OK'
            else:
                assessment = 'Fail'

        if assessment == 'OK':
            cmd = Popen(
                ['sudo', SMARTCTL_PATH, '-A', os.path.join('/dev/', disk_name)],
                stdout=PIPE,
                stderr=PIPE,
            )
            _stdout, _stderr = [i.decode('utf8') for i in cmd.communicate()]
            _stdout = _stdout.split('\n')
            for line in _stdout:
                if "Pre-fail" in line:
                    assessment = "Pre-fail"
        return assessment
