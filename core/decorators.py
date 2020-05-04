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

        if text != widget.get("__content__", text):
            widget.set("scrolling.start", 0)
            widget.set("scrolling.direction", "right")
        widget.set("__content__", text)

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
            scroll_speed = -scroll_speed
            if start + scroll_speed <= 0:  # bounce back
                widget.set("scrolling.direction", "right")

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
