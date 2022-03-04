import uuid
import logging

import core.event

import util.cli

LEFT_MOUSE = 1
MIDDLE_MOUSE = 2
RIGHT_MOUSE = 3
WHEEL_UP = 4
WHEEL_DOWN = 5
UPDATE = -1


def button_name(button):
    if button == LEFT_MOUSE:
        return "left-mouse"
    if button == RIGHT_MOUSE:
        return "right-mouse"
    if button == MIDDLE_MOUSE:
        return "middle-mouse"
    if button == WHEEL_UP:
        return "wheel-up"
    if button == WHEEL_DOWN:
        return "wheel-down"
    if button == UPDATE:
        return "update"
    return "n/a"


class Object(object):
    def __init__(self):
        super(Object, self).__init__()
        self.id = str(uuid.uuid4())


def __event_id(obj_id, button):
    return "{}::{}".format(obj_id, button_name(button))


def __execute(event, cmd, wait=False):
    try:
        util.cli.execute(
            cmd.format(instance=event.get("instance", ""), name=event.get("name", ""),),
            wait=wait,
            shell=True,
        )
    except Exception as e:
        logging.error("failed to invoke callback: {}".format(e))


def register(obj, button=None, cmd=None, wait=False):
    event_id = __event_id(obj.id if obj is not None else "", button)
    logging.debug("registering callback {}".format(event_id))
    core.event.unregister(event_id) # make sure there's always only one input event

    if callable(cmd):
        core.event.register_exclusive(event_id, cmd)
    elif obj and hasattr(obj, cmd) and callable(getattr(obj, cmd)):
        core.event.register_exclusive(event_id, lambda event: getattr(obj, cmd)(event))
    else:
        core.event.register_exclusive(event_id, lambda event: __execute(event, cmd, wait))


def trigger(event):
    if not "button" in event:
        return

    triggered = False
    for field in ["instance", "name"]:
        if not field in event:
            continue
        if core.event.trigger(__event_id(event[field], event["button"]), event):
            triggered = True
    if not triggered:
        core.event.trigger(__event_id("", event["button"]), event)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
