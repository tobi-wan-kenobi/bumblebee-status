import bumblebee.module
import subprocess
import os

def description():
    return "Displays available updates per repository for pacman."

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._count = 0

    def widgets(self):
        path = os.path.dirname(os.path.abspath(__file__))
        if self._count == 0:
            self._out = "?/?/?/?"
            process = subprocess.Popen([ "{}/../../bin/customupdates".format(path) ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self._query, self._error = process.communicate()

            if not process.returncode == 0:
                self._out = "?/?/?/?"
            else:
                self._community = 0
                self._core = 0
                self._extra = 0
                self._other = 0

                for line in self._query.splitlines():
                    if line.startswith(b'http'):
                        if b"community" in line:
                            self._community += 1
                            continue
                        if b"core" in line:
                            self._core += 1;
                            continue
                        if b"extra" in line:
                            self._extra += 1
                            continue
                        self._other += 1
                self._out = str(self._core)+"/"+str(self._extra)+"/"+str(self._community)+"/"+str(self._other)
            
        self._count += 1
        self._count = 0 if self._count > 300 else self._count
        return bumblebee.output.Widget(self, "{}".format(self._out))

    def sumUpdates(self):
        return self._core + self._community + self._extra + self._other 
    
    def critical(self, widget):
        #return self._sumUpdates(self)
        return self.sumUpdates() > 0





# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
