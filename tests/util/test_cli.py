import unittest

import util.cli


class cli(unittest.TestCase):
    def setUp(self):
        self.nonExistentCommand = "i-do-not-exist"
        self.validCommand = "echo test"
        self.validCommandOutput = "test\n"
        self.utfCommand = "echo ÖPmŧß"
        self.utfCommandOutput = "ÖPmŧß\n"

    def test_valid_command(self):
        rv = util.cli.execute(self.validCommand)
        self.assertEqual(self.validCommandOutput, rv)

    def test_utf_command(self):
        rv = util.cli.execute(self.utfCommand)
        self.assertEqual(self.utfCommandOutput, rv)

    def test_invalid_command(self):
        with self.assertRaises(RuntimeError):
            util.cli.execute(self.nonExistentCommand)

    def test_command_exit_code(self):
        with self.assertRaises(RuntimeError):
            util.cli.execute("cat {}".format(self.nonExistentCommand))

    def test_command_exit_code_no_error(self):
        try:
            util.cli.execute(
                "cat {}".format(self.nonExistentCommand), ignore_errors=True
            )
        except Exception:
            self.fail("exception was thrown")

    def test_async(self):
        rv = util.cli.execute(self.validCommand, wait=False)
        self.assertEqual("", rv)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
