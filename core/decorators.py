import util.format


def never(init):
    def call_init(obj, *args, **kwargs):
        init(obj, *args, **kwargs)
        if obj.parameter("interval") is None:
            obj.set("interval", "never")

    return call_init


def every(hours=0, minutes=0, seconds=0):
    def decorator_init(init):
        def call_init(obj, *args, **kwargs):
            init(obj, *args, **kwargs)
            if obj.parameter("interval") is None:
                obj.set("interval", hours * 3600 + minutes * 60 + seconds)

        return call_init

    return decorator_init


def scrollable(func):
    def wrapper(module, widget):
        text = func(module, widget)
        if not text:
            return text
        width = widget.get(
            "theme.width", util.format.asint(module.parameter("width", 30))
        )
        if util.format.asbool(module.parameter("scrolling.makewide", True)):
            widget.set("theme.minwidth", "A" * width)
        if width < 0 or len(text) <= width:
            return text

        start = widget.get("scrolling.start", 0)
        bounce = util.format.asbool(module.parameter("scrolling.bounce", True))
        scroll_speed = util.format.asint(module.parameter("scrolling.speed", 1))
        direction = widget.get("scrolling.direction", "right")

        if direction == "left":
            if start - scroll_speed <= 0:  # bounce back
                widget.set("scrolling.direction", "right")
            else:
                scroll_speed *= -1
        else:
            if start + scroll_speed + width > len(text):
                if not bounce:
                    start = -scroll_speed
                else:
                    start = len(text) - width
                    scroll_speed *= -1
                    widget.set("scrolling.direction", "left")

        next_start = start + scroll_speed
        widget.set("scrolling.start", next_start)

        return text[start:start + width]

    return wrapper


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
