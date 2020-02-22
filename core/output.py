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

    def __separator(self, widget):
        if not self._theme.separator():
            return []
        return [{
            'full_text': self._theme.separator(),
            'color': self._theme.bg(widget),
            'background': self._theme.prev_bg(widget),
            'separator': False,
            'separator_block_width': self._theme.separator_block_width(),
            'border_top': self._theme.border_top(),
            'border_left': self._theme.border_left(),
            'border_right': self._theme.border_right(),
            'border_bottom': self._theme.border_bottom(),
        }]

    def __main(self, module, widget):
        return [{
            'full_text': widget.full_text(),
            'instance': widget.id(),
            'name': module.id(),
            'color': self._theme.fg(widget),
            'background': self._theme.bg(widget),
            'separator': self._theme.default_separators(),
            'separator_block_width': self._theme.separator_block_width(),
            'border_top': self._theme.border_top(),
            'border_left': self._theme.border_left(),
            'border_right': self._theme.border_right(),
            'border_bottom': self._theme.border_bottom(),
        }]

    def widgets(self, module):
        widgets = []
        for widget in module.widgets():
            widgets += self.__separator(widget)
            widgets += self.__main(module, widget)
            core.event.trigger('next-widget')
        return widgets

    def update(self, affected_modules=None):
        for module in self._modules:
            module.update()
            self._status[module] = self.widgets(module)

    def statusline(self):
        widgets = []
        for module in self._modules:
            if module in self._status:
                widgets += self._status[module]
        return {
            'data': widgets,
            'suffix': ','
        }

    def wait(self, interval):
        time.sleep(interval)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
