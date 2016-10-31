import os
import bumblebee.util
import bumblebee.module

class Module(bumblebee.module.Module):
    def __init__(self, args):
        super(Module, self).__init__(args)
        self._path = args[0] if args else "/"

    def data(self):
        st = os.statvfs(self._path)

        self._size = st.f_frsize*st.f_blocks
        self._free = st.f_frsize*st.f_bavail
        self._perc = 100.0*self._free/self._size

        return "{} {}/{} ({:05.02f}%)".format(self._path, bumblebee.util.bytefmt(self._free), bumblebee.util.bytefmt(self._size), self._perc)

    def warning(self):
        return self._perc < 20

    def critical(self):
        return self._perc < 10

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
