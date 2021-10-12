import sys
import pytest
from unittest.mock import Mock

import core.config

sys.modules['libvirt'] = Mock()

import modules.contrib.libvirtvms

def build_module():
    return modules.contrib.libvirtvms.Module(
        config=core.config.Config([]),
        theme=None
    )

def test_load_module():
    __import__("modules.contrib.libvirtvms")

def test_input_registration(mocker):
   input_register = mocker.patch('core.input.register')

   module = build_module()

   input_register.assert_called_with(
       module,
       button=core.input.LEFT_MOUSE,
       cmd="virt-manager"
   )

def test_status_failed(mocker):
    mocker.patch('libvirt.openReadOnly', return_value=None)

    module = build_module()
    status = module.status(None)

    assert status == "Failed to open connection to the hypervisor"

def test_status(mocker):
    virtMock = mocker.Mock()
    virtMock.numOfDomains = mocker.Mock(return_value=10)

    mocker.patch('libvirt.openReadOnly', return_value=virtMock)

    module = build_module()
    status = module.status(None)

    assert status == "VMs 10"
