import os
import shlex
import subprocess
import logging


def execute(
    cmd,
    wait=True,
    ignore_errors=False,
    include_stderr=False,
    env=None,
    return_exitcode=False,
    shell=False,
):
    """Executes a commandline utility and returns its output

    :param cmd: the command (as string) to execute, returns the program's output
    :param wait: set to True to wait for command completion, False to return immediately, defaults to True
    :param ignore_errors: set to True to return a string when an exception is thrown, otherwise might throw, defaults to False
    :param include_stderr: set to True to include stderr output in the return value, defaults to False
    :param env: provide a dict here to specify a custom execution environment, defaults to None
    :param return_exitcode: set to True to return a pair, where the first member is the exit code and the message the second, defaults to False
    :param shell: set to True to run command in a separate shell, defaults to False

    :raises RuntimeError: the command either didn't exist or didn't exit cleanly, and ignore_errors was set to False

    :return: output of cmd, or stderr, if ignore_errors is True and the command failed; or a tuple of exitcode and the previous, if return_exitcode is set to True
    :rtype: string or tuple (if return_exitcode is set to True)
    """
    args = cmd if shell else shlex.split(cmd)
    logging.debug(cmd)

    if not env:
        env = os.environ.copy()

    myenv = env.copy()

    myenv["LC_ALL"] = "C"
    if "WAYLAND_SOCKET" in myenv:
        del myenv["WAYLAND_SOCKET"]

    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if include_stderr else subprocess.PIPE,
            env=myenv,
            shell=shell,
        )
    except FileNotFoundError as e:
        raise RuntimeError("{} not found".format(cmd))

    if wait:
        out, _ = proc.communicate()
        if proc.returncode != 0:
            err = "{} exited with code {}".format(cmd, proc.returncode)
            logging.warning(err)
            if ignore_errors:
                return (proc.returncode, err) if return_exitcode else err
            raise RuntimeError(err)
        res = out.decode("utf-8")
        logging.debug(res)
        return (proc.returncode, res) if return_exitcode else res
    return (0, "") if return_exitcode else ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
