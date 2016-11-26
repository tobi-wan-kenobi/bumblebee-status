import shlex
import exceptions
import subprocess

def bytefmt(num):
    for unit in [ "", "Ki", "Mi", "Gi" ]:
        if num < 1024.0:
            return "{:.2f}{}B".format(num, unit)
        num /= 1024.0
    return "{:05.2f%}{}GiB".format(num)

def durationfmt(duration):
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    res = "{:02d}:{:02d}".format(minutes, seconds)
    if hours > 0: res = "{:02d}:{}".format(hours, res)

    return res

def execute(cmd):
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()

    if p.returncode != 0:
        raise exceptions.RuntimeError("{} exited with {}".format(cmd, p.returncode))
