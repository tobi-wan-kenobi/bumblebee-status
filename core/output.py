import sys
import json
import time

import core.theme
import core.event

class i3(object):
    def __init__(self, theme=core.theme.Theme(), config=core.config.Config([])):
        self._modules = []
        self._status = {}
        self._theme = theme
        self._config = config
        core.event.register('start', self.draw, 'start')
        core.event.register('update', self.draw, 'statusline')
        core.event.register('stop', self.draw, 'stop')

    def theme(self, new_theme=None):
        if new_theme:
            self._theme = new_theme
        return self._theme

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

    def __pad(self, module, widget, full_text):
        padding = self._theme.padding()
        if not full_text: return padding
        return '{}{}{}'.format(padding, full_text, padding)

    def __decorate(self, module, widget, full_text):
        return '{}{}{}'.format(
            self.__pad(module, widget, self._theme.prefix(widget)),
            full_text,
            self.__pad(module, widget, self._theme.suffix(widget))
        )

    def __common_attributes(self, module, widget):
        return {
            'separator': self._theme.default_separators(),
            'separator_block_width': self._theme.separator_block_width(),
            'border_top': self._theme.border_top(),
            'border_left': self._theme.border_left(),
            'border_right': self._theme.border_right(),
            'border_bottom': self._theme.border_bottom(),
            'instance': widget.id(),
            'name': module.id(),
        }

    def __separator(self, module, widget):
        if not self._theme.separator():
            return []
        attr = self.__common_attributes(module, widget)
        attr.update({
            'full_text': self._theme.separator(),
            'color': self._theme.bg(widget),
            'background': self._theme.bg('previous'),
            '_decorator': True,
        })
        return [attr]

    def __main(self, module, widget, text):
        attr = self.__common_attributes(module, widget)
        attr.update({
            'full_text': self.__decorate(module, widget, text),
            'color': self._theme.fg(widget),
            'background': self._theme.bg(widget),
            'min_width': self.__decorate(module, widget, widget.get('theme.minwidth')),
        })
        return [attr]

    def widgets(self, module):
        widgets = []
        for widget in module.widgets():
            if widget.module() and self._config.autohide(widget.module().name()):
                if not any(state in widget.state() for state in [ 'warning', 'critical']):
                    continue
            widgets += self.__separator(module, widget)
            widgets += self.__main(module, widget, self._status[widget])
            core.event.trigger('next-widget')
        return widgets

    def update(self, affected_modules=None):
        now = time.time()
        for module in self._modules:
            if affected_modules and not module.id() in affected_modules:
                continue
            if not affected_modules and module.next_update:
                if now < module.next_update:
                    continue
            module.update_wrapper()
            module.next_update = now + float(module.parameter('interval', self._config.interval()))
            for widget in module.widgets():
                self._status[widget] = widget.full_text()

    def statusline(self):
        widgets = []
        for module in self._modules:
            widgets += self.widgets(module)
        return {
            'data': widgets,
            'suffix': ','
        }

    def wait(self, interval):
        time.sleep(interval)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
