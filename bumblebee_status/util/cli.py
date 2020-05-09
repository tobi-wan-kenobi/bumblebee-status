import os
import shlex
import subprocess
import logging


def execute(cmd, wait=True, ignore_errors=False, include_stderr=False, env=None):
    """Executes a commandline utility and returns its output

    :param cmd: the command (as string) to execute, returns the program's output
    :param wait: set to True to wait for command completion, False to return immediately, defaults to True
    :param ignore_errors: set to True to return a string when an exception is thrown, otherwise might throw, defaults to False
    :param include_stderr: set to True to include stderr output in the return value, defaults to False
    :param env: provide a dict here to specify a custom execution environment, defaults to None

    :raises RuntimeError: the command either didn't exist or didn't exit cleanly, and ignore_errors was set to False

    :return: output of cmd, or stderr, if ignore_errors is True and the command failed
    :rtype: string
    """
    args = shlex.split(cmd)
    logging.debug(cmd)
    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if include_stderr else subprocess.PIPE,
            env=env,
        )
    except FileNotFoundError as e:
        raise RuntimeError("{} not found".format(cmd))

    if wait:
        out, _ = proc.communicate()
        if proc.returncode != 0:
            err = "{} exited with code {}".format(cmd, proc.returncode)
            if ignore_errors:
                return err
            raise RuntimeError(err)
        return out.decode("utf-8")
    return ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
