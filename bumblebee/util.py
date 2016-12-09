import shlex
import subprocess

try:
    from exceptions import RuntimeError
except ImportError:
    # Python3 doesn't require this anymore
    pass

def execute(cmd, wait=True):
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if wait:
        out, _ = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError("{} exited with {}".format(cmd, proc.returncode))
        return out.decode("utf-8")
    return None

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
