# pylint: disable=C0111,R0903

'''Displays battery status, remaining percentage and charging information.

Parameters:
    * battery.device     : Comma-separated list of battery devices to read information from (defaults to auto for auto-detection)
    * battery.warning    : Warning threshold in % of remaining charge (defaults to 20)
    * battery.critical   : Critical threshold in % of remaining charge (defaults to 10)
    * battery.showdevice : If set to 'true', add the device name to the widget (defaults to False)
    * battery.decorate   : If set to 'false', hides additional icons (charging, etc.) (defaults to True)
    * battery.showpowerconsumption: If set to 'true', show current power consumption (defaults to False)
'''

import os
import glob
import logging
try:
    import power
except ImportError:
    pass

import core.module
import core.widget
import core.input

import util.format

log = logging.getLogger(__name__)

class Module(core.module.Module):
    def __init__(self, config=None):
        widgets = []
        super().__init__(config, widgets)

        self._batteries = util.format.aslist(self.parameter('device', 'auto'))
        if self._batteries[0] == 'auto':
            self._batteries = glob.glob('/sys/class/power_supply/BAT*')
        else:
            self._batteries = ['/sys/class/power_supply/{}'.format(b) for b in self._batteries]
        if len(self._batteries) == 0:
            raise Exceptions('no batteries configured/found')
        core.input.register(self, button=core.input.LEFT_MOUSE,
            cmd='gnome-power-statistics')

        for path in self._batteries:
            log.debug('adding new widget for {}'.format(path))
            widget = core.widget.Widget(full_text=self.capacity, name=path, module=self)
            widgets.append(widget)
            self.capacity(widget)
            if util.format.asbool(self.parameter('decorate', True)) == False:
                widget.set('theme.exclude', 'suffix')

    def remaining(self):
        estimate = 0.0
        try:
            estimate = power.PowerManagement().get_time_remaining_estimate()
            # do not show remaining if on AC
            if estimate == power.common.TIME_REMAINING_UNLIMITED:
                return None
            if estimate == power.common.TIME_REMAINING_UNKNOWN:
                return ''
        except Exception:
            return ''
        return util.format.duration(estimate*60, shorten=True, suffix=True) # estimate is in minutes

    def capacity(self, widget):
        widget.set('capacity', -1)
        widget.set('ac', False)
        if not os.path.exists(widget.name()):
            widget.set('capacity', 100)
            widget.set('ac', True)
            return 'ac'
        capacity = 100
        try:
            with open('{}/capacity'.format(widget.name())) as f:
                capacity = int(f.read())
        except IOError:
            return 'n/a'

        capacity = capacity if capacity < 100 else 100
        widget.set('capacity', capacity)

        # Read power conumption
        if util.format.asbool(self.parameter('showpowerconsumption', False)):
            r=open(widget.name() + '/power_now', 'r')
            output =  '{}% ({})'.format(capacity,str(int(r.read())/1000000) + 'W')
        else:
             output =  '{}%'.format(capacity)

        widget.set('theme.minwidth', '100%')
        if util.format.asbool(self.parameter('showremaining', True))\
                and self.getCharge(widget) == 'Discharging':
            output = '{} {}'.format(output, self.remaining())

        if util.format.asbool(self.parameter('showdevice', False)):
            output = '{} ({})'.format(output, os.path.basename(widget.name))

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
            charge = self.getCharge(widget)
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

    def getCharge(self, widget):
        charge = ''
        try:
            with open('{}/status'.format(widget.name())) as f:
                charge = f.read().strip()
        except IOError:
                pass
        return charge

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
