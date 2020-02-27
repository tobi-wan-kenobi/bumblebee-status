import util.format

def scrollable(func):
    def wrapper(module, widget):
        text = func(module, widget)
        if not text:
            return text
        width = widget.get('theme.width', util.format.asint(module.parameter('width', 30)))
        if util.format.asbool(module.parameter('scrolling.makewide', True)):
            widget.set('theme.minwidth', 'A'*width)
        if width < 0 or len(text) <= width:
            return text

        bounce = util.format.asbool(module.parameter('scrolling.bounce', True))
        scroll_speed = util.format.asint(module.parameter('scrolling.speed', 1))
        start = widget.get('scrolling.start', 0)

        if start + width > len(text):
            if bounce:
                widget.set('scrolling.direction', 'left')
                start -= scroll_speed*2
            else:
                start = 0
        elif start < 0:
            if bounce:
                widget.set('scrolling.direction', 'right')
        direction = widget.get('scrolling.direction', 'right')
        if direction == 'left':
            scroll_speed = -scroll_speed
        widget.set('scrolling.start', start + scroll_speed)
        text = text[start:width+start]

        return text
    return wrapper

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
