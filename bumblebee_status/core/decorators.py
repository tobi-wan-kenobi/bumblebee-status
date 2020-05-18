import difflib
import logging

import util.format

log = logging.getLogger(__name__)


"""Specifies that a module should never update (i.e. has static content).
This means that its update() method will never be invoked

:param init: The __init__() method of the module

:return: Wrapped method that sets the module's interval to "never"
"""


def never(init):
    def call_init(obj, *args, **kwargs):
        init(obj, *args, **kwargs)
        if obj.parameter("interval") is None:
            obj.set("interval", "never")

    return call_init


"""Specifies the interval for executing the module's update() method

:param hours: Hours between two update() invocations, defaults to 0
:param minutes: Minutes between two update() invocations, defaults to 0
:param seconds: Seconds between two update() invocations, defaults to 0

:return: Wrapped method that sets the module's interval correspondingly
"""


def every(hours=0, minutes=0, seconds=0):
    def decorator_init(init):
        def call_init(obj, *args, **kwargs):
            init(obj, *args, **kwargs)
            if obj.parameter("interval") is None:
                obj.set("interval", hours * 3600 + minutes * 60 + seconds)

        return call_init

    return decorator_init


"""Specifies that the module's content should scroll, if required

The exact behaviour of this method is governed by a number of parameters,
specifically: The module's parameter "scrolling.width"  specifies the width when
scrolling starts, "scrolling.makewide" defines whether the module should be expanded
to "scrolling.width" automatically, if the content is shorter, the parameter
"scrolling.bounce" defines whether it scrolls like a marquee (False) or should bounce
when the end of the content is reached. "scrolling.speed" defines the number of characters
to scroll each iteration.

:param func: Function for which the result should be scrolled
"""


def scrollable(func):
    def wrapper(module, widget):
        text = func(module, widget)
        if not text:
            return text

        if (
            difflib.SequenceMatcher(a=text, b=widget.get("__content__", text)).ratio()
            < 0.9
        ):
            widget.set("scrolling.start", 0)
            widget.set("scrolling.direction", "right")
        widget.set("__content__", text)

        width = util.format.asint(module.parameter("scrolling.width", 30))
        if util.format.asbool(module.parameter("scrolling.makewide", True)):
            widget.set("theme.minwidth", "A" * width)
        if width < 0 or len(text) <= width:
            return text

        start = widget.get("scrolling.start", 0)
        bounce = util.format.asbool(module.parameter("scrolling.bounce", True))
        scroll_speed = util.format.asint(module.parameter("scrolling.speed", 1))
        direction = widget.get("scrolling.direction", "right")

        if direction == "left":
            if start - scroll_speed < 0:  # bounce back
                widget.set("scrolling.direction", "right")
            else:
                scroll_speed = -scroll_speed

        next_start = start + scroll_speed
        if next_start + width > len(text):
            if not bounce:
                next_start = 0
            else:
                next_start = start - scroll_speed
                widget.set("scrolling.direction", "left")

        widget.set("scrolling.start", next_start)

        return text[start : start + width]

    return wrapper


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
