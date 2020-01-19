import importlib
import logging

log = logging.getLogger(__name__)

def load(module_name):
    try:
        mod = importlib.import_module('modules.{}'.format(module_name))
    except ImportError as error:
        log.fatal('failed to import {}: {}'.format(module_name, str(error)))
        return Error(module_name)
    return getattr(mod, 'Module')()

class Module(object):
    def update(self):
        pass

class Error(Module):
    def __init__(self, loaded_module_name):
        self._loaded_module_name = loaded_module_name

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
