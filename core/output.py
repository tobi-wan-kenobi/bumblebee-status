import sys
import json
import time

class i3(object):
    def __init__(self):
        self._modules = []
        self._status = {}

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

    def update(self, affected_modules=None):
        for module in self._modules:
            module.update()
            self._status[module] = []
            for widget in module.widgets():
                self._status[module].append({
                    'full_text': widget.full_text(),
                    'instance': widget.id(),
                    'name': module.id(),
                })

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
