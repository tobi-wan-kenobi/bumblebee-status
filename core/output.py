import sys
import json
import time

class i3(object):
    def __init__(self):
        self.clear()

    def draw(self, what):
        data = getattr(self, what)()
        if 'data' in data:
            sys.stdout.write(json.dumps(data['data']))
        if 'suffix' in data:
            sys.stdout.write(data['suffix'])
        sys.stdout.write('\n')

    def start(self):
        return {
            'data': { 'version': 1, 'click_events': True },
            'suffix': '\n[',
        }

    def stop(self):
        return { 'suffix': '\n]' }

    def clear(self):
        self._statusline = []

    def append(self, module):
        for widget in module.widgets():
            self._statusline.append({
                'full_text': widget.full_text()
            })

    def statusline(self):
        return {
            'data': self._statusline,
            'suffix': ','
        }

    def wait(self, interval):
        time.sleep(interval)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
