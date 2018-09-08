# pylint: disable=C0103,C0111

import unittest
import re

import tests.mocks as mocks

import bumblebee.util as bu


class TestUtil(unittest.TestCase):
    def setUp(self):
        self.popen = mocks.MockPopen("bumblebee.util")
        self.some_command_with_args = "sample-command -a -b -c"
        self.some_utf8 = "some string".encode("utf-8")

    def tearDown(self):
        self.popen.cleanup()

    def test_bytefmt(self):
        self.assertEquals(bu.bytefmt(10), "10.00B")
        self.assertEquals(bu.bytefmt(15 * 1024), "15.00KiB")
        self.assertEquals(bu.bytefmt(20 * 1024 * 1024), "20.00MiB")
        self.assertEquals(bu.bytefmt(22 * 1024 * 1024 * 1024), "22.00GiB")
        self.assertEquals(bu.bytefmt(35 * 1024 * 1024 * 1024 * 1024), "35840.00GiB")

    def test_durationfmt(self):
        self.assertEquals(bu.durationfmt(00), "00:00")
        self.assertEquals(bu.durationfmt(25), "00:25")
        self.assertEquals(bu.durationfmt(60), "01:00")
        self.assertEquals(bu.durationfmt(119), "01:59")
        self.assertEquals(bu.durationfmt(3600), "01:00:00")
        self.assertEquals(bu.durationfmt(7265), "02:01:05")

    def test_execute(self):
        bu.execute(self.some_command_with_args)
        self.assertTrue(self.popen.mock.popen.called)
        self.popen.mock.popen.assert_call(self.some_command_with_args)
        self.assertTrue(self.popen.mock.communicate.called)

    def test_execute_nowait(self):
        bu.execute(self.some_command_with_args, False)
        self.assertTrue(self.popen.mock.popen.called)
        self.popen.mock.popen.assert_call(self.some_command_with_args)
        self.assertFalse(self.popen.mock.communicate.called)

    def test_execute_utf8(self):
        self.popen.mock.communicate.return_value = [self.some_utf8, None]
        self.test_execute()

    def test_execute_error(self):
        self.popen.mock.returncode = 1

        with self.assertRaises(RuntimeError):
            bu.execute(self.some_command_with_args)

    def test_which(self):
        # test for a binary that has to be somewhere
        print(bu.which("ls"))
        self.assertTrue(re.search('/(ls)$', bu.which("ls")))

        # test for a binary that is not necessarily there
        program = "iwgetid"
        self.assertTrue(
            bu.which(program) is None or
            re.search('/(' + program + ')$', bu.which(program))
        )

        # test if which also works with garbage input
        self.assertTrue(bu.which("qwertygarbage") is None)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
