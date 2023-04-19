from unittest import TestCase, mock

import pytest
from requests import Session

import core.config
import core.widget
import modules.contrib.todoist

pytest.importorskip("requests")


def build_todoist_module(todoist_filter=None):
    config = core.config.Config([
        "-p",
        f"todoist.filter={todoist_filter}" if todoist_filter else ""
    ])

    return modules.contrib.todoist.Module(config=config, theme=None)


def mock_tasks_api_response():
    res = mock.Mock()
    res.json = lambda: [
        {
            "id": "-1",
            "project_id": "-1"
        },
        {
            "id": "-2",
            "project_id": "-2"
        }
    ]

    res.status_code = 200
    return res


class TestTodoistUnit(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.todoist")

    @mock.patch.object(Session, "get", return_value=mock_tasks_api_response())
    def test_default_values(self, mock_get):
        module = build_todoist_module()
        module.update()
        assert module.widgets()[0].full_text() == "2"

        mock_get.assert_called_with('https://api.todoist.com/rest/v2/tasks', params=None)

    @mock.patch.object(Session, "get", return_value=mock_tasks_api_response())
    def test_custom_filter(self, mock_get):
        module = build_todoist_module(todoist_filter="!assigned to: others & (Overdue | due: today)")
        module.update()
        assert module.widgets()[0].full_text() == "2"

        mock_get.assert_called_with('https://api.todoist.com/rest/v2/tasks',
                                    params={'filter': '!assigned to: others & (Overdue | due: today)'})
