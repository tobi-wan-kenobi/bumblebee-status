import os
import io
import json
import logging

import core.event
import util.algorithm

log = logging.getLogger(__name__)

THEME_BASE_DIR=os.path.dirname(os.path.realpath(__file__))
PATHS=[
    '.',
    os.path.join(THEME_BASE_DIR, '../themes'),
    os.path.expanduser('~/.config/bumblebee-status/themes'),
]

class Theme(object):
    def __init__(self, name='default', iconset='auto', raw_data=None):
        self.name = name
        self.__widget_count = 0
        self.__previous = {}
        self.__current = {}
        self.__keywords = {}
        self.__data = raw_data if raw_data else self.load(name)
        for icons in self.__data.get('icons', []):
            util.algorithm.merge(self.__data, self.load(icons, 'icons'))
        if iconset != 'auto':
            util.algorithm.merge(self.__data, self.load(iconset, 'icons'))
        for colors in self.__data.get('colors', []):
            util.algorithm.merge(self.__keywords, self.load_keywords(colors))

        core.event.register('update', self.__start)
        core.event.register('next-widget', self.__next_widget)

        for attr, default in [
            ('fg', None), ('bg', None),
            ('default-separators', True),
            ('separator-block-width', 0),
            ('separator', None),
            ('border-top', 0),
            ('border-bottom', 0),
            ('border-left', 0),
            ('border-right', 0),
            ('padding', ''),
            ('prefix', ''), ('suffix', ''),
        ]:
            setattr(self, attr.replace('-', '_'), lambda widget=None, default=default, attr=attr: self.__get(widget, attr, default))

    def keywords(self):
        return self.__keywords

    def load(self, name, subdir=''):
        if isinstance(name, dict): return name # support plain data
        for path in PATHS:
            theme_file = os.path.join(path, subdir, '{}.json'.format(name))
            if os.path.isfile(theme_file):
                with io.open(theme_file, encoding='utf-8') as data:
                    return json.load(data)
        raise RuntimeError('unable to find theme {}'.format(name))

    def __load(self, filename, sections):
        result = {}
        with io.open(os.path.expanduser(filename)) as data:
            colors = json.load(data)
            for field in sections:
                for key in colors.get(field, []):
                    result[key] = colors[field][key]
        return result

    def load_keywords(self, name):
        try:
            if isinstance(name, dict):
                return name
            if name.lower() == 'wal':
                return self.__load('~/.cache/wal/colors.json', ['special', 'colors'])
        except Exception as e:
            log.error('failed to load colors: {}', e)

    def __start(self):
        self.__widget_count = 0
        self.__current.clear()
        self.__previous.clear()

    def __next_widget(self):
        self.__widget_count = self.__widget_count + 1
        self.__previous = dict(self.__current)
        self.__current.clear()

    def __get(self, widget, key, default=None):
        if not widget:
            widget = core.widget.Widget('')
        if isinstance(widget, str):
            # special handling
            if widget == 'previous':
                return self.__previous.get(key, None)

        value = default

        for option in ['defaults', 'cycle']:
            if option in self.__data:
                tmp = self.__data[option]
                if isinstance(tmp, list):
                    tmp = tmp[self.__widget_count % len(tmp)]
                value = tmp.get(key, value)

        value = self.__data.get(key, value)

        if widget.module():
            value = self.__get(None, widget.module().name(), {}).get(key, value)

        if not key in widget.state():
            for state in widget.state():
                theme = self.__get(widget, state, {})
                value = theme.get(key, value)

        if not type(value) in (list, dict):
            value = self.__keywords.get(value, value)

        if isinstance(value, list):
            key = '__{}-idx__'.format(key)
            idx = widget.get(key, 0)
            widget.set(key, (idx + 1) % len(value))
            value = value[idx]
        self.__current[key] = value
        return value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
