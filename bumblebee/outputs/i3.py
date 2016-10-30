import json

class i3bar:
    def preamble(self):
        return json.dumps({ "version": 1 }) + "["

    def data(self, data):
        return json.dumps(data) + ","

    def finalize(self):
        return "]"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
