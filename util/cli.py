import os
import shlex
import subprocess
import logging

def execute(cmd, wait=True, ignore_errors=False, include_stderr=False, env=None):
    args = shlex.split(cmd)
    logging.debug(cmd)
    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT if include_stderr else subprocess.PIPE, env=env)
    except FileNotFoundError as e:
       raise RuntimeError('{} not found'.format(cmd))

    if wait:
        out, _ = proc.communicate()
        if proc.returncode != 0:
            err = '{} exited with code {}'.format(cmd, proc.returncode)
            if ignore_errors:
                return err
            raise RuntimeError(err)
        return out.decode('utf-8')
    return ''

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
