import os
import bumblebee.util
import bumblebee.module

def usage():
    return "disk or disk::<path, defaults to '/'>"

def notes():
    return "Warning is at 20% free diskspace, Critical at 10%."

def description():
    return "Shows free diskspace, total diskspace and the percentage of free disk space."

class Module(bumblebee.module.Module):
    def __init__(self, output, args):
        super(Module, self).__init__(args)
        self._path = args[0] if args else "/"

        output.add_callback(module=self.__module__, button=1,
            cmd="nautilus {instance}")

    def data(self):
        st = os.statvfs(self._path)

        self._size = st.f_frsize*st.f_blocks
        self._used = self._size - st.f_frsize*st.f_bavail
        self._perc = 100.0*self._used/self._size

        return "{} {}/{} ({:05.02f}%)".format(self._path, bumblebee.util.bytefmt(self._used), bumblebee.util.bytefmt(self._size), self._perc)

    def instance(self):
        return self._path

    def warning(self):
        return self._perc > 80

    def critical(self):
        return self._perc > 90

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
