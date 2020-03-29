# -*- coding: UTF-8 -*-

'''Displays sensor temperature and CPU frequency

Parameters:

    * sensors2.chip: 'sensors -u' compatible filter for chip to display (default to empty - show all chips)
    * sensors2.showcpu: Enable or disable CPU frequency display (default: true)
    * sensors2.showtemp: Enable or disable temperature display (default: true)
    * sensors2.showfan: Enable or disable fan display (default: true)
    * sensors2.showother: Enable or display 'other' sensor readings (default: false)
    * sensors2.showname: Enable or disable show of sensor name (default: false)
'''

import re

import core.module
import core.widget
import core.input

import util.cli
import util.format

class Module(core.module.Module):
    def __init__(self, config):
        super().__init__(config, [])

        self.__chip = self.parameter('chip', '')
        self.__data = {}

    def update(self):
        self.widgets(self.__create_widgets())
        self.__update()
        for widget in self.widgets():
            self.__update_widget(widget)

    def state(self, widget):
        widget_type = widget.get('type', '')
        try:
            data = self._data[widget.get('adapter')][widget.get('package')][widget.get('field')]
            if 'crit' in data and float(data['input']) > float(data['crit']):
                return ['critical', widget_type]
            if 'max' in data and float(data['input']) > float(data['max']):
                return ['warning', widget_type]
        except:
            pass
        return [widget_type]

    def __create_widgets(self):
        widgets = []
        show_temp = util.format.asbool(self.parameter('showtemp', True))
        show_fan = util.format.asbool(self.parameter('showfan', True)) 
        show_other = util.format.asbool(self.parameter('showother', False))

        if util.format.asbool(self.parameter('showcpu', True)):
            widget = core.widget.Widget(full_text=self.__cpu)
            widget.set('type', 'cpu')
            widgets.append(widget)

        for adapter in self.__data:
            for package in self.__data[adapter]:
                if util.format.asbool(self.parameter('showname', False)):
                    widget = core.widget.Widget(full_text=package)
                    widget.set('data', self._data[adapter][package])
                    widget.set('package', package)
                    widget.set('field', '')
                    widget.set('adapter', adapter)
                    widgets.append(widget)
                for field in self.__data[adapter][package]:
                    widget = core.widget.Widget()
                    widget.set('package', package)
                    widget.set('field', field)
                    widget.set('adapter', adapter)
                    if 'temp' in field and show_temp:
                        # seems to be a temperature
                        widget.set('type', 'temp')
                        widgets.append(widget)
                    if 'fan' in field and show_fan:
                        # seems to be a fan
                        widget.set('type', 'fan')
                        widgets.append(widget)
                    elif show_other:
                        # everything else
                        widget.set('type', 'other')
                        widgets.append(widget)
        return widgets

    def __update_widget(self, widget):
        if widget.get('field', '') == '':
            return # nothing to do
        data = self.__data[widget.get('adapter')][widget.get('package')][widget.get('field')]
        if 'temp' in widget.get('field'):
            widget.full_text(u'{:0.01f}°C'.format(data['input']))
        elif 'fan' in widget.get('field'):
            widget.full_text(u'{:0.0f}RPM'.format(data['input']))
        else:
            widget.full_text(u'{:0.0f}'.format(data['input']))

    def __update(self):
        output = util.cli.execute('sensors -u {}'.format(self.__chip))
        self.__data = self.__parse(output)

    def __parse(self, data):
        output = {}
        package = ''
        adapter = None
        chip = None
        for line in data.split('\n'):
            if 'Adapter' in line:
                # new adapter
                line = line.replace('Adapter: ', '')
                adapter = '{} {}'.format(chip, line)
                output[adapter] = {}
            chip = line #default - line before adapter is always the chip
            if not adapter: continue
            key, value = (line.split(':') + ['', ''])[:2]
            if not line.startswith(' '):
                # assume this starts a new package
                if package in output[adapter] and output[adapter][package] == {}:
                    del output[adapter][package]
                output[adapter][key] = {}
                package = key
            else:
                # feature for this chip
                try:
                    name, variant = (key.strip().split('_', 1) + ['',''])[:2]
                    if not name in output[adapter][package]:
                        output[adapter][package][name] = { }
                    if variant:
                        output[adapter][package][name][variant] = {}
                    output[adapter][package][name][variant] = float(value)
                except Exception as e:
                    pass
        return output

    def __cpu(self, _):
        mhz = None
        try:
            output = open('/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq').read()
            mhz = int(float(output)/1000.0)
        except:
            output = open('/proc/cpuinfo').read()
            m = re.search(r'cpu MHz\s+:\s+(\d+)', output)
            if m:
                mhz = int(m.group(1))
            else:
                m = re.search(r'BogoMIPS\s+:\s+(\d+)', output)
                if m:
                    return '{} BogoMIPS'.format(int(m.group(1)))
        if not mhz:
            return 'n/a'

        if mhz < 1000:
            return '{} MHz'.format(mhz)
        else:
            return '{:0.01f} GHz'.format(float(mhz)/1000.0)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
