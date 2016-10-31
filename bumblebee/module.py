
class Module(object):
    def __init__(self, args):
        pass

    def data(self):
        pass

    def critical(self):
        return False

    def warning(self):
        return False

    def state(self):
        return "default"

    def next(self):
        return False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
