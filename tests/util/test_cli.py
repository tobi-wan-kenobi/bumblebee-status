import pytest

import util.cli


def test_valid_command():
    assert util.cli.execute("echo test") == "test\n"


def test_utf_command():
    rv = util.cli.execute("echo ÖPmŧß")
    assert util.cli.execute("echo ÖPmŧß") == "ÖPmŧß\n"


def test_invalid_command():
    with pytest.raises(RuntimeError):
        util.cli.execute("i-do-not-exist")


def test_command_exit_code():
    with pytest.raises(RuntimeError):
        util.cli.execute("cat i-do-not-exist")


def test_command_exit_code_no_error():
    util.cli.execute("cat i-do-not-exist", ignore_errors=True)


def test_async():
    assert util.cli.execute("echo test", wait=False) == ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
