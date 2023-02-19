import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.contrib.gitlab

from requests import Session
from requests.models import Response

pytest.importorskip("requests")


def build_gitlab_module(actions=""):
    config = core.config.Config(["-p", "gitlab.actions={}".format(actions)])
    return modules.contrib.gitlab.Module(config=config, theme=None)

def mock_todo_api_response():
    res = mock.Mock()
    res.json = lambda: [
        {"action_name": "assigned"},
        {"action_name": "assigned"},
        {"action_name": "approval_required"},
    ]
    res.status_code = 200
    return res

class TestGitlabUnit(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.gitlab")

    @mock.patch.object(Session, "get", return_value=mock_todo_api_response())
    def test_unfiltered(self, _):
        module = build_gitlab_module()
        module.update()
        assert module.widgets()[0].full_text() == "3"

    @mock.patch.object(Session, "get", return_value=mock_todo_api_response())
    def test_filtered(self, _):
        module = build_gitlab_module(actions="approval_required")
        module.update()
        assert module.widgets()[0].full_text() == "1"
