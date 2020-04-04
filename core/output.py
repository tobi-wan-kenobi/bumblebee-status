import sys
import json
import time

import core.theme
import core.event

class i3(object):
    def __init__(self, theme=core.theme.Theme(), config=core.config.Config([])):
        self.__modules = []
        self.__status = {}
        self.__theme = theme
        self.__config = config
        core.event.register('start', self.draw, 'start')
        core.event.register('update', self.draw, 'statusline')
        core.event.register('stop', self.draw, 'stop')

    def theme(self, new_theme=None):
        if new_theme:
            self.__theme = new_theme
        return self.__theme

    def modules(self, modules=None):
        if not modules:
            return self.__modules
        self.__modules = modules if isinstance(modules, list) else [ modules ]

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
        padding = self.__theme.padding()
        if not full_text: return padding
        return '{}{}{}'.format(padding, full_text, padding)

    def __decorate(self, module, widget, full_text):
        if full_text is None: return None
        return '{}{}{}'.format(
            self.__pad(module, widget, self.__theme.prefix(widget)),
            full_text,
            self.__pad(module, widget, self.__theme.suffix(widget))
        )

    def __common_attributes(self, module, widget):
        return {
            'separator': self.__theme.default_separators(),
            'separator_block_width': self.__theme.separator_block_width(),
            'border_top': self.__theme.border_top(),
            'border_left': self.__theme.border_left(),
            'border_right': self.__theme.border_right(),
            'border_bottom': self.__theme.border_bottom(),
            'instance': widget.id,
            'name': module.id,
        }

    def __separator(self, module, widget):
        if not self.__theme.separator():
            return []
        attr = self.__common_attributes(module, widget)
        attr.update({
            'full_text': self.__theme.separator(),
            'color': self.__theme.bg(widget),
            'background': self.__theme.bg('previous'),
            '_decorator': True,
        })
        return [attr]

    def __main(self, module, widget, text):
        attr = self.__common_attributes(module, widget)
        attr.update({
            'full_text': self.__decorate(module, widget, text),
            'color': self.__theme.fg(widget),
            'background': self.__theme.bg(widget),
            'min_width': self.__decorate(module, widget, widget.get('theme.minwidth')),
        })
        if (self.__config.debug()):
            attr.update({
                '__state': ", ".join(module.state(widget))
            })
        return [attr]

    def widgets(self, module):
        widgets = []
        for widget in module.widgets():
            if widget.module() and self.__config.autohide(widget.module().name()):
                if not any(state in widget.state() for state in [ 'warning', 'critical']):
                    continue
            widgets += self.__separator(module, widget)
            widgets += self.__main(module, widget, self.__status[widget])
            core.event.trigger('next-widget')
        return widgets

    def update(self, affected_modules=None):
        now = time.time()
        for module in self.__modules:
            if affected_modules and not module.id in affected_modules:
                continue
            if not affected_modules and module.next_update:
                if now < module.next_update:
                    continue
            module.update_wrapper()
            module.next_update = now + float(module.parameter('interval', self.__config.interval()))
            for widget in module.widgets():
                self.__status[widget] = widget.full_text()

    def statusline(self):
        widgets = []
        for module in self.__modules:
            widgets += self.widgets(module)
        return {
            'data': widgets,
            'suffix': ','
        }

    def wait(self, interval):
        time.sleep(interval)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
