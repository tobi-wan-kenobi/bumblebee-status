"""Core application engine"""

class Engine(object):
    """Engine for driving the application

    This class connects input/output, instantiates all
    required modules and drives the "event loop"
    """
    def __init__(self, config):
        self._running = True

    def running(self):
        """Check whether the event loop is running"""
        return self._running

    def stop(self):
        """Stop the event loop"""
        self._running = False

    def run(self):
        """Start the event loop"""
        while self.running():
            pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
