import sys
import json
import time

import core.theme
import core.event

def dump_json(obj):
    return obj.__dict__

class block(object):
    __COMMON_THEME_FIELDS = [
        'separator', 'separator_block_width',
        'border_top', 'border_left', 'border_right', 'border_bottom',
        'pango', 'fg', 'bg'
    ]
    def __init__(self, theme, module, widget):
        self.__attributes = {}
        for key in self.__COMMON_THEME_FIELDS:
            tmp = theme.get(key, widget)
            if tmp:
                self.__attributes[key] = tmp

        self.__attributes['name'] = module.id
        self.__attributes['instance'] = widget.id

    def set(self, key, value):
        self.__attributes[key] = value

    def __dict__(self):
        return {}

class i3(object):
    def __init__(self, theme=core.theme.Theme(), config=core.config.Config([])):
        self.__modules = []
        self.__content = {}
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
        if 'blocks' in data:
            sys.stdout.write(json.dumps(data['blocks'], default=dump_json))
        if 'suffix' in data:
            sys.stdout.write(data['suffix'])
        sys.stdout.write('\n')
        sys.stdout.flush()

    def start(self):
        return {
            'blocks': { 'version': 1, 'click_events': True },
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

    def __separator_block(self, module, widget):
        blk = block(self.__theme, module, widget)
        blk.set('_decorator', True)
        return blk

    def __content_block(self, module, widget):
        text = self.__content[widget]
        blk = block(self.__theme, module, widget)
        blk.set('min_width', self.__decorate(module, widget, widget.get('theme.minwidth')))
        blk.set('full_text', self.__decorate(module, widget, text))
        if self.__config.debug():
            blk.set('__state', ', '.join(module.state(widget)))
        return blk

    def blocks(self, module):
        blocks = []
        for widget in module.widgets():
            if widget.module() and self.__config.autohide(widget.module().name()):
                if not any(state in widget.state() for state in [ 'warning', 'critical']):
                    continue
            blocks.append(self.__separator_block(module, widget))
            blocks.append(self.__content_block(module, widget))
            core.event.trigger('next-widget')
        return blocks

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
                self.__content[widget] = widget.full_text()

    def statusline(self):
        blocks = []
        for module in self.__modules:
            blocks.extend(self.blocks(module))
        return {
            'blocks': blocks,
            'suffix': ','
        }

    def wait(self, interval):
        time.sleep(interval)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
