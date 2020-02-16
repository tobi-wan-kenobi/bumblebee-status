import sys
import json
import time

import core.theme
import core.event

class i3(object):
    def __init__(self, theme=core.theme.Theme()):
        self._modules = []
        self._status = {}
        self._theme = theme
        core.event.register('start', self.draw, 'start')
        core.event.register('update', self.draw, 'statusline')
        core.event.register('stop', self.draw, 'stop')

    def modules(self, modules=None):
        if not modules:
            return self._modules
        self._modules = modules if isinstance(modules, list) else [ modules ]

    def draw(self, what, args=None):
        cb = getattr(self, what)
        data = cb(args) if args else cb()
        if 'data' in data:
            sys.stdout.write(json.dumps(data['data']))
        if 'suffix' in data:
            sys.stdout.write(data['suffix'])
        sys.stdout.write('\n')
        sys.stdout.flush()

    def start(self):
        return {
            'data': { 'version': 1, 'click_events': True },
            'suffix': '\n[',
        }

    def stop(self):
        return { 'suffix': '\n]' }

    def widgets(self, module):
        widgets = []
        for widget in module.widgets():
            widgets.append({
                'full_text': widget.full_text(),
                'instance': widget.id(),
                'name': module.id(),
                'color': self._theme.fg(widget),
                'background': self._theme.bg(widget),
                'separator': self._theme.default_separators(),
            })
        return widgets

    def update(self, affected_modules=None):
        for module in self._modules:
            module.update()
            self._status[module] = self.widgets(module)

    def statusline(self):
        widgets = []
        for module in self._modules:
            widgets += self._status[module]
        return {
            'data': widgets,
            'suffix': ','
        }

    def wait(self, interval):
        time.sleep(interval)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
