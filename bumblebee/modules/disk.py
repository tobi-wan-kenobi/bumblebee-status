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
    def __init__(self, output, config):
        super(Module, self).__init__(output, config)
        self._path = self._config.parameter("disk.path", "/")

# TODO
#        output.add_callback(module=self.__module__, button=1,
#            cmd="nautilus {instance}")

    def widgets(self):
        st = os.statvfs(self._path)

        self._size = st.f_frsize*st.f_blocks
        self._used = self._size - st.f_frsize*st.f_bavail
        self._perc = 100.0*self._used/self._size

        return bumblebee.output.Widget(self,
            "{} {}/{} ({:05.02f}%)".format(self._path,
            bumblebee.util.bytefmt(self._used),
            bumblebee.util.bytefmt(self._size), self._perc)
        )

    def instance(self, widget):
        return self._path

    def warning(self, widget):
        return self._perc > self._config.parameter("disk.warning", 80)

    def critical(self, widget):
        return self._perc > self._config.parameter("disk.critical", 90)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
