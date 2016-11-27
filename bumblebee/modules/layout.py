import subprocess
import shlex
import bumblebee.module
import bumblebee.util

def description():
    return "Showws current keyboard layout and change it on click."

#def parameters():
#    module = __name__.split(".")[-1]
#    return 


class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)


        # click
        output.add_callback(module="layout.cir", button=1, cmd="setxkbmap us")
        output.add_callback(module="layout.us", button=1, cmd="setxkbmap rs")
        output.add_callback(module="layout.rs", button=1, cmd="setxkbmap -layout rs -variant latin")




    def widgets(self):
        output = subprocess.check_output(["setxkbmap", "-print"], stderr=subprocess.STDOUT)
        for line in str(output).split("\\n"):
            if "xkb_symbols" in line:
                res = line.split("\"")[1].split("+")[1]
        
        if res == "rs":
            return bumblebee.output.Widget(self, res, instance="layout.rs")
        elif res == "us":
            return bumblebee.output.Widget(self, res, instance="layout.us")
        else:
            return bumblebee.output.Widget(self, res, instance="layout.cir")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
