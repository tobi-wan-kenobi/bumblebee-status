"""Input classes"""

import sys
import json
import uuid
import time
import threading
import bumblebee.util

LEFT_MOUSE = 1
RIGHT_MOUSE = 3

def read_input(inp):
    """Read i3bar input and execute callbacks"""
    while inp.running:
        line = sys.stdin.readline().strip(",").strip()
        inp.has_event = True
        try:
            event = json.loads(line)
            inp.callback(event)
        except ValueError:
            pass
    inp.has_event = True
    inp.clean_exit = True

class I3BarInput(object):
    """Process incoming events from the i3bar"""
    def __init__(self):
        self.running = True
        self._callbacks = {}
        self.clean_exit = False
        self.global_id = str(uuid.uuid4())
        self.need_event = False
        self.has_event = False

    def start(self):
        """Start asynchronous input processing"""
        self.has_event = False
        self.running = True
        self._thread = threading.Thread(target=read_input, args=(self,))
        self._thread.start()

    def alive(self):
        """Check whether the input processing is still active"""
        return self._thread.is_alive()

    def _wait(self):
        while not self.has_event:
            time.sleep(0.1)
        self.has_event = False

    def stop(self):
        """Stop asynchronous input processing"""
        if self.need_event:
            self._wait()
        self.running = False
        self._thread.join()
        return self.clean_exit

    def register_callback(self, obj, button, cmd):
        """Register a callback function or system call"""
        uid = self.global_id
        if obj:
            uid = obj.id

        if uid not in self._callbacks:
            self._callbacks[uid] = {}
        self._callbacks[uid][button] = cmd

    def callback(self, event):
        """Execute callback action for an incoming event"""
        cmd = self._callbacks.get(self.global_id, {})
        cmd = self._callbacks.get(event["name"], cmd)
        cmd = self._callbacks.get(event["instance"], cmd)
        cmd = cmd.get(event["button"], None)
        if cmd is None:
            return
        if callable(cmd):
            cmd(event)
        else:
            bumblebee.util.execute(cmd)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
