from unittest import TestCase, mock

import pytest
from requests import Session

import core.config
import core.widget
import modules.contrib.wakatime

pytest.importorskip("requests")


def build_wakatime_module(waka_format=None, waka_range=None):
    config = core.config.Config([
        "-p",
        f"wakatime.format={waka_format}" if waka_format else "",
        f"wakatime.range={waka_range}" if waka_range else ""
    ])

    return modules.contrib.wakatime.Module(config=config, theme=None)


def mock_summaries_api_response():
    res = mock.Mock()
    res.json = lambda: {
        "cumulative_total": {
            "text": "3 hrs 2 mins",
            "seconds": 10996,
            "digital": "3:02",
            "decimal": "3.03"
        },
    }

    res.status_code = 200
    return res


class TestWakatimeUnit(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.wakatime")

    @mock.patch.object(Session, "get", return_value=mock_summaries_api_response())
    def test_default_values(self, mock_get):
        module = build_wakatime_module()
        module.update()
        assert module.widgets()[0].full_text() == "3:02"

        mock_get.assert_called_with('https://wakatime.com/api/v1/users/current/summaries?range=Today')

    @mock.patch.object(Session, "get", return_value=mock_summaries_api_response())
    def test_custom_configs(self, mock_get):
        module = build_wakatime_module(waka_format="text", waka_range="last 7 days")
        module.update()
        assert module.widgets()[0].full_text() == "3 hrs 2 mins"

        mock_get.assert_called_with('https://wakatime.com/api/v1/users/current/summaries?range=last 7 days')
