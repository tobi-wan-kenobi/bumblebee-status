# pylint: disable=C0103,C0111

import mock
import shlex
import subprocess

class MockPopen(object):
    def __init__(self, module):
        self._patch = mock.patch("{}.subprocess.Popen".format(module))
        self._popen = self._patch.start()
        self.mock = mock.Mock()
        # for a nicer, more uniform interface
        self.mock.popen = self._popen
        # for easier command execution checks
        self.mock.popen.assert_call = self.assert_call
        self._popen.return_value = self.mock

        self.mock.communicate.return_value = [ "", None ]
        self.mock.returncode = 0

    def assert_call(self, cmd):
        self.mock.popen.assert_called_with(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def cleanup(self):
        self._patch.stop()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
