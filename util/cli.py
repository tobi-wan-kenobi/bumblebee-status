import os
import shlex
import subprocess
import logging

def execute(cmd, wait=True, ignore_errors=False):
    args = shlex.split(cmd)
    logging.debug(cmd)
    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except FileNotFoundError as e:
        raise RuntimeError('{} not found'.format(cmd))

    if wait:
        out, _ = proc.communicate()
        if proc.returncode != 0 and not ignore_errors:
            raise RuntimeError('{} exited with {}'.format(cmd, proc.returncode))
        return out.decode('utf-8')
    return ''

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
