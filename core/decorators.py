import util.format

def scrollable(func):
    def wrapper(module, widget):
        text = func(module, widget)
        widget.set('_raw', text)
        if not text:
            return text
        width = widget.get('theme.width', util.format.asint(module.parameter('width', 30)))
        if util.format.asbool(module.parameter('scrolling.makewide', True)):
            widget.set('theme.minwidth', 'A'*width)
        if width < 0 or len(text) <= width:
            return text

        start = widget.get('scrolling.start', 0)
        bounce = util.format.asbool(module.parameter('scrolling.bounce', True))
        scroll_speed = util.format.asint(module.parameter('scrolling.speed', 1))
        direction = widget.get('scrolling.direction', 'right')

        if direction == 'left':
            scroll_speed = -scroll_speed
            if start + scroll_speed <= 0: # bounce back
                widget.set('scrolling.direction', 'right')

        next_start = start + scroll_speed
        if next_start + width > len(text):
            if not bounce:
                next_start = 0
            else:
                next_start = start - scroll_speed
                widget.set('scrolling.direction', 'left')

        widget.set('scrolling.start', next_start)

        return text[start:start+width]
    return wrapper

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
