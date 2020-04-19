# pylint: disable=C0111,R0903

"""Displays battery status, remaining percentage and charging information.

Parameters:
    * battery.device     : Comma-separated list of battery devices to read information from (defaults to auto for auto-detection)
    * battery.warning    : Warning threshold in % of remaining charge (defaults to 20)
    * battery.critical   : Critical threshold in % of remaining charge (defaults to 10)
    * battery.showdevice : If set to 'true', add the device name to the widget (defaults to False)
    * battery.decorate   : If set to 'false', hides additional icons (charging, etc.) (defaults to True)
    * battery.showpowerconsumption: If set to 'true', show current power consumption (defaults to False)
"""

import os
import glob
import logging
log = logging.getLogger(__name__)

try:
    import power
except ImportError:
    log.warning('unable to import module "power": Time estimates will not be available')

import core.module
import core.widget
import core.input

import util.format

class BatteryManager(object):
    def remaining(self):
        try:
            estimate = power.PowerManagement().get_time_remaining_estimate()
            # do not show remaining if on AC
            if estimate == power.common.TIME_REMAINING_UNLIMITED:
                return None
            return estimate*60 # return value in seconds
        except Exception as e:
            return -1
        return -1

    def read(self, battery, component, default=None):
        path = '/sys/class/power_supply/{}'.format(battery)
        if not os.path.exists(path):
            return default
        try:
            with open('{}/{}'.format(path, component)) as f:
                return f.read().strip()
        except IOError:
            return 'n/a'
        return default


    def capacity(self, battery):
        capacity = self.read(battery, 'capacity', 100)
        if capacity != 'n/a':
            capacity = int(capacity)

        return capacity if capacity < 100 else 100

    def isac(self, battery):
        path = '/sys/class/power_supply/{}'.format(battery)
        return not os.path.exists(path)

    def consumption(self, battery):
        consumption = self.read(battery, 'power_now', 'n/a')
        if consumption == 'n/a':
            return 'n/a'
        return '{}W'.format(int(consumption)/1000000)

    def charge(self, battery):
        return self.read(battery, 'status', 'n/a')

class Module(core.module.Module):
    def __init__(self, config):
        widgets = []
        super().__init__(config, widgets)

        self.__manager = BatteryManager()

        self._batteries = util.format.aslist(self.parameter('device', 'auto'))
        if self._batteries[0] == 'auto':
            self._batteries = [ os.path.basename(battery) for battery in glob.glob('/sys/class/power_supply/BAT*') ]
        if len(self._batteries) == 0:
            raise Exceptions('no batteries configured/found')
        core.input.register(self, button=core.input.LEFT_MOUSE,
            cmd='gnome-power-statistics')

        for battery in self._batteries:
            log.debug('adding new widget for {}'.format(battery))
            widget = core.widget.Widget(full_text=self.capacity, name=battery, module=self)
            widgets.append(widget)
            if util.format.asbool(self.parameter('decorate', True)) == False:
                widget.set('theme.exclude', 'suffix')

    def capacity(self, widget):
        capacity = self.__manager.capacity(widget.name())
        widget.set('capacity', capacity)
        widget.set('ac', self.__manager.isac(widget.name()))
        widget.set('theme.minwidth', '100%')

        # Read power conumption
        if util.format.asbool(self.parameter('showpowerconsumption', False)):
            output = '{}% ({})'.format(capacity, self.__manager.consumption(widget.name()))
        else:
             output =  '{}%'.format(capacity)

        if util.format.asbool(self.parameter('showremaining', True))\
                and self.__manager.charge(widget.name()) == 'Discharging':
            remaining = self.__manager.remaining()
            if remaining >= 0:
                output = '{} {}'.format(output, util.format.duration(remaining, compact=True, unit=True))

        if util.format.asbool(self.parameter('showdevice', False)):
            output = '{} ({})'.format(output, widget.name())

        return output
       
    def state(self, widget):
        state = []
        capacity = widget.get('capacity')

        if capacity < 0:
            log.debug('battery state: {}'.format(state))
            return ['critical', 'unknown']

        if capacity < int(self.parameter('critical', 10)):
            state.append('critical')
        elif capacity < int(self.parameter('warning', 20)):
            state.append('warning')

        if widget.get('ac'):
            state.append('AC')
        else:
            charge = self.__manager.charge(widget.name())
            if charge == 'Discharging':
                state.append('discharging-{}'.format(min([10, 25, 50, 80, 100], key=lambda i: abs(i-capacity))))
            elif charge == 'Unknown':
                state.append('unknown-{}'.format(min([10, 25, 50, 80, 100], key=lambda i: abs(i-capacity))))
            else:
                if capacity > 95:
                    state.append('charged')
                else:
                    state.append('charging')
        return state

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
