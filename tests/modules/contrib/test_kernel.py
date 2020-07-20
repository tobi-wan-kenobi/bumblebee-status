import pytest

import core.config
import modules.contrib.kernel


@pytest.fixture
def some_kernel():
    return "this-is-my-kernel"


@pytest.fixture
def kernel_module():
    return modules.contrib.kernel.Module(config=core.config.Config([]), theme=None)


def test_full_text(mocker, kernel_module):
    platform = mocker.patch("modules.contrib.kernel.platform")
    platform.release.return_value = some_kernel
    assert len(kernel_module.widgets()) == 1
    assert some_kernel == kernel_module.widget().full_text()


def test_load_module():
    __import__("modules.contrib.kernel")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
