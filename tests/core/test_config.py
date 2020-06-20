import os
import pytest

import core.config


@pytest.fixture
def defaultConfig():
    return core.config.Config([])


def test_module():
    modules = ["module-1", "module-2", "module-3"]

    cfg = core.config.Config(["-m"] + modules)

    assert cfg.modules() == modules


def test_module_ordering_maintained():
    modules = ["module-1", "module-5", "module-7"]
    more_modules = ["module-0", "module-2", "aaa"]

    cfg = core.config.Config(["-m"] + modules + ["-m"] + more_modules)

    assert cfg.modules() == modules + more_modules


def test_default_interval(defaultConfig):
    assert defaultConfig.interval() == 1


def test_interval():
    interval = 4
    cfg = core.config.Config(["-p", "interval={}".format(interval)])

    assert cfg.interval() == interval


def test_floating_interval():
    interval = 4.5
    cfg = core.config.Config(["-p", "interval={}".format(interval)])

    assert cfg.interval() == interval


def test_default_theme(defaultConfig):
    assert defaultConfig.theme() == "default"


def test_theme():
    theme_name = "sample-theme"
    cfg = core.config.Config(["-t", theme_name])
    assert cfg.theme() == theme_name


def test_default_iconset(defaultConfig):
    assert defaultConfig.iconset() == "auto"


def test_iconset():
    iconset_name = "random-iconset"
    cfg = core.config.Config(["-i", iconset_name])
    assert cfg.iconset() == iconset_name


def test_reverse(defaultConfig):
    assert defaultConfig.reverse() == False

    cfg = core.config.Config(["-r"])

    assert cfg.reverse() == True


def test_logfile(defaultConfig):
    assert defaultConfig.logfile() is None

    logfile = "some-random-logfile"
    cfg = core.config.Config(["-f", logfile])
    assert cfg.logfile() == logfile


def test_all_modules():
    modules = core.config.all_modules()
    assert len(modules) > 0

    for module in modules:
        pyname = "{}.py".format(module)
        base = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "..",
                "..",
                "bumblebee_status",
                "modules",
            )
        )
    assert os.path.exists(os.path.join(base, "contrib", pyname)) or os.path.exists(
        os.path.join(base, "core", pyname)
    )


def test_list_output(mocker):
    mocker.patch("core.config.sys")
    cfg = core.config.Config(["-l", "themes"])
    cfg = core.config.Config(["-l", "modules"])
    cfg = core.config.Config(["-l", "modules-rst"])


def test_missing_parameter():
    cfg = core.config.Config(["-p", "test.key"])

    assert cfg.get("test.key") == None
    assert cfg.get("test.key", "no-value-set") == "no-value-set"


#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
