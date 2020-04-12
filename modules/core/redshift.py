# pylint: disable=C0111,R0903

"""Displays the current color temperature of redshift

Requires the following executable:
    * redshift

Parameters:
    * redshift.location : location provider, either of 'auto' (default), 'geoclue2',
        'ipinfo' (requires the requests package), or 'manual'
        'auto' uses whatever redshift is configured to do
    * redshift.lat : latitude if location is set to 'manual'
    * redshift.lon : longitude if location is set to 'manual'
"""

import threading
import logging
log = logging.getLogger(__name__)
try:
    import requests
except ImportError:
    log.warning('unable to import module "requests": Location via IP disabled')

import core.module
import core.widget
import core.input
import core.decorators

import util.cli

def get_redshift_value(module):
    widget = module.widget()
    location = module.parameter('location', 'auto')
    lat = module.parameter('lat', None)
    lon = module.parameter('lon', None)

    # Even if location method is set to manual, if we have no lat or lon,
    # fall back to the geoclue2 method.
    if location == 'manual' and (lat is None or lon is None):
        location = 'geoclue2'

    command = ['redshift', '-p']
    if location == 'manual':
        command.extend(['-l', '{}:{}'.format(lat, lon)])
    if location == 'geoclue2':
        command.extend(['-l', 'geoclue2'])

    try:
        res = util.cli.execute(' '.join(command))
    except Exception:
        res = ''
    widget.set('temp', 'n/a')
    widget.set('transition', None)
    widget.set('state', 'day')
    for line in res.split('\n'):
        line = line.lower()
        if 'temperature' in line:
            widget.set('temp', line.split(' ')[2])
        if 'period' in line:
            state = line.split(' ')[1]
            if 'day' in state:
                widget.set('state', 'day')
            elif 'night' in state:
                widget.set('state', 'night')
            else:
                widget.set('state', 'transition')
                widget.set('transition', ' '.join(line.split(' ')[2:]))
    core.event.trigger('update', [ widget.module().id ], redraw_only=True)

class Module(core.module.Module):
    @core.decorators.every(seconds=10)
    def __init__(self, config):
        widget = core.widget.Widget(self.text)
        super().__init__(config, widget)

        self.__thread = threading.Thread(target=get_redshift_value, args=(self,))

        if self.parameter('location', '') == 'ipinfo':
            # override lon/lat with ipinfo
            try:
                location_url = 'http://ipinfo.io/json'
                location = requests.get(location_url).json()
                self.parameter('lat', location['loc'].split(',')[0])
                self.parameter('lon', location['loc'].split(',')[1])
                self.parameter('location', 'manual')
            except Exception:
                # Fall back to geoclue2.
                self.parameter('location', 'geoclue2')

        self._text = ''

    def text(self, widget):
        val = widget.get('temp', 'n/a')
        transition = widget.get('transition', None)
        if transition:
            val = '{} {}'.format(val, transition)
        return val

    def update(self):
        if self.__thread.isAlive():
            return
        self.__thread.start()

    def state(self, widget):
        return widget.get('state', None)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
