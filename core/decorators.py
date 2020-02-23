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

        bounce = util.format.asint(module.parameter('scrolling.bounce', 1))
        scroll_speed = util.format.asint(module.parameter('scrolling.speed', 1))
        start = widget.get('scrolling.start', -1)
        direction = widget.get('scrolling.direction', 'right')
        start += scroll_speed if direction == 'right' else -(scroll_speed)

        if width + start > len(text) + (scroll_speed -1):
            if bounce:
                widget.set('scrolling.direction', 'left')
            else:
                start = 0
        elif start <= 0:
            if bounce:
                widget.set('scrolling.direction', 'right')
            else:
                start = len(text)
        widget.set('scrolling.start', start)
        text = text[start:width+start]

        return text
    return wrapper

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
