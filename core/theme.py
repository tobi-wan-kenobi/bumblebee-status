import os
import io
import json

import core.event

THEME_BASE_DIR=os.path.dirname(os.path.realpath(__file__))
PATHS=[
    '.',
    os.path.join(THEME_BASE_DIR, '../themes'),
    os.path.expanduser('~/.config/bumblebee-status/themes'),
]

class Theme(object):
    def __init__(self, name='default', iconset=None, raw_data=None):
        self.name = name
        self.__widget_count = 0
        if raw_data:
            self.__data = raw_data
        else:
            self.__data = self.load(name)
        core.event.register('start', self.__start)
        core.event.register('next-widget', self.__next_widget)

    def load(self, name):
        for path in PATHS:
            theme_file = os.path.join(path, '{}.json'.format(name))
            if os.path.isfile(theme_file):
                with io.open(theme_file, encoding='utf-8') as data:
                    return json.load(data)
        raise RuntimeError('unable to find theme {}'.format(name))

    def fg(self, widget=None):
        return self.__get(widget, 'fg')

    def bg(self, widget=None):
        return self.__get(widget, 'bg')

    def default_separators(self, widget=None):
        return self.__get(widget, 'default-separators', True)

    def __start(self):
        self.__widget_count = 0

    def __next_widget(self):
        self.__widget_count = self.__widget_count + 1

    def __get(self, widget, key, default=None):
        value = default

        for option in ['defaults', 'cycle']:
            if option in self.__data:
                tmp = self.__data[option]
                if isinstance(tmp, list):
                    tmp = tmp[self.__widget_count % len(tmp)]
                value = tmp.get(key, value)
        return value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
