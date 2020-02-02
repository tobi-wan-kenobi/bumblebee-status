import sys
import json
import time

class i3(object):
    def __init__(self):
        self._modules = []
        self.clear()

    def modules(self, modules=None):
        if not modules:
            return self._modules
        self._modules = modules if isinstance(modules, list) else [ modules ]

    def draw(self, what):
        data = getattr(self, what)()
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

    def clear(self):
        self._statusline = []

    def statusline(self):
        status = []
        for module in self._modules:
            for widget in module.widgets():
                status.append({
                    'full_text': widget.full_text()
                })
        return {
            'data': status,
            'suffix': ','
        }

    def wait(self, interval):
        time.sleep(interval)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
