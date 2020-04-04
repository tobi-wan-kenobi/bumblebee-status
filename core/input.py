import uuid
import logging

import core.event

import util.cli

LEFT_MOUSE = 1
MIDDLE_MOUSE = 2
RIGHT_MOUSE = 3
WHEEL_UP = 4
WHEEL_DOWN = 5

def button_name(button):
    if button == LEFT_MOUSE: return 'left-mouse'
    if button == RIGHT_MOUSE: return 'right-mouse'
    if button == MIDDLE_MOUSE: return 'middle-mouse'
    if button == WHEEL_UP: return 'wheel-up'
    if button == WHEEL_DOWN: return 'wheel-down'
    return 'n/a'

callbacks = {}

class Object(object):
    def __init__(self):
        super(Object, self).__init__()
        self.id = str(uuid.uuid4())

def register(obj, button=None, cmd=None):
    logging.debug('registering callback {} {}'.format(obj.id, button))
    callbacks.setdefault(obj.id, {}).setdefault(button, []).append(cmd)

def trigger(event):
    for field in ['instance', 'name']:
        if field in event:
            cb = callbacks.get(event[field])
            __invoke(event, cb)

def __invoke(event, callback):
    if not callback: return
    if not 'button' in event: return

    for cb in callback.get(event['button'], []):
        if callable(cb):
            cb(event)
        else:
            try:
                util.cli.execute(cb, wait=False)
            except Exception as e:
                logging.error('failed to invoke callback: {}'.format(e))
                return

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
