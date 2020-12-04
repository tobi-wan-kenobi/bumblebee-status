import pytest

from util.format import *


def test_int_from_string():
    assert asint("100") == 100
    assert asint("-100") == -100
    assert asint("0") == 0


def test_int_from_none():
    assert asint(None) == 0


def test_int_from_int():
    assert asint(100) == 100
    assert asint(-100) == -100
    assert asint(0) == 0


def test_int_minimum():
    assert asint(100, minimum=10) == 100
    assert asint(100, minimum=100) == 100
    assert asint(5, minimum=10) == 10


def test_int_maximum():
    assert asint(100, maximum=200) == 100
    assert asint(100, maximum=100) == 100
    assert asint(200, maximum=100) == 100


def test_true_from_str():
    assert asbool("true") == True
    assert asbool(True) == True
    assert asbool("t") == True
    assert asbool("1") == True
    assert asbool("yes") == True
    assert asbool("y") == True
    assert asbool("on") == True


def test_false_from_str():
    assert asbool("false") == False
    assert asbool(False) == False
    assert asbool("f") == False
    assert asbool("0") == False
    assert asbool("no") == False
    assert asbool("n") == False
    assert asbool("off") == False
    assert asbool(None) == False


def test_list_from_None():
    assert aslist(None) == []


def test_list_from_list():
    assert aslist([1, 2, 3] == [1, 2, 3])


def test_list_from_str():
    assert aslist("12,13,14") == ["12", "13", "14"]


def test_byteformat():
    assert byte(500) == "500.00B"
    assert byte(1024) == "1.00KiB"
    assert byte(1024, "{:.0f}") == "1KiB"
    assert byte(1024 + 512) == "1.50KiB"
    assert byte(1024 * 1024 * 2 + 1024 * 512) == "2.50MiB"
    assert byte(1024 * 1024 * 1024 * 4 + 1024 * 1024 * 512) == "4.50GiB"
    assert byte(1024 * 1024 * 1024 * 1024 * 2) in ["2048.00GiB", "2.00TiB"]


def test_duration():
    assert duration(4 * 60 * 60 + 20 * 60) == "04:20:00"
    assert duration(4 * 60 * 60 + 20 * 60, unit=True) == "04:20:00h"
    assert duration(4 * 60 * 60 + 20 * 60, compact=True, unit=True) == "04:20h"

    assert duration(20 * 60) == "20:00"
    assert duration(20 * 60, unit=True) == "20:00m"
    assert duration(20 * 60, compact=True, unit=True) == "20:00m"

    assert duration(20) == "00:20"
    assert duration(20, unit=True) == "00:20m"
    assert duration(20, compact=True, unit=True) == "00:20m"

    assert duration(-1) == "n/a"


def test_seconds():
    assert seconds(10) == 10
    assert seconds("10") == 10

    assert seconds("5m") == 300
    assert seconds("5m20s") == 320

    assert seconds("4h") == 4 * 3600
    assert seconds("4h5m22s") == 4 * 3600 + 5 * 60 + 22

    assert seconds("4h5m") == 4 * 3600 + 5 * 60


def test_temperature():
    assert astemperature(10) == "10°C"
    assert astemperature(10, "metric") == "10°C"
    assert astemperature(-100, "imperial") == "-100°F"
    assert astemperature(-100, "kelvin") == "-100°K"


def test_temperature_case():
    assert astemperature(100, "ImPeRiAl") == "100°F"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
