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

def bytefmt(num):
    for unit in [ "", "Ki", "Mi", "Gi" ]:
        if num < 1024.0:
            return "{:.2f}{}B".format(num, unit)
        num /= 1024.0
    return "{:.2f}GiB".format(num*1024.0)

def durationfmt(duration):
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    res = "{:02d}:{:02d}".format(minutes, seconds)
    if hours > 0: res = "{:02d}:{}".format(hours, res)

    return res

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
