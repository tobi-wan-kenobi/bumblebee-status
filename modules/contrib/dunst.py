#pylint: disable=C0111,R0903

"""Toggle dunst notifications."""

import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                bumblebee.output.Widget(full_text="")
        )
        self._paused = False
        # Make sure that dunst is currently not paused
        try:
            bumblebee.util.execute("killall -SIGUSR2 dunst")
        except:
            pass
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                cmd=self.toggle_status
        )

    def toggle_status(self, event):
        self._paused = not self._paused
        
        try:
            if self._paused:
                bumblebee.util.execute("killall -SIGUSR1 dunst")
            else:
                bumblebee.util.execute("killall -SIGUSR2 dunst")
        except:
            self._paused = not self._paused # toggling failed

    def state(self, widget):
        if self._paused:
            return ["muted", "warning"]
        return ["unmuted"]
