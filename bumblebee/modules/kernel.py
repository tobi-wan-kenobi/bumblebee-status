import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._release_name = bumblebee.util.execute("uname -r")[:-1]

    def output(self, widget):
        return self._release_name
