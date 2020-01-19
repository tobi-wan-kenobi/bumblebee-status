import json

class i3(object):
    def start(self):
        return '{}\n'.format(json.dumps({ 'version': 1, 'click_events': True }))

    def stop(self):
        return ']\n'

    def begin_status_line(self):
        return '['

    def end_status_line(self):
        return '],\n'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
